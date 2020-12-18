import pandas as pd

from datetime import datetime, date
from typing import List

from twitter.data_layer.database.models.tweet import Tweet
from twitter.data_layer.database.models.user import User
from twitter.data_layer.database.user_queries import get_users_by_mode
from twitter.data_layer.database.tweet_queries import get_tweets_by_mode_and_date
from twitter.processing.tweet_processing import get_tweet_words, filter_covid_tweets


class AnalysisData:

    def __init__(self, df: pd.DataFrame, covid_df: pd.DataFrame, users: List[User]):
        self.df = df
        self.covid_df = covid_df
        self.users = users


def create_analysis_data(from_date: date, to_date: date, mode='moh') -> AnalysisData:
    """
    Returns the data to be used in the analysis
    :param from_date: minimum date for tweets
    :param to_date: maximum date for tweets
    :param mode: mode for analysis e.g moh, kcca
    :return:
    """
    users = get_users_by_mode(mode)
    tweets = get_tweets_by_mode_and_date(
        mode,
        datetime(from_date.year, from_date.month, from_date.day),
        datetime(to_date.year, to_date.month, to_date.day)
    )
    print(len(tweets))
    df = create_pd_from_tweets(tweets)
    covid_df = filter_covid_tweets(df)
    return AnalysisData(df, covid_df, users)


def process_tweet(tweet: Tweet) -> dict:
    """Process tweets from raw objects"""
    text = tweet.text
    words = get_tweet_words(text)
    retweet_count = tweet.retweet_count
    reply_count = tweet.reply_count
    quote_count = tweet.quote_count
    like_count = tweet.like_count
    engagement = retweet_count + reply_count + quote_count + like_count

    return {
        'username': tweet.user.username,
        'user_id': tweet.author_id,
        'tweet_id': tweet.tweet_id,
        'created_time': tweet.created_time,
        'text': text,
        'words': words,
        'retweet_count': retweet_count,
        'reply_count': reply_count,
        'quote_count': quote_count,
        'like_count': like_count,
        'engagement': engagement
    }


def create_pd_from_tweets(tweets: List[Tweet]) -> pd.DataFrame:
    df = pd.DataFrame([process_tweet(tweet) for tweet in tweets])
    df.set_index('created_time', inplace=True)
    return df
