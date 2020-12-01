import streamlit as st
import pandas as pd

import twitter.visualizations.graphs as graphs

from twitter.processing.tweet_processing import get_tweets_from_json_file, create_pd_from_tweets, filter_covid_tweets

TITLE_TO_MODE = {
    'Ministry of Health': 'moh',
    'KCCA': 'kcca',
    'Influencers': 'influencers',
    'Engagers': 'engagers'
}


def summary(df: pd.DataFrame, mode: str):
    number_of_tweets = len(df.index)
    st.write(f"Number of tweets: {number_of_tweets}")
    # TODO: Replace this list of users with a dynamically generated one based on the mode
    st.write(
        """
        Accounts
        - MinofHealthUG
        - JaneRuth_Aceng
        - WHOUganda
        """
    )


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


def display_twitter(mode_title: str):
    """
    Displays the twitter specific UI elements
    :param mode_title: the title of the mode
    """
    # TODO: Move this setup to the processing module
    mode = TITLE_TO_MODE[mode_title]
    tweets = get_tweets_from_json_file(mode)
    df = create_pd_from_tweets(tweets)
    covid_df = filter_covid_tweets(df)

    summary(df, mode)
    account_comparisons(df, mode)
    covid_analysis(covid_df)
