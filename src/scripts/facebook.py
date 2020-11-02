import os
import pandas as pd
import requests
from dotenv import load_dotenv
load_dotenv()

def get_posts():
    """
        Fetches Facebook posts from a given CrowdTangle list
        using the CrowdTangle API
    """
    api_token = os.getenv('CROWDTANGLE_API_TOKEN')
    group_list = os.getenv('GROUP_LIST_ID')
    posts_url = os.getenv('POSTS_URL')

    params = {
        'token': api_token,
        'listIds': group_list,
        'startDate': '2020-10-24',
        'endDate': '2020-10-31',
        'sortBy': 'date',
        'count': 99
    }

    resp = requests.get(posts_url, params=params)
    if resp.status_code != 200:
        print(f'GET /posts/ {resp.status_code}')

    data = resp.json()
    posts_df = pd.json_normalize(data['result']['posts'])
    return posts_df

if __name__=='__main__':
    get_posts()
