# fiverr-scraper
Web crawler for Fiverr forums - data collection for observing censorship.

https://forum.fiverr.com/

Extracts the following data from the forums:
thread_name ,categories, replies, views, total_likes, creation_date, first_reply_date, last_reply_date, review_day, thread_url, frequent_posters, thread_author, thread_likes, thread_text, thread_images, thread_edits, latest_thread_edit_date, reply_author, reply_likes, reply_text, reply_images, reply_date, crawl_date

Required: Geckodriver- make sure it is added to the $PATH

Compile and run the driver.c

<pre>gcc driver.c</pre>

The Fiverr forums have 6 main categories:

<li>1 - Welcome</li>
<li>2 - COVID-19 Discussions</li>
<li>3 - Fiverr Tips</li>
<li>4 - Your Fiverr Experience</li>
<li>5 - Fiverr Site</li>
<li>6 - Events</li>
<br>

The default execution of the program by using driver.c will scrape only the contents of categories 2-5. 

You can alternatively run the program by issuing the following command inside the crawler directory:<pre>python spider.py</pre>
<br>
<p>There are options to scrape specific forum categories by using:</p>
<pre>python spider.py 1 X</pre>
<p>This will enable scraping specific threads only where X is one of the main categories listed above.</p>
<br>
<p> Example: </p>
<pre>python spider.py 1 2</pre> 
<p> This will scrape and analyze only the COVID-19 Discussions forums.</p>
