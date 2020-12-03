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
    posts, top_posts, summary = process_posts()
    st.subheader(summary)
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
        post1.subheader("Highest ranking ")
        post1.write(top_posts.at[0, "message"])
        post2.write(top_posts.at[1, "message"])


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
