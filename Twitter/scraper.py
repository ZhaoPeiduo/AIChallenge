from Twitter.Scweet_Modified import scweet

'''
columns = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Emojis',
   'Comments', 'Likes', 'Retweets','Image link', 'Tweet URL']
'''


DEFAULT_SETTING = {
    "from_account": None,
    "interval": 1,
    "headless": True,
    "display_type": "top",
    "save_images": False,
    "lang": "en",
    "filter_replies": True,
    "proximity": True,
}


def search_by_words(product_queue, input_dict):
    customised_setting = {
        "queue": product_queue,
        "words": [input_dict["words"]],
        "since": input_dict["since"],
        "until": input_dict["until"],
        "limit": input_dict["limit"]
    }
    customised_setting.update(DEFAULT_SETTING)
    return scweet.scrape(**customised_setting)


def search_by_hashtag(product_queue, input_dict):
    customised_setting = {
        "queue": product_queue,
        "hashtag": input_dict["hashtag"],
        "since": input_dict["since"],
        "until": input_dict["until"],
        "limit": input_dict["limit"]
    }

    customised_setting.update(DEFAULT_SETTING)
    return scweet.scrape(**customised_setting)
