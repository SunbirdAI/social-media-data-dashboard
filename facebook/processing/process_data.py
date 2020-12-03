from facebook.data.fetch_from_api import get_fb_posts


def process_posts(metric="likes"):
    posts = get_fb_posts(get_from_csv=True) # fetch posts from dummy file for now
    posts.sort_values(by='date', inplace=True)
    posts['date'] = posts['date'].astype('datetime64')
    posts['date'] = posts['date'].dt.strftime('%b %d')
    posts = calculate_total_interactions(posts)
    top_posts = highest_performing_posts(posts)
    summary = generate_summary(posts)
    
    return posts, top_posts, summary

def generate_summary(posts):
    return f"Number of posts: {len(posts)}"

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

def highest_performing_posts(posts):
    top_posts = posts.sort_values(by='total_interactions', ascending=False)
    top_posts.reset_index(drop=True,inplace=True)
    return top_posts.head(2)




