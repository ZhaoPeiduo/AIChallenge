from Twitter.Scweet_Modified import scweet
import queue

DEFAULT_SETTING = {
    "from_account": None,
    "interval": 1,
    "headless": True,
    "display_type": "top",
    "lang": "en",
    "filter_replies": True,
    "proximity": True,
}


def search_by_words(product_queue: queue.Queue, input_dict: dict, driver_type: str = "chrome") -> None:
    customised_setting = {
        "queue": product_queue,
        "words": [input_dict["words"]],
        "since": input_dict["since"],
        "until": input_dict["until"],
        "limit": input_dict["limit"],
        "driver_type": driver_type
    }
    customised_setting.update(DEFAULT_SETTING)
    scweet.scrape(**customised_setting)


def search_by_hashtag(product_queue: queue.Queue, input_dict: dict, driver_type: str = "chrome") -> None:
    customised_setting = {
        "queue": product_queue,
        "hashtag": input_dict["hashtag"],
        "since": input_dict["since"],
        "until": input_dict["until"],
        "limit": input_dict["limit"],
        "driver_type": driver_type
    }

    customised_setting.update(DEFAULT_SETTING)
    scweet.scrape(**customised_setting)
