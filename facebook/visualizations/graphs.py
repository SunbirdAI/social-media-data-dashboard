"""
Display graphs of the data
"""

import streamlit as st
import matplotlib.pyplot as plt
from facebook.processing.process_data import process_posts


def display_facebook():
    """
        Display Facebook posts data
    """
    posts, top_posts = process_posts()
    summary(len(posts))
    with st.beta_expander("Graphs of likes and total interactions"):
        col1, col2 = st.beta_columns(2)
        with col1:
            st.subheader("Total Interactions")
            display_total_interactions_graph(posts)
        with col2:
            st.subheader("Likes")
            display_likes_graph(posts)
    with st.beta_expander("Highest perfoming posts"):
        st.subheader("Highest performing posts (ranked by total interactions)")
        post1, post2 = st.beta_columns(2)
        with post1:
            display_post(top_posts, "Highest ranking post", 0)
        with post2:
            display_post(top_posts, "Second highest ranking post", 0)

def summary(number_of_posts, accounts = None):
    st.write(f"Number of posts: {number_of_posts}")
    st.write(
        """
        Accounts
        - Ministry of Health Uganda
        """
    )

def display_post(top_posts, subheader, position):
    st.subheader(subheader)
    st.write(top_posts.at[position, "message"])
    st.write(top_posts.at[position, "link"])

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
