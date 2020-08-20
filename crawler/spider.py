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

options = Options()
#options.headless = True
options.add_argument("--headless")

class Spider:

        def __init__(self, driver, fiverr_url, arg1 = False, arg2 = None):

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
                self.crawl_forum(data, driver, forum_urls[int(arg2) - 1], int(arg2) - 1, True)


        def crawl_forum(self, data, driver, forum_url, forum_num, arg1 = False):

            print("Initializing...")

            # Get web page
            driver.get(forum_url)

            print("Collecting thread URLs...")
            # Execute script to scroll down the page
            for i in range(1):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                time.sleep(2)

            thread_urls = []
            for element in driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//a[starts-with(@class, 'title raw-link')]"):
                thread_urls.append(element.get_attribute("href"))

            print("Collected the thread URLs, starting to scrape...")
            for url in thread_urls:
                ThreadScraper(data, driver, url)

            # Save the data
            filename = self.save_data(data, forum_num)

            # Run the analysis on the collected data
            if(arg1 == False):
                self.run_analysis(filename, forum_num, driver)
            else:
                self.run_analysis(filename, forum_num, driver, True)

        def save_data(self, data, forum_num):

            print("Saving data...")

            # Conver to pandas dataframe
            df = pd.DataFrame(data, columns=["thread_name", "categories", "replies", "views", "total_likes", "creation_date", "first_reply_date", "last_reply_date", "thread_url", "frequent_posters", "thread_author", "thread_likes", "thread_text", "thread_images", "thread_edits", "latest_thread_edit_date", "reply_author", "reply_likes", "reply_text", "reply_images", "reply_date", "crawl_date"])

            # Get the datet1.type(
            crawl_date = str(datetime.now()).split(" ")[0]
            filename = crawl_date + ".csv"

            # Save to the appropriate directory
            if forum_num == 0:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/welcome/')
                df.to_csv(filename, index=False, encoding='utf-8')

            elif forum_num == 1:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')
                df.to_csv(filename, index=False, encoding='utf-8')

            elif forum_num == 2:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_tips/')
                df.to_csv(filename, index=False, encoding='utf-8')

            elif forum_num == 3:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/your_fiverr_experience/')
                df.to_csv(filename, index=False, encoding='utf-8')

            elif forum_num == 4:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/fiverr_site/')
                df.to_csv(filename , index=False, encoding='utf-8')

            elif forum_num == 5:
                os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/events/')
                df.to_csv(filename , index=False, encoding='utf-8')

            return filename

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




url = "https://forum.fiverr.com/"

if(len(sys.argv) > 1):
    if (sys.argv[1] == "1" and len(sys.argv) > 2):
        if(int(sys.argv[2]) > 6):
            print("Invalid thread option, aborting scraping...")
        else:
            #driver = webdriver.Chrome()
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
