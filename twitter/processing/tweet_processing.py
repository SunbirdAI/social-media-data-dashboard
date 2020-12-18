import json
import re
import pandas as pd

from typing import List
from nltk.tokenize import word_tokenize

from constants import DATA_FOLDER, STOP_WORDS

COVID_WORDS = ["covid", "covid19", "corona", "coronavirus", "mask", "masks", "lockdown",
               "staysafe", "virus", "cov", "stayhome", "staysafeug", "socialdistance",
               "washyourhands", "wearamask", "cases", "covid-19"]


def get_tweets_from_json_file(mode: str) -> List[dict]:
    # TODO: Probably move this to the twitter/data module
    data_file = DATA_FOLDER.joinpath(f"{mode}_analysis_tweets.json")
    with open(data_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data['tweets']


def get_tweet_words(tweet_text: str) -> List[str]:
    """Clean up tweet"""
    tweet = tweet_text.lower()
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
    tweet = re.sub(r'@[^\s]+', 'AT_USER', tweet)  # remove usernames
    tweet = re.sub(r'#([\w]+)', '', tweet)  # remove the # in #hashtag
    tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)

    return [word for word in tweet if word not in STOP_WORDS and len(word) > 3]


def is_covid_related_tweet(tweet_words: List[str]) -> bool:
    for word in COVID_WORDS:
        if word in tweet_words:
            return True
    return False


def covid_non_covid(words: List[str]) -> str:
    return "COVID Tweets" if is_covid_related_tweet(words) else "NON-COVID Tweets"


def filter_covid_tweets(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: Figure out why a call to this function doesn't work in the notebook
    return df[df['words'].apply(lambda t_words: is_covid_related_tweet(t_words))]
