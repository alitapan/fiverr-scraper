# Import Libraries
import sys
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from thread_scraper import ThreadScraper
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

        def __init__(self, data, driver, fiverr_url):
            print("Initializing")
            # Get web page
            driver.get(fiverr_url)

            print("Collecting thread URLs...")
            # Execute script to scroll down the page
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                time.sleep(2)
            thread_urls = []
            for element in driver.find_elements_by_xpath("//table[@class='topic-list ember-view']//tbody//tr//a[starts-with(@class, 'title raw-link')]"):
                thread_urls.append(element.get_attribute("href"))
            print("Collected the thread URLs, starting to scrape...")
            for url in thread_urls:
                ThreadScraper(data, driver, url)

data = []
driver = webdriver.Chrome()
#driver = webdriver.Chrome(options = options)
url = "https://forum.fiverr.com/c/Your-Fiverr-Experience/"

crawl_date = str(datetime.now()).split(" ")[0]
start_time = str(datetime.now()).split(" ")[1]

# Start crawling
Spider(data, driver, url)
driver.quit()

filename = crawl_date + "-" + start_time + ".csv"
# Save to pandas dataframe
df = pd.DataFrame(data, columns=["thread_name", "categories", "replies", "views", "total_likes", "creation_date", "first_reply_date", "last_reply_date", "thread_url", "frequent_posters", "thread_author", "thread_likes", "thread_text", "thread_images", "thread_edits", "latest_thread_edit_date", "reply_author", "reply_likes", "reply_text", "reply_images", "reply_date", "crawl_date"])
df.to_csv(filename , index=False, encoding='utf-8')
print("Done!")
