"""
Fetch posts and related stats from Facebook
through the CrowdTangle API
"""

import pandas as pd
import requests
from constants import FB_TITLE_TO_MODE
from facebook.data.api_utils import load_env_vars


# @st.cache
def get_fb_posts(start_date, end_date, mode,
                 get_from_csv=False, create_csv=False):
    """
        Fetch Facebook posts from a given CrowdTangle list
        using the CrowdTangle API
    """

    if get_from_csv:
        df = pd.read_csv('data/sample_fb_data.csv', index_col=[0])
        return df

    mode = FB_TITLE_TO_MODE[mode]

    api_token, list_id, posts_url = load_env_vars(mode)

    params = {
        'token': api_token,
        'listIds': list_id,
        'startDate': start_date,
        'endDate': end_date,
        'sortBy': 'date',
        'count': 99
    }

    keep_columns = [
        'id', 'platform', 'date', 'type', 'message', 'link',
        'statistics.actual.likeCount', 'statistics.actual.shareCount',
        'statistics.actual.loveCount', 'statistics.actual.wowCount',
        'statistics.actual.hahaCount', 'statistics.actual.sadCount',
        'statistics.actual.angryCount', 'statistics.actual.thankfulCount',
        'statistics.actual.careCount', 'statistics.actual.commentCount'
    ]
    new_columns = [
        'id', 'platform', 'date', 'type', 'message', 'link',
        'like', 'share', 'love', 'wow', 'haha',
        'sad', 'angry', 'thankful', 'care', 'comment'
    ]

    resp = requests.get(posts_url, params=params)
    if resp.status_code != 200:
        print(f'GET /posts/ {resp.status_code}')

    data = resp.json()
    df = pd.json_normalize(data['result']['posts'])
    final_df = df[keep_columns].fillna(0)
    final_df.columns = new_columns

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
        inc_df = df[keep_columns].fillna(0)
        inc_df.columns = new_columns
        final_df = final_df.append(inc_df, ignore_index=True)

    if create_csv:
        final_df.to_csv('data/sample_fb_data.csv')

    return final_df


if __name__ == "__main__":
    start_date = "2020-11-30"
    end_date = "2020-12-5"
    mode = "MOH"
    get_fb_posts(start_date, end_date, mode, create_csv=True)
