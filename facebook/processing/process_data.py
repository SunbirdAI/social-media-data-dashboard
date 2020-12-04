from facebook.data.fetch_from_api import get_fb_posts


def process_posts(start_date, end_date, mode):
    """
        Call the function that fetches posts from the API
        and do some preliminary processing on them
    """
    # fetch posts from dummy file when testing
    # posts = get_fb_posts(get_from_csv=True) 

    # fetch posts from API
    posts = get_fb_posts(start_date, end_date, mode)

    posts.sort_values(by='date', inplace=True)
    posts['date'] = posts['date'].astype('datetime64')
    posts['date'] = posts['date'].dt.strftime('%b %d')
    posts = calculate_total_interactions(posts)
    top_posts = highest_performing_posts(posts)
    
    return posts, top_posts

def calculate_total_interactions(posts):
    """
        Calculate total interactions on posts by adding
        up all interactions
    """
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

def highest_performing_posts(posts):
    """
        Pick the two posts with the highest 
        total interactions
    """
    top_posts = posts.sort_values(by='total_interactions', ascending=False)
    top_posts.reset_index(drop=True,inplace=True)
    return top_posts.head(2)




