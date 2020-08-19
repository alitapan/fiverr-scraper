# import libraries
import sys
import os
import time
import pandas as pd
import math
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class CompareThreads:

    def __init__(self, a, b, webdriver):

        print("Starting thread analysis...")

        censored = []
        t1 = self.createThreadFlow(a)
        t2 = self.createThreadFlow(b)

        print("Running thread analysis...")
        # compare the data objects stored in the dictionaries while iterating over t2's entries.
        for key_entry in t1:
            # check if this thread exists in t1
            if (t2.get(key_entry) != None):

                thread_flag = False
                # compare the thread_text and reply flow to check if anything is potentially censored
                if t1.get(key_entry).thread_text != t2.get(key_entry).thread_text:
                    thread_flag = True

                # # compare the reply flows for further analysis
                # t1_list = t1.get(key_entry).reply_list
                # t2_list = t2.get(key_entry).reply_list

                # # check the replies to this thread if anything has been removed
                # non_equal_indices = []
                # for i in range(len(t1_list)):
                #     if PostObject.equals(t2_list[i], t1_list[i]) == 0:
                #         # The post may been deleted/censcored/changed get the index
                #         non_equal_indices.append(i)

                # # Get a detailed report of changed posts for further investigation
                # # if(len(non_equal_indices) > 0 or thread_flag):
                # if(len(non_equal_indices) > 0):
                #     # replies dont match or the thread text has been changed
                #     # report(t1.get(key_entry), t2.get(key_entry), non_equal_indices, thread_flag)
                #     self.report(t1.get(key_entry), t2.get(key_entry), non_equal_indices)
            else:
                # thread does not exist in t2
                # check to see if the thread is deleted
                self.check_thread(t1.get(key_entry), webdriver, censored)

        # # ----------------------------------------------------------------------------------------------------#
        # # TEST
        # a = PostObject(0, 0, 0, 0, 0, 0)
        # o = []
        # for i in range(4):
        #     o.append(a)
        #
        # b = DataObject(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, o)
        # censored.append(b)
        # # ----------------------------------------------------------------------------------------------------#

        if len(censored) > 0:
            self.store_censored(censored)
            print("Found potentially censored thread(s)")
        else:
            print("No censorship found")

    def report(self, thread_1, thread_2, non_equal_indices, thread_flag = False):
        # Check if thread flag is up, this will determine if we need to investigate further
        if thread_flag == True:
            print("reported thread")
        else:
            print("reported non-thread")

    def check_thread(self, thread_1, driver, censored):
        # t2 does not exist in t1 check if it has been deleted by accessing the url of the page

        # Get the thread page
        driver.get(thread_1.thread_url)

        # Let the page load
        time.sleep(3)

        # Let everythin load
        time.sleep(1)

        # if the url is NOT accessible then the thread has been deleted and needs to be reported!!
        if(not(len(driver.find_elements_by_xpath("//div[@class='title-wrapper']//a[@class='fancy-title']")) > 0)):
            # The page is deleted save to the deleted list
            censored.append(thread_1)
            thread_id = ''
            for c in thread_1.thread_url[::-1]:
                if(c == '/'):
                    thread_id = thread_id[::-1]
                    break
                else:
                    thread_id = thread_id + c
            print("Found potentially censored thread - thread id = " + thread_id)

    def createThreadFlow(self, t):
        scrape_dict = {}

        # iterate rows through the data frame
        i = 0
        for row in t.iterrows():
            # special case for i = 0
            if i == 0:
                # set current object
                current_row = row

                # initialize list
                reply_list = []

                # create PostObject
                p = PostObject(current_row[1]["reply_author"], current_row[1]["reply_likes"], current_row[1]["reply_date"], current_row[1]["reply_text"], current_row[1]["reply_images"], current_row[1]["crawl_date"])

                # append the list
                reply_list.append(p)

                # increment counter
                i = i + 1

            elif i == t.shape[0]:
                # create new DataObject and store the DataObject in the dictionary
                d = DataObject(current_row[1]["thread_name"], current_row[1]["categories"], current_row[1]["replies"],
                               current_row[1]["views"], current_row[1]["total_likes"], current_row[1]["creation_date"],
                               current_row[1]["first_reply_date"], current_row[1]["last_reply_date"], current_row[1]["thread_url"],
                               current_row[1]["frequent_posters"], current_row[1]["thread_author"], current_row[1]["thread_likes"],
                               current_row[1]["thread_text"], current_row[1]["thread_images"], current_row[1]["thread_edits"],
                               current_row[1]["latest_thread_edit_date"], reply_list)

                scrape_dict[current_row[1]["thread_name"] + "_" + current_row[1]["creation_date"]] = d

            else:
                # if current thread_name and creation_date are same as the next one
                if current_row[1]["thread_name"] == row[1]["thread_name"] and current_row[1]["creation_date"] == row[1]["creation_date"]:

                    # reset current_row
                    current_row = row

                    # create PostObject
                    p = PostObject(current_row[1]["reply_author"], current_row[1]["reply_likes"], current_row[1]["reply_date"], current_row[1]["reply_text"], current_row[1]["reply_images"], current_row[1]["crawl_date"])
                    # add the post object to the list
                    reply_list.append(p)

                    # increment counter
                    i = i + 1

                else:
                    # create new DataObject and store the DataObject in the dictionary
                    d = DataObject(current_row[1]["thread_name"], current_row[1]["categories"], current_row[1]["replies"],
                                   current_row[1]["views"], current_row[1]["total_likes"], current_row[1]["creation_date"],
                                   current_row[1]["first_reply_date"], current_row[1]["last_reply_date"], current_row[1]["thread_url"],
                                   current_row[1]["frequent_posters"], current_row[1]["thread_author"], current_row[1]["thread_likes"],
                                   current_row[1]["thread_text"], current_row[1]["thread_images"], current_row[1]["thread_edits"],
                                   current_row[1]["latest_thread_edit_date"], reply_list)

                    scrape_dict[str(current_row[1]["thread_name"]) + "_" + str(current_row[1]["creation_date"])] = d

                    # set new current object
                    current_row = row

                    # re-initialize list
                    reply_list = []

                    # create PostObject
                    p = PostObject(current_row[1]["reply_author"], current_row[1]["reply_likes"], current_row[1]["reply_date"], current_row[1]["reply_text"], current_row[1]["reply_images"], current_row[1]["crawl_date"])

                    # add the post object to the list
                    reply_list.append(p)

                    # increment counter
                    i = i + 1

        return scrape_dict

    def store_censored(self, censored):

        data = []

        for dataObject in censored:
            thread_name = dataObject.thread_name
            categories = dataObject.categories
            replies = dataObject.replies
            views = dataObject.views
            total_likes = dataObject.total_likes
            creation_date = dataObject.creation_date
            first_reply_date = dataObject.first_reply_date
            last_reply_date = dataObject.last_reply_date
            thread_url = dataObject.thread_url
            frequent_posters = dataObject.frequent_posters
            thread_author = dataObject.thread_author
            thread_likes = dataObject.thread_likes
            thread_text = dataObject.thread_text
            thread_images = dataObject.thread_images
            thread_edits = dataObject.thread_edits
            latest_thread_edit_date = dataObject.latest_thread_edit_date

            for postObject in dataObject.reply_list:
                data.append((thread_name, categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date, thread_url, frequent_posters, thread_author, thread_likes, thread_text, thread_images, thread_edits, latest_thread_edit_date, postObject.author, postObject.likes, postObject.text, postObject.images, postObject.date, postObject.crawl_date))

            # Convert to pandas dataframe
            df = pd.DataFrame(data, columns=["thread_name", "categories", "replies", "views", "total_likes", "creation_date", "first_reply_date", "last_reply_date", "thread_url", "frequent_posters", "thread_author", "thread_likes", "thread_text", "thread_images", "thread_edits", "latest_thread_edit_date", "reply_author", "reply_likes", "reply_text", "reply_images", "reply_date", "crawl_date"])

            # Save in the censored directory
            filename = str(datetime.now()).split(" ")[0] + ".csv"
            df.to_csv("censored/" + filename, index=False, encoding='utf-8')

