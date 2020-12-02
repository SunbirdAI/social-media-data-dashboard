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
    st.header("Facebook posts")
    st.subheader("Likes")
    display_likes_graph(posts)
    st.subheader("Total Interactions")
    display_total_interactions_graph(posts)

def display_likes_graph(posts):
    fig, ax = plt.subplots()
    ax.plot(posts["date"], posts["statistics.actual.likeCount"])
    ax.set(title="Likes on MOH Facebook posts")
    ax.set(ylabel="Likes")
    st.pyplot(fig)

def display_total_interactions_graph(posts):
    fig, ax = plt.subplots()
    ax.plot(posts["date"], posts["total_interactions"])
    ax.set(title="Total interactions on MOH Facebook posts")
    ax.set(ylabel="Total interactions")
    st.pyplot(fig)
