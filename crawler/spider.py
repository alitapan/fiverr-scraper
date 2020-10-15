# Import Libraries
import sys
import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from scraper import ThreadScraper
from analysis import CompareThreads
from pathlib import Path
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import zipfile
import shutil

options = Options()
#options.headless = True
options.add_argument("--headless")

#--------------------------------------------------------------------------------------------------------------------------#

class Spider:

        def __init__(self, driver, fiverr_url, arg1 = False, arg2 = None, arg3 = False):

            # Get web page
            driver.get(fiverr_url)

            # Get the appropriate forum URLs
            forum_urls = []
            for element in driver.find_elements_by_xpath("//div[@class='column categories']//tr//td//h3//a"):
                forum_urls.append(element.get_attribute("href"))
                if(len(forum_urls) == 6):
                    break

            if (arg1 == False):
                # Loop through the forum URLs and scrape them
                for url in forum_urls:
                    data = []
                    self.crawl_forum(data, driver, url, forum_urls.index(url))
            else:

                # Pick the index of the forum URLs with arg2
                # arg2 = 1 --> Scrape the Welcome threads
                # arg2 = 2 --> Scrape the COVID-19 Discussions threads
                # arg2 = 3 --> Scrape the Fiverr Tips threads
                # arg2 = 4 --> Scrape the Your Fiverr Experience threads
                # arg2 = 5 --> Scrape the Fiverr Site threads
                # arg2 = 6 --> Scrape the Events threads

                data = []
                if(arg3 == True):
                    self.crawl_forum(data, driver, forum_urls[int(arg2) - 1], int(arg2) - 1, True, True)
                else:
                    self.crawl_forum(data, driver, forum_urls[int(arg2) - 1], int(arg2) - 1, True)

        def crawl_forum(self, data, driver, forum_url, forum_num, arg1 = False, cont = False, analysis = False):

            if cont == True:
                print("Continuing where the program left off last time...")

                # Change to the appropriate directory
                self.chdir_forum(forum_num)

                thread_urls = []
                # Get the text file and save_thread_urls
                try:
                    os.chdir('saved')
                    with open('saved_thread_urls.txt', 'r') as f:
                        thread_urls = f.readlines()
                    os.chdir('..')
                except:
                    print("There is no previous thread collection for the selected option")
                    print("Exiting program")
                    quit()

                # Get the index where it was left off
                counter = int(thread_urls[0])

                # Clean up the thread_urls
                thread_urls = thread_urls[1:]
                thread_urls = [x.strip() for x in thread_urls]

                # Unzip the previous data and load it into memory
                csv_zip = str(min(os.listdir()))
                with zipfile.ZipFile(csv_zip, 'r') as zip_ref:
                    zip_ref.extractall()

                # Delete the csv after loading to memory
                data_old = pd.read_csv(csv_zip.split(".")[0] + ".csv")
                os.remove(csv_zip.split(".")[0] + ".csv")

                # Start scraping starting at the specified index
                try:
                    for i in range(counter, len(thread_urls)):
                        # Scrape the thread
                        ThreadScraper(data, driver, thread_urls[i])
                        # After scraping the thread increment the counter. If we interrupt the program we can continue from where we left off by using this variable
                        counter += 1
                # If something goes wrong or the user interrupts the program, save the csv and the update the thread_urls text file
                except:
                    print("\n"+"Something went wrong or the user has interrupted. Saving the collected data so far...")
                    self.save_thread_urls(thread_urls, forum_num, counter)
                    filename = self.save_data(data, forum_num, data_old, True)
                    print("Done")
                    quit()

                # Save the data
                filename = self.save_data(data, forum_num, data_old, True)

            else:
                print("Initializing...")
                # Get web page
                driver.get(forum_url)

                print("Collecting thread URLs...")

                # For manual scraping
                # Execute script to scroll down the page
                # for i in range(10):
                #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                #     time.sleep(2)

                # Scrapes the entire forum
                reached_bottom_of_page = False
                while(not reached_bottom_of_page):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if(len(driver.find_elements_by_xpath("//footer[@class='topic-list-bottom']//div[@class='footer-message ember-view']//h3")) > 0):
                        reached_bottom_of_page = True
                    time.sleep(5.0)

                thread_urls = []
                for element in driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//a[starts-with(@class, 'title raw-link')]"):
                    thread_urls.append(element.get_attribute("href"))

                # Change to the appropriate directory
                self.chdir_forum(forum_num)

                # Start scraping through the forums
                print("Collected the thread URLs, starting to scrape...")

                # This counter variable keeps track of how many threads we have scraped so far
                counter = 0

                # Save the thread URLs so we can continue later if something goes wrong
                self.save_thread_urls(thread_urls, forum_num, counter)
                try:
                    for url in thread_urls:
                        # Scrape the thread
                        ThreadScraper(data, driver, url)
                        # After scraping the thread increment the counter. If we interrupt the program we can continue from where we left off by using this variable
                        counter += 1
                # If something goes wrong or the user interrupts the program, save the csv and the update the thread_urls text file
                except:
                    print("\n"+"Something went wrong or the user has interrupted. Saving the collected data so far...")
                    self.save_thread_urls(thread_urls, forum_num, counter)
                    filename = self.save_data(data, forum_num)
                    print("Done")
                    quit()

                # Save the data
                filename = self.save_data(data, forum_num)

            # Run the analysis on the collected data
            if(analysis == True):
                if(arg1 == False):
                    self.run_analysis(filename, forum_num, driver)
                else:
                    self.run_analysis(filename, forum_num, driver, True)

            # Cleanup the saved folder
            os.chdir('saved')
            if(len(os.listdir()) > 0):
                os.remove(min(os.listdir))
            os.chdir('..')

        def save_data(self, data, forum_num, data_old = None, continue_flag = False):

            print("Saving data...")

            # Check if there is already saved file
            try:
                if(len(os.listdir()) == 3):
                    # There is a saved file, move the saved file to the old direcetory
                    shutil.move(str(min(os.listdir())), 'old')
            except:
                print("The updated file already exist in the old directory, skipping moving files")

            # Conver to pandas dataframe
            df = pd.DataFrame(data, columns=["thread_name", "categories", "replies", "views", "total_likes", "creation_date", "first_reply_date", "last_reply_date", "thread_url", "frequent_posters", "thread_author", "thread_likes", "thread_text", "thread_images", "thread_edits", "latest_thread_edit_date", "reply_author", "reply_likes", "reply_text", "reply_images", "reply_date", "crawl_date"])

            # If there is previous data append it
            if(continue_flag == True):
                df = data_old.append(df)

            # Get the date
            crawl_date = str(datetime.now()).split(" ")[0]
            filename = crawl_date + ".csv"

            # Save to the appropriate directory
            df.to_csv(filename, index=False, encoding='utf-8')

            # Zip the file
            zipfile.ZipFile(crawl_date + ".zip", "w").write(filename)

            # Delete the csv (Some csv's will be massive as they need to be compressed we dont acutally need the csv)
            os.remove(filename)
            return filename

        def chdir_forum(self, forum_num):

            if forum_num == 0:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/welcome/')

            elif forum_num == 1:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')

            elif forum_num == 2:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_tips/')

            elif forum_num == 3:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/your_fiverr_experience/')

            elif forum_num == 4:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_site/')

            elif forum_num == 5:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/events/')

        def run_analysis(self, filename, forum_num, driver, arg1 = False):

            # if(arg1 == False):
            #     # Get the most recent file after the filename
            #     if forum_num == 0:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/welcome/')
            #
            #     elif forum_num == 1:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')
            #
            #     elif forum_num == 2:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_tips/')
            #
            #     elif forum_num == 3:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/your_fiverr_experience/')
            #
            #     elif forum_num == 4:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_site/')
            #
            #     elif forum_num == 5:
            #         os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/events/')

            all_files = os.listdir()
            # remove the censored directory
            uneccessary_dir = max(all_files)
            all_files.remove(uneccessary_dir)
            all_files.remove(filename)

            t1 = pd.read_csv(max(all_files))
            t2 = pd.read_csv(filename)

            CompareThreads(t1, t2, driver)

        def save_thread_urls(self, thread_urls, forum_num, index):

            os.chdir('saved')
            # Create a text file and store the collected thread urls
            try:
                with open("saved_thread_urls.txt", "w") as f:
                    f.write(str(index) + "\n")
                    for url in thread_urls:
                        f.write(str(url) + "\n")
            except:
                print("Something went wrong during backing up thread_urls...")
                inp = input("Would you like continue with the program execution? Note that the programs will not be able continue where its left off if someting goes wrong during the execution![y/n]")
                if inp == "y" or inp == "Y":
                    return
                elif inp =="n" or inp =="N":
                    print("Exiting the program...")
                    quit()
                else:
                    print("Invalid input, exiting the program...")
                    quit()
            os.chdir('..')

