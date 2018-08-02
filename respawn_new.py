# Pulls new data in the last 5 pages or 1 page if there's only 1

print("running new")
import time
import pyodbc
import datetime
import xml.etree.cElementTree as ET
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import respawn_dupcheck
import dateutil.parser
from urllib.request import Request, urlopen
import feedparser
import re

sep = '+'
print("modules ran fine")



# Loop for sites with several pages

def feed_new(feed_grouped):
    sep = '+'
    feed_id = feed_grouped[0]
    feed_name = feed_grouped[1]
    feed_url = feed_grouped[2]
    feed_lastchecked = feed_grouped[3]
    feed_credit = feed_grouped[4]
    feed_articleid = feed_grouped[5].strip()
    feed_pubdate = feed_grouped[6].strip()
    feed_description = feed_grouped[7]
    feed_category = feed_grouped[8]
    feed_creator = feed_grouped[9].strip()
    feed_type = feed_grouped[10]
    feed_title = feed_grouped[11].strip()
    feed_link = feed_grouped[12].strip()
    page_max = feed_grouped[13]
    feed_date_node = feed_grouped[14]

    print("name", feed_url)
    print (feed_pubdate)

    loop_pages = 0
    page_number = 0

# If statement is used to differentiate between sites with several pages and sites with just one.
    print("page max", page_max)
    if int(page_max) > 1:
        while loop_pages <= 5:

            print(loop_pages, "this is loop_pages")
            page_number = page_number + 1
            feed_url_page = feed_url + str(page_number)
            print("currently working on", feed_url)
            doc = feedparser.parse(feed_url_page)
            doc_entries = doc["entries"]

            for item in doc_entries:

                content_title = item["title"]
                content_link = item["link"]
                content_id = item["id"]
                timestamp_date_now = datetime.datetime.now()
                content_published_siteformat_dirty = item[feed_pubdate]
                content_published_siteformat = dateutil.parser.parse(content_published_siteformat_dirty)
                old_format = "%a, %d %b %Y %H:%M:%S %z"
                new_format = '%Y-%m-%d %H:%M:%S'
                datetime_format = '%Y-%m-%d %H:%M:%S'
                content_link = content_link.replace("\n", "").replace("	", "")
                content_published_siteformat = str(content_published_siteformat).split(sep, 1)[0]
                content_published = datetime.datetime.strptime(str(content_published_siteformat), new_format).strftime(new_format)

                try:
                    chunk_description = item["summary"]
                    cleanr = re.compile('<.*?>')
                    chunk_description = re.sub(cleanr, '', chunk_description)
                    try:
                        content_description = chunk_description[9:998]
                    except TypeError:
                        content_description = ''
                except AttributeError:
                    content_description = ''
                print (content_description)


                try:
                    content_creator = item["author"]
                except AttributeError:
                    content_creator = ''


                timestamp_date_now = datetime.datetime.now()
                old_format = "%Y-%m-%d %H:%M:%S.%f"
                new_format = '%Y-%m-%d %H:%M:%S'
                date_now_format = '%Y-%m-%d'
                time_now_change = dateutil.parser.parse(str(timestamp_date_now))
                date_now_formatted = datetime.datetime.strptime(str(time_now_change), old_format).strftime(date_now_format)


# Check for dups against text file

                dup_check = open("dup_check.txt", "r")
                dups = (dup_check.read())
                dup_fatigue = 0

                if content_link in dups:
                    print(content_link, "we have this one", dup_fatigue)
                    dup_fatigue = dup_fatigue + 1
                    break

                if content_link not in dups:
                    print(content_link, "we DON'T have this one")
                    print(content_title)
                    time.sleep(1)
                    content_published = datetime.datetime.strptime(content_published, '%Y-%m-%d %H:%M:%S')
                    timestamp_date_now = datetime.datetime.strptime(str(timestamp_date_now), '%Y-%m-%d %H:%M:%S.%f')

                    print(content_id, content_link, content_published, content_description, content_creator, feed_id,
                          feed_name, feed_url, timestamp_date_now, content_title)
                    
                    cnt_achim.commit()

# Put share link in ACHIM_Shares
                    time.sleep(1)
                    cursor = cnt_achim.cursor()
                    cursor.execute("INSERT INTO ACHIM_SHARES (content_link) values(?)", content_link)
                    cnt_achim.commit()

# Update last checked date in ACHIM FEED
                    time.sleep(1)
                    today = datetime.date.today()
                    date_now = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

                    print("added to achim content, shares, feeds")

            time.sleep(15)
            loop_pages = loop_pages + 1
            print("end. loop_pages is", loop_pages)

    else:
        doc = feedparser.parse(feed_url_page)
        doc_entries = doc["entries"]

        for item in doc_entries:

            content_title = item["title"]
            content_link = item["link"]
            content_id = item["id"]
            timestamp_date_now = datetime.datetime.now()
            content_published_siteformat_dirty = item[feed_pubdate]
            content_published_siteformat = dateutil.parser.parse(content_published_siteformat_dirty)
            old_format = "%a, %d %b %Y %H:%M:%S %z"
            new_format = '%Y-%m-%d %H:%M:%S'
            datetime_format = '%Y-%m-%d %H:%M:%S'
            content_link = content_link.replace("\n", "").replace("	", "")
            content_published_siteformat = str(content_published_siteformat).split(sep, 1)[0]
            content_published = datetime.datetime.strptime(str(content_published_siteformat), new_format).strftime(
                new_format)

            try:
                chunk_description = item["summary"]
                cleanr = re.compile('<.*?>')
                chunk_description = re.sub(cleanr, '', chunk_description)
                try:
                    content_description = chunk_description[9:998]
                except TypeError:
                    content_description = ''
            except AttributeError:
                content_description = ''
            print(content_description)

            try:
                content_creator = item["author"]
            except AttributeError:
                content_creator = ''

            timestamp_date_now = datetime.datetime.now()
            old_format = "%Y-%m-%d %H:%M:%S.%f"
            new_format = '%Y-%m-%d %H:%M:%S'
            date_now_format = '%Y-%m-%d'
            time_now_change = dateutil.parser.parse(str(timestamp_date_now))
            date_now_formatted = datetime.datetime.strptime(str(time_now_change), old_format).strftime(date_now_format)

            # Check for dups against text file

            dup_check = open("dup_check.txt", "r")
            dups = (dup_check.read())
            dup_fatigue = 0

            if content_link in dups:
                print(content_link, "we have this one", dup_fatigue)
                dup_fatigue = dup_fatigue + 1
                break

            if content_link not in dups:
                print(content_link, "we DON'T have this one")
                print(content_title)
                time.sleep(1)
                content_published = datetime.datetime.strptime(content_published, '%Y-%m-%d %H:%M:%S')
                timestamp_date_now = datetime.datetime.strptime(str(timestamp_date_now), '%Y-%m-%d %H:%M:%S.%f')

                print(content_id, content_link, content_published, content_description, content_creator, feed_id,
                      feed_name, feed_url, timestamp_date_now, content_title)

# Put share link in ACHIM_Shares
                time.sleep(1)


# Update last checked date in ACHIM FEED
                time.sleep(1)
                today = datetime.date.today()
                date_now = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

                print("added to achim content, shares, feeds")

        time.sleep(15)
        loop_pages = loop_pages + 1
        print("end. loop_pages is", loop_pages)


