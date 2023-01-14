import Scweet.scweet

if __name__ == '__main__':
    data = Scweet.scweet.scrape(words=['bitcoin'], since="2021-10-01", until="2021-10-05", from_account=None, interval=1,
                  limit=20,headless=True, display_type="Top", save_images=False, lang="en",
                  resume=False, filter_replies=False, proximity=False, geocode="38.3452,-0.481006,200km")
    print(data.head())