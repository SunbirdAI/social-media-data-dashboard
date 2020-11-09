"""
Fetch posts and related stats from Facebook
through the CrowdTangle API
"""

import os
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

@st.cache
def get_fb_posts():
    """
        Fetch Facebook posts from a given CrowdTangle list
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
    df = pd.json_normalize(data['result']['posts'])
    final_df = df

    # pagination
    while 'nextPage' in data['result']['pagination']:
        next_page = data['result']['pagination']['nextPage']
        print(f'Loading page ... {next_page}')
        resp = requests.get(next_page)
        if resp.status_code != 200:
            print('GET /posts/ {}'.format(resp.status_code))
            break
        data = resp.json()
        df = pd.json_normalize(data['result']['posts'])
        inc_df = df
        final_df = final_df.append(inc_df, ignore_index=True)
        next_page = data['result']['pagination']['nextPage']

    return final_df

if __name__=='__main__':
    get_fb_posts()
