from Scweet_Modified import scweet
import pandas as pd
from IPython.display import display

DEFAULT_SETTING = {
    "from_account": None,
    "interval": 1,
    "headless": True,
    "display_type": "top",
    "save_images": False,
    "lang": "en",
    "resume": False,
    "filter_replies": False,
    "proximity": True,
}


def search_by_words(words, since, limit):
    customised_setting = {
        "words": words,
        "since": since,
        "limit": limit
    }

    customised_setting.update(DEFAULT_SETTING)
    return scweet.scrape(**customised_setting)


def search_by_hashtag(hashtag, since, limit):
    customised_setting = {
        "hashtag": hashtag,
        "since": since,
        "limit": limit
    }

    customised_setting.update(DEFAULT_SETTING)
    return scweet.scrape(**customised_setting)


if __name__ == '__main__':
    # data = search_by_words(["Covid"], "2022-01-10", 40)
    data = pd.read_csv("./outputs/Covid_2022-01-10_2023-01-15.csv")
    display(data)
