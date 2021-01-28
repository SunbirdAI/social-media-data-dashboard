import os
from dotenv import load_dotenv
load_dotenv()


def load_env_vars(mode="MOH"):
    """
    Load environment variables containing keys
    and other information required to access
    the CrowdTangle API.

    The CrowdTangle list id is chosen corresponding
    to the 'mode' passed in by the user.

    Args:
        mode: The CrowdTangle list of pages/groups
        to fetch posts from. Defaults to 'MOH'.
    """
    api_token = os.getenv("CROWDTANGLE_API_TOKEN")
    posts_url = os.getenv("CROWDTANGLE_POSTS_URL")
    list_id = os.getenv(f"CROWDTANGLE_{mode}_LIST_ID")

    return (api_token, list_id, posts_url)


def load_prediction_api_vars():
    """
    Load environment variables containing keys
    required to access the SunBERT text classification API
    """
    return os.getenv("COVID_PREDICTION_API_URL")
