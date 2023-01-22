import csv
import os
import datetime
from time import sleep
import random
import threading
from .utils import init_driver, log_search_page, keep_scroling, dowload_images

DATA_DIR = "./outputs/"
CSV_PATH = "./outputs/data.csv"

def scrape(queue, since, until=None, words=None, to_account=None, from_account=None, mention_account=None, interval=5, lang=None,
          headless=True, limit=float("inf"), display_type="Top", proxy=None, hashtag=None, save_images=False, filter_replies=False, proximity=False,
          geocode=None, minreplies=None, minlikes=None, minretweets=None, driver_type="chrome"):
    """
    scrape data from twitter using requests, starting from <since> until <until>. The program make a search between each <since> and <until_local>
    until it reaches the <until> date if it's given, else it stops at the actual date.

    return:
    data : df containing all tweets scraped with the associated features.
    save a csv file containing all tweets scraped with the associated features.
    """

    # ------------------------- Variables :

    # unique tweet ids
    tweet_ids = set()
    # start scraping from <since> until <until>
    # add the <interval> to <since> to get <until_local> for the first refresh
    until_local = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
    # if <until>=None, set it to the actual date
    if until is None:
        until = datetime.date.today().strftime("%Y-%m-%d")
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # initiate the driver
    driver = init_driver(headless, proxy, driver_type)
    # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <until>
    while until_local <= datetime.datetime.strptime(until, '%Y-%m-%d'):
        # number of scrolls
        scroll = 0
        # convert <since> and <until_local> to str
        if type(since) != str :
            since = datetime.datetime.strftime(since, '%Y-%m-%d')
        if type(until_local) != str :
            until_local = datetime.datetime.strftime(until_local, '%Y-%m-%d')
        # log search page between <since> and <until_local>
        path = log_search_page(driver=driver, words=words, since=since,
                        until_local=until_local, to_account=to_account,
                        from_account=from_account, mention_account=mention_account, hashtag=hashtag, lang=lang,
                        display_type=display_type, filter_replies=filter_replies, proximity=proximity,
                        geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
        # number of logged pages (refresh each <interval>)
        refresh += 1
        # number of days crossed
        #days_passed = refresh * interval
        # last position of the page : the purpose for this is to know if we reached the end of the page or not so
        # that we refresh for another <since> and <until_local>
        last_position = driver.execute_script("return window.pageYOffset;")
        # should we keep scrolling ?
        scrolling = True
        print("looking for tweets between " + str(since) + " and " + str(until_local) + " ...")
        # print(" path : {}".format(path))
        # number of tweets parsed
        tweet_parsed = 0
        # sleep
        sleep(random.uniform(0.5, 1.5))
        # start scrolling and get tweets
        driver, queue, tweet_ids, scrolling, tweet_parsed, scroll, last_position = \
            keep_scroling(driver, queue, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position)

        # keep updating <start date> and <end date> for every search
        if type(since) == str:
            since = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
        else:
            since = since + datetime.timedelta(days=interval)
        if type(since) != str:
            until_local = datetime.datetime.strptime(until_local, '%Y-%m-%d') + datetime.timedelta(days=interval)
        else:
            until_local = until_local + datetime.timedelta(days=interval)

    queue.put(None)
    # close the web driver
    driver.close()
