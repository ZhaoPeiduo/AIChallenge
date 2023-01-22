import csv
import os.path
import threading

from Models import sgnlp_pipeline
from Twitter import scraper
from Twitter.Scweet_Modified.scweet import DATA_DIR, CSV_PATH
import concurrent.futures
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import queue
import logging
import time

'''
columns = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Emojis',
   'Comments', 'Likes', 'Retweets','Image link', 'Tweet URL']
'''

TEXT_POSITION = 4  # Refer to the column legend above


class Runner:
    def __init__(self, num_of_days: int, word: str, limit: int):
        self._num_of_days = num_of_days
        self._word = word
        self._limit = limit

    def __call__(self):
        # Silent debug info
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("selenium").setLevel(logging.WARNING)
        return self.run()

    def producer(self, product_queue: queue.Queue, input_dict: Dict) -> None:
        print("producer called!", flush=True)
        scraper.search_by_words(product_queue, input_dict)

    def consumer(self, product_queue: queue.Queue, result_queue: queue.Queue, word: str) -> None:
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
                print(f"{tweet_text} to be modified", flush=True)
                tweet_text = self.reformat_input(tweet_text, word)
                print(f"{tweet_text} after modified", flush=True)
            input_dict["sentence"] = tweet_text

            try:
                result = sgnlp_pipeline.run_model([input_dict])
                tweet[TEXT_POSITION] = tweet_text
                csv_writer_lock = threading.Lock()
                with csv_writer_lock:
                    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(tweet)
                result_queue.put(result)
            except RuntimeError:
                print(f"{tweet_text} cannot be processed")

    def reformat_input(self, original_tweet: str, word: str) -> str:
        index = original_tweet.lower().find(word)
        front = index
        back = index
        while original_tweet[front] != " " and front > -1:
            front -= 1
        while original_tweet[back] != " " and back < len(original_tweet):
            back += 1
        # Shift front pointer to retain the space
        reformat_tweet = original_tweet.replace(original_tweet[front + 1:back], word)
        return reformat_tweet

    def split_task(self, num_of_days: int) -> List[Tuple]:
        current_time = datetime.now()
        start = current_time - timedelta(days=num_of_days)
        end = start + timedelta(days=1)
        result = []

        for i in range(num_of_days):
            result.append((start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
            start += timedelta(days=1)
            end += timedelta(days=1)

        return result

    def generate_input_dictionaries(self, workload_assignment: List[Tuple], word: str, limit: int) -> List[Dict]:
        dict_list = []
        for start, end in workload_assignment:
            curr_dict = dict()
            curr_dict["words"] = word
            curr_dict["since"] = start
            curr_dict["until"] = end
            curr_dict["limit"] = limit
            dict_list.append(curr_dict)
        return dict_list

    def flatten(self, nested_lst: List[List]) -> List:
        result = []
        for lst in nested_lst:
            result.extend(lst)
        return result

    def setup_datafile(self) -> None:
        if os.path.exists(CSV_PATH):
            os.remove(CSV_PATH)
        # header of csv
        header = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Emojis', 'Comments', 'Likes',
                  'Retweets',
                  'Image link', 'Tweet URL']
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    def run(self) -> List:
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        self.setup_datafile()

        workload_assignment = self.split_task(self._num_of_days)
        input_dictionaries = self.generate_input_dictionaries(workload_assignment, self._word, self._limit)

        product_queue = queue.Queue()
        result_queue = queue.Queue()
        print(input_dictionaries)
        # self.producer(product_queue, input_dict=input_dictionaries[0])
        # print(len(product_queue.queue))
        # self.consumer(product_queue, result_queue, self._word)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for input_dictionary in input_dictionaries:
                executor.submit(self.producer, product_queue, input_dictionary)
                future = executor.submit(self.consumer, product_queue, result_queue, self._word)
        evaluation_results = list(result_queue.queue)
        return evaluation_results


# if __name__ == '__main__':
#     start = time.time()
#     # Silent debug info
#     logging.getLogger("urllib3").setLevel(logging.WARNING)
#     logging.getLogger("selenium").setLevel(logging.WARNING)
#     result = self.run(5, "covid", 40)
#     print(result, len(result))
#     end = time.time()
#     print(f"Total time taken for scraping 5 days: {end - start}")
