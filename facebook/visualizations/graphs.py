"""
Display graphs of the data
"""

import streamlit as st
import matplotlib.pyplot as plt
from facebook.processing.process_data import process_posts


def display_facebook(start_date, end_date, mode):
    """
        Display Facebook posts data
    """
    posts, top_posts = process_posts(start_date, end_date, mode)
    summary(len(posts))
    with st.beta_expander("Graphs of likes and total interactions"):
        col1, col2 = st.beta_columns(2)
        with col1:
            st.subheader("Total Interactions")
            display_total_interactions_graph(posts)
        with col2:
            st.subheader("Likes")
            display_likes_graph(posts)
    with st.beta_expander("Top posts for this time period"):
        st.markdown("*Note:* _Top posts are ranked by total interactions_")
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
    likes = top_posts.at[position, "statistics.actual.likeCount"]
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


def display_likes_graph(posts):
    line_graph(
        posts["date"], posts["statistics.actual.likeCount"],
        "Likes on MOH Facebook posts",
        "Likes"
    )

def display_total_interactions_graph(posts):
    line_graph(
        posts["date"], posts["total_interactions"],
        "Total interactions on MOH Facebook posts",
        "Total interactions"
    )

def line_graph(x, y, title, ylabel):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(title=title)
    ax.set(ylabel=ylabel)
    st.pyplot(fig)

