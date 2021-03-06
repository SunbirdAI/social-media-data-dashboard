import os

from typing import List
from dotenv import load_dotenv


def load_env_vars() -> dict:
    """
    Get Twitter api URL and bearer token
    :return: a dict with the URL and token
    """
    load_dotenv()
    return {
        "api_root": os.getenv("TWITTER_API_URL"),
        "token": os.getenv("TWITTER_BEARER_TOKEN")
    }


def create_query(users: List[str], include_retweets=False):
    """
    Creates the query string for fetching tweets from a given list of users
    :param users: the list of users
    :param include_retweets: whether to include retweets or not
    :return: the query string
    """
    return " OR ".join(f"from:{user}" for user in users) + (" -is:retweet" if not include_retweets else "")


def create_url_with_query(api_root: str, query: str):
    """
    Combines the root url with the query string
    :param api_root: the root url of the twitter api
    :param query: the query string
    :return: the url to which the request will be made
    """
    tweet_fields = "tweet.fields=id,author_id,text,created_at,public_metrics&expansions=author_id" \
                   "&user.fields=name,username"
    return api_root + f"tweets/search/recent?query={query}&{tweet_fields}"


def create_headers(bearer_token: str):
    """
    Creates the header to be sent along with the request to the api
    :param bearer_token: the authentication token
    :return: dictionary with authentication information
    """
    return {"Authorization": f"Bearer {bearer_token}"}
