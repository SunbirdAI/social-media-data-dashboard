from typing import List
from datetime import datetime

import streamlit as st
import pandas as pd

import twitter.visualizations.graphs as graphs
from twitter.data_layer.database.models.user import User

from twitter.processing.prepare_data_for_processing import create_analysis_data

from constants import TITLE_TO_MODE


def summary(df: pd.DataFrame, users: List[User]):
    number_of_tweets = len(df.index)
    st.write(f"Number of tweets: {number_of_tweets}")
    # TODO: Maybe use twitter embedding
    accounts_string = "Accounts:\n\n- " + "\n- ".join([user.username for user in users])
    st.write(accounts_string)


def account_comparisons(df: pd.DataFrame, mode: str):
    """
    Renders account comparison graphs
    :param df: the pandas dataframe
    :param mode: determines which accounts are being considered
    """
    comparisons = st.beta_expander("Account comparisons")
    left, right = comparisons.beta_columns(2)

    tweet_dist = graphs.distribution_of_tweets(df, mode)
    eng_cmp = graphs.compare_engagement(df, mode)

    left.write("Distribution of tweets among accounts:")
    left.pyplot(tweet_dist)

    right.write("Engagement on tweets:")
    right.pyplot(eng_cmp)


def covid_analysis(covid_df: pd.DataFrame):
    """
    Renders the covid analysis graphs
    :param covid_df: the pandas dataframe
    """
    cv_analysis_expander = st.beta_expander("Covid Analysis")
    if covid_df is None:
        cv_analysis_expander.write("No covid data for these accounts in this time period")
        return
    left, right = cv_analysis_expander.beta_columns(2)

    covid_tweet_dist = graphs.covid_tweets_by_user(covid_df)
    covid_engagement = graphs.engagement_on_covid_tweets(covid_df)

    left.write("Covid tweet distribution among users")
    left.pyplot(covid_tweet_dist)

    right.write("Engagement on covid tweets")
    right.pyplot(covid_engagement)

    covid_summary = graphs.summarise_covid_tweets(covid_df)
    cv_analysis_expander.write("Frequency of COVID tweets by day")
    cv_analysis_expander.pyplot(covid_summary)


def popular_tweets(df: pd.DataFrame):
    """
    :param df the pandas dataframe
    Displays the top 5 tweets with the highest engagement
    :return:
    """
    # TODO: Display embedded tweets if possible
    pop_tweets = st.beta_expander("Popular Tweets and Likes distribution")
    highest_engagement_tweets = graphs.highest_engagement_tweets(df)

    df_to_display = pd.DataFrame({
        'username': highest_engagement_tweets['username'],
        'text': highest_engagement_tweets['text'],
        'retweets': highest_engagement_tweets['retweet_count'],
        'replies': highest_engagement_tweets['reply_count'],
        'likes': highest_engagement_tweets['like_count'],
        'engagement': highest_engagement_tweets['engagement']
    })

    pop_tweets.write("Highest engagement tweets:")
    pop_tweets.write(df_to_display)


def display_twitter(mode_title: str, from_date: datetime, to_date: datetime):
    """
    Displays the twitter specific UI elements
    :param mode_title: the title of the mode
    :param from_date: starting time for the analysis
    :param to_date: ending time for the analysis
    """
    mode = TITLE_TO_MODE[mode_title]
    analysis_data = create_analysis_data(from_date, to_date, mode)
    if analysis_data.no_data:
        st.write("No data for this time period")
    else:
        summary(analysis_data.df, analysis_data.users)
        account_comparisons(analysis_data.df, mode)
        covid_analysis(analysis_data.covid_df)
        popular_tweets(analysis_data.df)
