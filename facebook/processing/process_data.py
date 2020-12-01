from facebook.data.fetch_from_api import get_fb_posts


def process_posts(metric="likes"):
    posts = get_fb_posts(get_from_csv=True) # fetch posts from dummy file for now
    posts.sort_values(by='date', inplace=True)
    posts['date'] = posts['date'].astype('datetime64')
    posts['date'] = posts['date'].dt.strftime('%b %d %Y')
    return posts

def calculate_total_interactions(posts):
    posts['total_interactions'] = posts['statistics.actual.likeCount'] 
    + posts['statistics.actual.shareCount']
    + posts['statistics.actual.commentCount']
    + posts['statistics.actual.loveCount']
    + posts['statistics.actual.wowCount']
    + posts['statistics.actual.hahaCount']
    + posts['statistics.actual.sadCount']
    + posts['statistics.actual.angryCount']
    + posts['statistics.actual.thankfulCount']
    + posts['statistics.actual.careCount']

    return posts