#--------------------------------------------------------------------------------------------------------------------------#

url = "https://forum.fiverr.com/"
t1 = datetime.now()

if(len(sys.argv) > 1):
    if(len(sys.argv) > 3 and sys.argv[3] == "continue" and (sys.argv[1] == "1" or sys.argv[1] == "2")):

        if(int(sys.argv[2]) > 6):
            print("Invalid thread option, aborting scraping...")

        else:
            if(sys.argv[1] == "1"):
                driver = webdriver.Chrome()
            else:
                driver = webdriver.Chrome(options = options)
            Spider(driver, url, True, sys.argv[2], True)
            driver.quit()
            print("Done!")

    elif ((sys.argv[1] == "1" or sys.argv[1] == "2") and len(sys.argv) > 2):

        if(int(sys.argv[2]) > 6):
            print("Invalid thread option, aborting scraping...")
        else:
            if(sys.argv[1] == "1"):
                driver = webdriver.Chrome()
            else:
                driver = webdriver.Chrome(options = options)
            Spider(driver, url, True, sys.argv[2])
            driver.quit()
            print("Done!")

    else:
        print("Invalid options, cleaning up...")
else:
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(options = options)
    Spider(driver, url)
    driver.quit()
    print("Done!")

t2 = datetime.now()
delta = t2 - t1
print("Time elapsed: " + str(int(delta.total_seconds()/60)) + " minutes")
