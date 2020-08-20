# import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import pandas as pd


class ThreadScraper:

    def __init__(self, data, driver, thread_url):

        # Get the thread page
        driver.get(thread_url)

        # Let the page load
        time.sleep(2)

        # Let everythin load
        time.sleep(1)

        # Scrape the information
        # -----------------------#

        # Thread name
        try:
            thread_name = driver.find_elements_by_xpath("//div[@class='title-wrapper']//a[@class='fancy-title']")[0].text
        except:
            print("Failed to scrape the following URL:" + thread_url)
            return

        # Thread categories
        categories = driver.find_elements_by_xpath("//div[@class='title-wrapper']//div[starts-with(@class, 'topic-category')]")[0].text

        # Frequent posters
        try:
            driver.find_elements_by_xpath("//div[@class='topic-map']//button")[0].click()
        except:
            # No reviews or meta data
            None
        frequent_posters = "N/A"
        try:
            for i in range(len(driver.find_elements_by_xpath("//div[@class='topic-map']//section[@class='topic-map-expanded']//div//a"))):
                if i == 0:
                    frequent_posters = driver.find_elements_by_xpath("//div[@class='topic-map']//section[@class='topic-map-expanded']//div//a")[i].get_attribute("title")
                else:
                    frequent_posters = frequent_posters + ", " + driver.find_elements_by_xpath("//div[@class='topic-map']//section[@class='topic-map-expanded']//div//a")[i].get_attribute("title")
        except:
            frequent_posters = "N/A"

        # Thread creation date
        try:
            creation_date = driver.find_elements_by_xpath("//div[@class='topic-map']//li[@class='created-at']//span")[0].get_attribute("title")
        except:
            creation_date = "N/A"

        # Last reply date
        try:
            last_reply_date = driver.find_elements_by_xpath("//div[@class='topic-map']//li[@class='last-reply']//span")[0].get_attribute("title")
        except:
            last_reply_date = "N/A"

        # Total thread replies
        try:
            replies = driver.find_elements_by_xpath("//div[@class='topic-map']//li[@class='replies']//span")[0].text
        except:
            replies = "0"

        # Total thread views
        try:
            views = driver.find_elements_by_xpath("//div[@class='topic-map']//li[@class='secondary views']//span")[0].text
        except:
            views = "0"

        # Total thread likes
        try:
            total_likes = driver.find_elements_by_xpath("//div[@class='topic-map']//li[@class='secondary likes']//span")[0].text
        except:
            total_likes = "0"

        # Thread author
        thread_author = driver.find_elements_by_xpath("//div[@class='post-stream']/div[1]//div[@class='topic-meta-data']//div[starts-with(@class, 'names')]")[0].text

        # Thread text
        try:
            # for i in range(len(driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//p"))):
            #     if (i == 0):
            #         thread_text = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//p")[i].text
            #     else:
            #         thread_text = thread_text + "\n" + driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//p")[i].text
            thread_text = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//div[@class='cooked']")[0].text
        except:
            thread_text = "N/A"

        # Thread likes
        try:
            thread_likes = driver.find_elements_by_xpath("//div[starts-with(@class, 'topic-body ')]//div[@class='regular contents']//section[starts-with(@class, 'post-menu-area')]//div")[0].text
        except:
            thread_likes = "0"

        # Thread Images
        thread_images = "N/A"
        try:
            for i in range(len(driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//*[@class='lightbox']"))):
                if (i == 0):
                    thread_images = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//*[@class='lightbox']")[i].get_attribute("href")
                else:
                    thread_images = thread_images + "\n" + driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']//div[starts-with(@class, 'topic-post')][1]//div[@class='regular contents']//*[@class='lightbox']")[i].get_attribute("href")
        except:
            thread_images = "N/A"

        # Thread edits
        try:
            thread_edits = driver.find_elements_by_xpath("//div[@class='topic-meta-data']//div[@class='post-info edits']")[0].text
        except:
            thread_edits = "N/A"

        # Latest thread edit date
        if(thread_edits != "N/A"):
            latest_thread_edit_date = driver.find_elements_by_xpath("//div[@class='topic-meta-data']//div[@class='post-info edits']//a")[0].get_attribute("title").split("on ")[1]
        else:
            latest_thread_edit_date = "N/A"

        if replies != "0":
             self.scrape_replies(driver, data, thread_name, categories, creation_date, last_reply_date, replies, views, total_likes, frequent_posters, thread_author, thread_text, thread_likes, thread_images, thread_edits, latest_thread_edit_date, thread_url)
             print("Finished scraping " + thread_name)
        else:
            crawl_date = datetime.now()

            # If frequent posters is included
            data.append((thread_name, categories, replies, views, total_likes, creation_date, last_reply_date, "N/A", thread_url, frequent_posters, thread_author, thread_likes, thread_text, thread_images, thread_edits, latest_thread_edit_date, "N/A", "N/A", "N/A", "N/A", "N/A", crawl_date))

            # If frequent posters is not included (for headless browser)
            # data.append((thread_name, categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date, thread_url, thread_author, thread_likes, thread_text, thread_images, thread_edits, latests_thread_edit_date, reply_author, reply_likes, reply_text, reply_images, reply_date, crawl_date))
            print("Finished scraping " + thread_name)

    def scrape_replies(self, driver, data, thread_name, categories, creation_date, last_reply_date, replies, views, total_likes, frequent_posters, thread_author, thread_text, thread_likes, thread_images, thread_edits, latest_thread_edit_date, thread_url):

        # TODO: Reply Flag and Reply Edits and Latest Reply Edit Date

        # First scroll all the way down to the end so the elements load
        if int(replies) >= 15:
            for i in range(int(int(replies)/15) + 1):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                #Let the replies load
                time.sleep(1)

        # Then scroll all the way up
        ActionChains(driver).move_to_element(driver.find_elements_by_xpath("//div[@class='title-wrapper']//a[@class='fancy-title']")[0]).perform()


        # Store all the replies for easier access when scrolling
        all_replies = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div")

        # Loop over the number of replies
        for i in range(int(replies)):
            # Scroll to the reply, there is a +1 because the first reply is the thread post itself
            ActionChains(driver).move_to_element(all_replies[i+1]).perform()

            # Reply Author
            try:
                reply_author = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[@class='topic-meta-data']//div[starts-with(@class, 'names')]")[0].text
            except:
                reply_author = "N/A"

            # Reply Likes
            try:
                reply_likes = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[starts-with(@class, 'regular')]//div[@class='actions']")[0].text
                if reply_likes == "":
                    reply_likes = "0"
            except:
                reply_likes = "N/A"

            # Reply text and flag
            try:
                # TODO: do something when you see "This post was flagged by the community and is temporarily hidden."
                # reply_flagged = False
                reply_text = driver.find_element_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[starts-with(@class, 'regular')]//div[@class='cooked']").text
            except:
                reply_text = "N/A"

            # Reply Images
            reply_images ="N/A"
            try:
                for j in range(len(driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[starts-with(@class, 'regular')]//div[@class='cooked']//*[@class='lightbox']"))):
                    if (j == 0):
                        reply_images = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[starts-with(@class, 'regular')]//div[@class='cooked']//*[@class='lightbox']")[j].get_attribute("href")
                    else:
                        reply_images = reply_images + "\n" + driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[starts-with(@class, 'regular')]//div[@class='cooked']//*[@class='lightbox']")[j].get_attribute("href")
            except:
                reply_images = "N/A"

            # Reply Dates
            try:
                reply_date = driver.find_elements_by_xpath("//div[@class='posts-wrapper']//div[@class='post-stream']/div" + str([i+2]) + "//div[@class='topic-meta-data']//div[@class='post-infos']//a[@class='post-date']//span")[0].get_attribute("title")
            except:
                reply_date = "N/A"

            if i == 0:
                first_reply_date = reply_date

            crawl_date = datetime.now()

            # If frequent posters is included
            data.append((thread_name, categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date, thread_url, frequent_posters, thread_author, thread_likes, thread_text, thread_images, thread_edits, latest_thread_edit_date, reply_author, reply_likes, reply_text, reply_images, reply_date, crawl_date))

            # If frequent posters is not included (for headless browser)
            # data.append((thread_name, categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date, thread_url, thread_author, thread_likes, thread_text, thread_images, thread_edits, latests_thread_edit_date, reply_author, reply_likes, reply_text, reply_images, reply_date, crawl_date))

        return
