# import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import pandas as pd
import zipfile

# argv[1] will determine which forum to update
# if no argv then it will update everything


class Update:

    def __init__(self, driver, fiverr_url, arg1 = False):

        # Get web page
        driver.get(fiverr_url)

        # Get the appropriate forum URLs
        forum_urls = []
        for element in driver.find_elements_by_xpath("//div[@class='column categories']//tr//td//h3//a"):
            forum_urls.append(element.get_attribute("href"))
            if(len(forum_urls) == 6):
                break

        if (arg1 == False):
            # Loop through the forum URLs and update them
            for url in forum_urls:
                data = []
                self.update_forum(data, driver, url, forum_urls.index(url))

        else:

                # Pick the index of the forum URLs with arg2
                # arg2 = 1 --> Update the Welcome threads
                # arg2 = 2 --> Update the COVID-19 Discussions threads
                # arg2 = 3 --> Update the Fiverr Tips threads
                # arg2 = 4 --> Update the Your Fiverr Experience threads
                # arg2 = 5 --> Update the Fiverr Site threads
                # arg2 = 6 --> Update the Events threads

                data = []
                self.update_forum(data, driver, forum_urls[int(arg1) - 1], int(arg1) - 1, True)

    def update_forum(self, data, driver, forum_url, forum_num, arg1 = False):

        print("Preparing to update...")

        # Get web page
        driver.get(forum_url)

        # Check last update date
        try:
            # Get the csv file - previously updated df = pud
            pud = get_last_updated_csv(forum_num)
            # Get the last update date from the file name of the csv
            last_update = str(min(os.listdir()))

        except:
            print("Failed to update the specified forum, could not find a previously updated csv zip")
            quit()

        # Scroll down until right before the given date
        # Check the date of the last forum element in the page and compare it to the last_update
        update_counter = len(driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr"))
        end_flag = False

        # Data to be updated
        data = []

        # Thread URLs to be scraped for updating
        thread_urls = []

        while(update_counter > 0):
            # If the last forum element "activity" is after the last_update --> scroll down to load more forum threads
            if((convert_date(str(driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//td[starts-with(@class, 'num age')]")[update_counter].title)) >= last_update) and end_flag == False):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                # Reset the counter since new forum posts appear when we scroll down
                update_counter = len(driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr"))
                # Corner case: If the loop reaches the end of the forum
                if(len(driver.find_elements_by_xpath("//footer[@class='topic-list-bottom']//div[@class='footer-message ember-view']//h3")) > 0):
                    end_flag = True
                time.sleep(5 .0)

            # Else we have all the forum threads that were updated/posted on the page, start iterating from the last element towards the first one to store the updates on to data
            else:
                thread_urls.append(driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//a[starts-with(@class, 'title raw-link')]")[update_counter].get_attribute("href"))
                # ThreadScraper(data, driver, url)
                update_counter -= 1

        # Scrape the threads


        # Update the csv file
        update_csv(data, forum_num, pud)

    def get_last_updated_csv(self, forum_num):

        extension = ''
        if forum_num == 0:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/welcome/')
            extension = '/data/welcome/'
        elif forum_num == 1:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')
            extension = '/data/covid-19_discussions/'
        elif forum_num == 2:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_tips/')
            extension = '/data/fiverr_tips/'
        elif forum_num == 3:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/your_fiverr_experience/')
            extension = '/data/your_fiverr_experience/'
        elif forum_num == 4:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_site/')
            extension = '/data/fiverr_site/'
        elif forum_num == 5:
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/events/')
            extension = '/data/events/'

        # Unzip the file
        csv_zip = str(min(os.listdir()))
        with zipfile.ZipFile(csv_zip, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)) + extension)

        # delete the zip file
        os.remove(csv_zip)

        # Return the csv in pandas dataframe
        return pd.read_csv(csv_zip.split(".")[0] + ".csv")



    # Converts the given string into datetime format
    # Example: "Sep 19, 2020 2:26pm" will be converted into
    def convert_date(self, date, forum_num):

        # TODO:

        date_list = date.split()

        month = date_list[0]
        day = date_list[1].split(",")[0]
        year = date_list[2]

    def update_csv(self, data, pud):

        print("Updating csv...")

        # Find rows with matching thread name or matching thread_id* from data in previously_updated_df
        # *thread_id is the last digits in the thread_url
        row_index = 0
        while(row_index < data.size - 1):

            # If the current forum rows exist in the pud then
            # replace the rows in previously_updated_df with newly collected data
            # if(pud["thread_url"].str.contains(str(data["thread_url"][row_index])) or pud["thread_name"].str.contains(str(data["thread_name"][row_index]))):
            if(pud["thread_url"].str.contains(str(data["thread_url"][row_index]))):

                # insert data rows into previously_updated_df
                # Get index of the first and last occurence of the matched forum threads
                index_list = pud[pud["thread_url"].str.contains(str(data["thread_url"][row_index]))].index.tolist()

                first_index = index_list[0]
                last_index = index_list[-1]

                # Create a new dataframe upto the first index --> df_1
                df_1 = pud.iloc[:index_list[0]]
                # Create a new dataframe starting from last index to the end of the csv --> df_2
                df_2 = pud.iloc[index_list[-1]:]

                try:
                    # Append df_1 with new data
                    # Append df_1 with df_2 --> pud
                    pud = df_1.append(data.iloc[row_index:(row_index + int(data["replies"][row_index]))]).append(df_2)

                except:
                    print("Something went wrong... ")
                    print("Failed to update " + str(data["thread_name"][row_index]))

            # The current forum row does not exist, insert it into the beginning of the previosuly_updated_df
            else:

                try:
                    pud = data.iloc[row_index:(row_index + int(data["replies"][row_index]))].append(pud)
                except:
                    print("Something went wrong... ")
                    print("Failed to update " + str(data["thread_name"][row_index]))

            #------------------------------------------------------------------------------------------#
            # Update index: skip through each forum thread instead of incrementing the loop index by 1
            replies = int(d["replies"][row_index])
            # If there are no replies skip to the next post
            try:
                 if(replies == 0):
                     row_index += 1
                 else:
                     row_index += replies
            except:
                row_index += 1


        # TODO:
        # Save new edited csv
        crawl_date = str(datetime.now()).split(" ")[0]
        filename = crawl_date + ".csv"


url = "https://forum.fiverr.com/"
t1 = datetime.now()

if(len(sys.argv) == 2):

    if(int(sys.argv[2]) > 6):
        print("Invalid options, cleaning up...")

    else:
        driver = webdriver.Chrome()
        #driver = webdriver.Chrome(options = options)
        Update(driver, url, date, sys.argv[1])
        driver.quit()
        print("Done!")

elif(len(sys.argv) == 1):
    driver = webdriver.Chrome()
    #driver = webdriver.Chrome(options = options)
    Update(driver, url, t1)
    driver.quit()
    print("Done!")

else:
    print("Invalid options, cleaning up...")

t2 = datetime.now()
delta = t2 - t1
print("Time elapsed: " + str(int(delta.total_seconds()/60)) + " minutes")
