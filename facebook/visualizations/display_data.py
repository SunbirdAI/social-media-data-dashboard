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
    posts = process_posts()
    st.header("Facebook posts")
    st.write(posts)
    display_likes_graph(posts)

def display_likes_graph(posts):
    st.subheader("Likes")
    fig, ax = plt.subplots()
    ax.plot(posts["date"], posts["statistics.actual.likeCount"])
    ax.set(title="Likes on MOH Facebook posts")
    ax.set(ylabel="Likes")
    st.pyplot(fig)

def display_total_interactions_graph(posts):
    st.subheader("Total interactions")
    st.line_chart(posts)
