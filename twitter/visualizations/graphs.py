import nltk
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Tuple
from wordcloud import WordCloud

from twitter.processing.tweet_processing import covid_non_covid

TITLES = {
    "moh": "MOH Accounts",
    "kcca": "KCCA Accounts",
    "influencers": "Influencers Accounts",
    "moh_engagement": "Engagers Accounts"
}


def summary(df: pd.DataFrame):
    """
    Summarize the data
    """
    print(f"Number of tweets: {df.shape[0]}")
    print(f"Columns:\n{df.info()}")


def barplot(data: pd.DataFrame, xy: Tuple[str, str], ylabel: str, title: str, rotate_x=False):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))

    ax = sns.barplot(x=xy[0], y=xy[1], data=data, ax=axes)
    ax.set(ylabel=ylabel)
    ax.set_title(title)
    if rotate_x:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

    return fig


def distribution_of_tweets(df: pd.DataFrame, mode="moh", is_covid=False):
    """
    Graph representing distribution of users
    """
    usernames = list(df['username'])
    usernames_freq = nltk.FreqDist(usernames)
    usernames_df = pd.DataFrame({
        'Username': list(usernames_freq.keys()),
        'Count': list(usernames_freq.values())
    })
    # popular_users = usernames_df.nlargest(columns='Count', n=13)
    covid = "COVID " if is_covid else ""
    return barplot(data=usernames_df,
                   xy=('Username', 'Count'),
                   ylabel='Count',
                   title=f"Distribution of {covid}tweets among {TITLES[mode]}",
                   rotate_x=True)


def compare_engagement(df: pd.DataFrame, mode="moh"):
    columns_to_show = ["username", "retweet_count", "reply_count", "quote_count", "like_count", "engagement"]

    eng_df = df.groupby(['username'])[columns_to_show]

    aggregate = eng_df.agg([np.mean])
    average_engagement_df = pd.DataFrame({
        "Username": list(eng_df.groups.keys()),
        "Average Engagement": list(aggregate[('engagement', 'mean')])
    })

    return barplot(data=average_engagement_df,
                   xy=('Username', 'Average Engagement'),
                   ylabel='Average Engagement',
                   title=f'Average Engagement of {TITLES[mode]}',
                   rotate_x=True)


def summarise_covid_tweets(covid_df: pd.DataFrame, mode="moh"):
    print(f"Number of COVID tweets: {covid_df.shape[0]}")
    fig, _ = plt.subplots(nrows=1, ncols=1, figsize=(12, 8))
    daily_covid = covid_df['tweet_id'].groupby([covid_df.index.date]).count()
    ax = daily_covid.plot(figsize=(12, 7))
    ax.set(title=f"Frequency of COVID tweets from {TITLES[mode]}")
    ax.set(ylabel="Tweet counts")
    ax.set(xlabel="Date")

    return fig


def distribution_of_covid_tweets(df: pd.DataFrame):
    df['Distribution of COVID Tweets'] = df['words'].apply(covid_non_covid)

    fig, axes = plt.subplots(figsize=(12, 8))
    sns.countplot(x="Distribution of COVID Tweets", data=df)
    return fig


def covid_tweets_by_user(covid_df: pd.DataFrame, mode="moh"):
    return distribution_of_tweets(covid_df, mode, is_covid=True)


def engagement_on_covid_tweets(covid_df: pd.DataFrame, mode="moh"):
    return compare_engagement(covid_df, mode)


def highest_engagement_tweets(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by='engagement', ascending=False).head()


def word_cloud(df: pd.DataFrame):
    tweet_words = list(itertools.chain.from_iterable(df['words']))

    wordcloud = WordCloud(width=800, height=500, random_state=20, max_font_size=110).generate(' '.join(tweet_words))
    fig, _ = plt.subplots(figsize=(15, 10))

    # plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    return fig


def words_alongside_covid(covid_df: pd.DataFrame):
    return word_cloud(covid_df)
