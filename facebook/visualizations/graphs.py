"""
Display graphs of the data
"""

import streamlit as st
import altair as alt
from facebook.processing.process_data import (
    process_posts,
    highest_performing_posts,
    group_post_metrics_by_date
)

def display_facebook(start_date, end_date, mode):
    """
        Display Facebook posts data
    """
    posts = process_posts(start_date, end_date, mode)
    summary(len(posts))

    with st.beta_expander("Graphs of likes and total interactions"):
        grouped_posts = group_post_metrics_by_date(posts)
        line_graph(grouped_posts)

    with st.beta_expander("Top posts for this time period"):
        st.markdown("""*Note:* _Top posts are ranked by total interactions 
                    (sum of likes, comments, shares and all other reactions)_""")
        top_posts = highest_performing_posts(posts)
        post1, post2 = st.beta_columns(2)
        with post1:
            display_post(top_posts, "Top post 1", 0)
        with post2:
            display_post(top_posts, "Top post 2", 1)

def summary(number_of_posts, accounts = None):
    st.write(f"Number of posts: {number_of_posts}")
    st.write(
        """
        Accounts
        - Ministry of Health Uganda
        """
    )

def display_post(top_posts, header, position):
    st.header(header)

    link = top_posts.at[position, "link"]
    display_link = f"[Link to post]({link})"

    st.markdown(display_link, unsafe_allow_html=True)

    total_int = top_posts.at[position, "total_interactions"]
    likes = top_posts.at[position, "like"]
    date = top_posts.at[position, "date"]

    st.markdown(
        f"""<div style='margin: 1 rem; padding: 1rem;
            border: 1px solid #eee; border-radius: 1%;'>
                <div><strong>Total interactions</strong>: {total_int}</div>
                <div><strong>Likes</strong>: {likes}</div>
                <div><strong>Date</strong>: {date}</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    text = top_posts.at[position, "message"]

    st.markdown(
        f"""<div style='margin: 1 rem; padding: 1rem; height: 400px; 
                border: 1px solid #eee; border-radius: 1%;'>
                <div>{text}</div>
            </div>
        """,
        unsafe_allow_html=True
    )

def line_graph(data):
    st.line_chart(
        data,
        height=500,
        use_container_width=True
    )

