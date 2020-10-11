# import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import pandas as pd


# argv[1] will determine which forum to update
# if no argv then it will update everything


class Update:

    def __init__(self, driver, fiverr_url, date, arg1 = False):

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
                self.update_forum(data, driver, url, forum_urls.index(url), date)

        else:

                # Pick the index of the forum URLs with arg2
                # arg2 = 1 --> Update the Welcome threads
                # arg2 = 2 --> Update the COVID-19 Discussions threads
                # arg2 = 3 --> Update the Fiverr Tips threads
                # arg2 = 4 --> Update the Your Fiverr Experience threads
                # arg2 = 5 --> Update the Fiverr Site threads
                # arg2 = 6 --> Update the Events threads

                data = []
                self.update_forum(data, driver, forum_urls[int(arg1) - 1], int(arg1) - 1, date, True)

    def update_forum(self, data, driver, forum_url, forum_num, last_update, arg1 = False):

        print("Preparing to update...")

        # Get web page
        driver.get(forum_url)

        # Check last update date from data
        # Go in data and read the name, store it in last_update
        # last_update = ...

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

            # Else we have all the forum threads that were updated/posted on the page, start iterating from the last element towards the first one to sotre the updates on to data
            else:
                thread_urls.append(driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//a[starts-with(@class, 'title raw-link')]")[update_counter].get_attribute("href"))
                ThreadScraper(data, driver, url)
                update_counter -= 1

        # Update the csv file
        update_csv(data)

    # Converts the given string into datetime format
    # Example: "Sep 19, 2020 2:26pm" will be converted into
    def convert_date(self, date):
        date_list = date.split()

        month = date_list[0]
        day = date_list[1].split(",")[0]
        year = date_list[2]

    def update_csv(self, data):
        None


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
