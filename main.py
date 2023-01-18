import os

from Models import sgnlp_pipeline
from Twitter import scraper
import concurrent.futures
import multiprocessing
from itertools import repeat
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import math
import logging


'''
columns = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Emojis',
   'Comments', 'Likes', 'Retweets','Image link', 'Tweet URL']
'''

TEXT_POSITION = 4  # Refer to the column legend above
CPU_COUNT = os.cpu_count()


def producer(product_queue: multiprocessing.Queue, input_dict: Dict) -> None:
    print("producer called!", flush=True)
    scraper.search_by_words(product_queue, input_dict)


def consumer(product_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue, word: str) -> List[List]:
    print("consumer called!", flush=True)
    while True:
        tweet = product_queue.get()
        if tweet is None:
            break
        input_dict = dict()
        input_dict["aspects"] = [word]
        tweet_text = tweet[TEXT_POSITION]

        # Remove link
        if tweet_text.find("https") != -1:
            tweet_text = tweet_text[:tweet_text.find("https")]

        # Remove extra lines:
        if tweet_text.find("\n") != -1:
            tweet_text = tweet_text[:tweet_text.find("\n")]

        # If the keyword is in extra lines or link, continue.
        # Scraper allows a tweet to pass to this stage as long as the tweet contains the word.
        # Change to the exact word for the model to work
        if word not in tweet_text.lower():
            continue
        elif tweet_text.find(word) == -1:
            tweet_text = reformat_input(tweet_text, word)
        input_dict["sentence"] = tweet_text

        try:
            output = sgnlp_pipeline.run_model([input_dict])
            result_queue.put(output)
        except RuntimeError:
            print(f"{tweet_text} cannot be processed")


def reformat_input(original_tweet: str, word: str) -> str:
    index = original_tweet.lower().find(word)
    front = index
    back = index
    while original_tweet[front] != " ":
        front -= 1
    while original_tweet[back] != " ":
        back += 1
    # Shift front pointer to retain the space
    reformat_tweet = original_tweet.replace(original_tweet[front + 1:back], word)
    return reformat_tweet


def split_task(num_of_days:int) ->  List[Tuple]:
    current_time = datetime.now()
    start = current_time - timedelta(days=num_of_days)
    result = []
    if num_of_days < CPU_COUNT:
        end = start + timedelta(days=1)
        for i in range(num_of_days):
            result.append((start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
            start += timedelta(days=1)
            end += timedelta(days=1)
    else:
        split_size = math.ceil(num_of_days / CPU_COUNT)  # Get floor value
        print(f"split size: {split_size}")
        end = start + timedelta(days=split_size)
        for i in range(CPU_COUNT - 1):
            result.append((start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
            start += timedelta(days=split_size)
            end += timedelta(days=split_size)
        # Assign slightly larger workload to the last CPU.
        result.append((start.strftime('%Y-%m-%d'), current_time.strftime('%Y-%m-%d')))

    return result


def generate_input_dictionaries(workload_assignment: List[Tuple], word: str, limit: int) -> List[Dict]:
    dict_list = []
    for start, end in workload_assignment:
        curr_dict = dict()
        curr_dict["words"] = word
        curr_dict["since"] = start
        curr_dict["until"] = end
        curr_dict["limit"] = limit
        dict_list.append(curr_dict)
    return dict_list


def flatten(nested_lst: List[List]) -> List:
    result = []
    for lst in nested_lst:
        result.extend(lst)
    return result


def run(num_of_days: int, word: str, limit: int) -> List:
    workload_assignment = split_task(num_of_days)
    input_dictionaries = generate_input_dictionaries(workload_assignment, word, limit)

    num_worker = len(workload_assignment)
    futures = []
    product_queues = [multiprocessing.Queue() for _ in range(num_worker)]
    result_queues = [multiprocessing.Queue() for _ in range(num_worker)]
    print(product_queues, result_queues)
    print(input_dictionaries)

    #TODO: Debug consumer and parallel parts
    with concurrent.futures.ThreadPoolExecutor(num_worker) as executor:
        executor.map(producer, product_queues, input_dictionaries)
        executor.map(consumer, product_queues, result_queues, repeat(word, num_worker))
        # for i in range(num_worker):
        #     executor.submit(producer, product_queues[i], input_dictionaries[i])
        #     future = executor.submit(consumer, product_queues[i], result_queues[i], word)
        #     futures.append(future)
        # concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_EXCEPTION)
    evaluation_results = flatten([list(x.queue) for x in result_queues])
    # evaluation_results = flatten([x.result() for x in futures])
    return evaluation_results


if __name__ == '__main__':
    # Silent debug info
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    # print(run(1, "covid", 40))
    prod_queue = multiprocessing.Queue()
    res_queue = multiprocessing.Queue()
    producer(prod_queue, {'words': 'covid', 'since': '2023-01-17', 'until': '2023-01-18', 'limit': 40})
    consumer(prod_queue, res_queue, "covid")
    output = []
    while not res_queue.empty():
        print(res_queue.get())
