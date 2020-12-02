"""
Display graphs of the data
"""

import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
from facebook.processing.process_data import process_posts


def display_facebook():
    """
        Display Facebook posts data
    """
    posts = process_posts()
    st.subheader("Likes")
    display_likes_graph(posts)
    st.subheader("Total Interactions")
    display_total_interactions_graph(posts)

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
    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(x, y)
    ax.set(title=title)
    ax.set(ylabel=ylabel)
    st.pyplot(fig)

