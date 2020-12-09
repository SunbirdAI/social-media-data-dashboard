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
    
    return posts

def calculate_total_interactions(posts):
    """
        Calculate total interactions on posts by adding
        up all interactions
    """
    cols_to_sum = [
        'like', 'share', 'love', 'wow', 'haha',
        'sad', 'angry', 'thankful', 'care'
    ]

    posts["total_interactions"] = posts[cols_to_sum].agg("sum", axis=1)

    return posts

def highest_performing_posts(posts):
    """
        Pick the two posts with the highest 
        total interactions
    """
    top_posts = posts.sort_values(by='total_interactions', ascending=False)
    top_posts.reset_index(drop=True, inplace=True)
    return top_posts.head(2)

def group_post_metrics_by_date(posts):
    posts_gb_total_int = posts.groupby(by='date', as_index=True).agg(
        {"total_interactions": "sum"}
    )
    posts_gb_likes = posts.groupby(by='date', as_index=True).agg(
        {"like": "sum"}
    )
    posts = posts_gb_total_int.merge(
        posts_gb_likes,
        left_index=True,
        right_index=True
    )

    return posts