class DataObject:

    def __init__(self, thread_name, categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date,
                thread_url, frequent_posters, thread_author, thread_likes, thread_text, thread_images, thread_edits,
                latest_thread_edit_date, reply_list):

        self.thread_name = thread_name
        self.categories = categories
        self.replies = replies
        self.views = views
        self.total_likes = total_likes
        self.creation_date = creation_date
        self.first_reply_date = first_reply_date
        self.last_reply_date = last_reply_date
        self.thread_url = thread_url
        self.frequent_posters = frequent_posters
        self.thread_author = thread_author
        self.thread_likes = thread_likes
        self.thread_text = thread_text
        self.thread_images = thread_images
        self.thread_edits = thread_edits
        self.latest_thread_edit_date = latest_thread_edit_date
        self.reply_list = reply_list


class PostObject:

    def __init__(self, author, likes, date, text, images, crawl_date):

        self.author = author
        self.likes = likes
        self.date = date
        #self.edits = edits
        self.text = text
        self.images = images
        #self.latest_edit_date = latest_edit_date
        self.crawl_date = crawl_date

    @staticmethod
    def equals(p1, p2):
        print(p1.author)
        print(p2.author)
        print(p1.date)
        print(p2.date)
        if (p1.author == p2.author and p1.date == p2.date) or (math.isnan(p1.author) and math.isnan(p1.date) and math.isnan(p2.author) and math.isnan(p2.date)):
            return 1
        else:
            return 0
