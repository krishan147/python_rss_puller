# Pulls all data

print("running everything")
import time
import pyodbc
import datetime
import xml.etree.cElementTree as ET
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import respawn_dupcheck

print("modules work fine")


# Loop for sites with several pages

def feed_everything(feed_grouped):
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

    loop_pages = 0
    page_number = 0

    if int(page_max) > int(1):

        while int(loop_pages) <= int(page_max):
            print(loop_pages, "this is loop_pages")

            # try:

            page_number = page_number + 1
            feed_url_page = feed_url + str(page_number)
            print(feed_url_page)
            req = urllib.request.Request(feed_url_page, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read()
            parser = etree.XMLParser(recover=True)
            doc = ET.fromstring(html, parser=parser)

            print ("1")

            for item in doc.iter('item'):

                print (item)

                content_title = item.find("title").text
                content_id = item.find("guid").text
                content_link = item.find("link").text
                timestamp_date_now = datetime.datetime.now()
                content_published_siteformat = item.find("pubDate").text

                print (content_published_siteformat)

                old_format = "%a, %d %b %Y %H:%M:%S %z"
                new_format = '%Y-%m-%d %H:%M:%S'
                content_published = datetime.datetime.strptime(content_published_siteformat, old_format).strftime(new_format)
                chunk_description = item.find("description").text
                content_description_truncated = chunk_description[0:998]
                content_description = BeautifulSoup(content_description_truncated, "lxml").text
                content_category = item.find("category")
                content_creator = ""
                content_creator = str(item.find("creator"))
                date_now_formatted = (time.strftime(new_format, timestamp_date_now))

                the = item[999999999]
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
                    time.sleep(1)
                    # print(content_id, content_link, content_published, content_description, content_creator, feed_id, feed_name,feed_url, timestamp_date_now,content_category,content_title)

                    # Put share link in ACHIM_Shares
                    time.sleep(1)


                    # Update last checked date in ACHIM FEED
                    time.sleep(1)

                    print("added to achim content, shares, feeds")

            time.sleep(15)
            loop_pages = loop_pages + 1
            print("end. loop_pages is", loop_pages)

    else:
        while int(loop_pages) <= int(page_max):
            print(loop_pages, "this is loop_pages")

            # try:

            feed_url_page = feed_url
            print(feed_url_page)
            req = urllib.request.Request(feed_url_page, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read()
            parser = etree.XMLParser(recover=True)
            doc = ET.fromstring(html, parser=parser)

            for item in doc.iter('item'):
                content_title = item.find("title").text
                content_id = item.find("guid").text
                content_link = item.find("link").text
                timestamp_date_now = datetime.datetime.now()
                content_published_siteformat = item.find("pubDate").text
                old_format = "%a, %d %b %Y %H:%M:%S %z"
                new_format = '%Y-%m-%d %H:%M:%S'
                content_published = datetime.datetime.strptime(content_published_siteformat, old_format).strftime(new_format)
                chunk_description = item.find("description").text
                content_description_truncated = chunk_description[0:998]
                content_description = BeautifulSoup(content_description_truncated, "lxml").text
                content_category = item.find("category")
                content_creator = ""
                content_creator = str(item.find("creator"))
                date_now_formatted = (time.strftime(new_format, timestamp_date_now))

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
                    time.sleep(1)
                    # print(content_id, content_link, content_published, content_description, content_creator, feed_id, feed_name,feed_url, timestamp_date_now,content_category,content_title)

                    cnt_achim.commit()

                    # Put share link in ACHIM_Shares
                    time.sleep(1)


                    # Update last checked date in ACHIM FEED
                    time.sleep(1)

                    print("added to achim content, shares, feeds")

            time.sleep(15)
            loop_pages = loop_pages + 1
            print("end. loop_pages is", loop_pages)





            #  except Exception as e:
            #      print(str(e))
            #      time.sleep(3)
            #      break




