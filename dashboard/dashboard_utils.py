import streamlit as st
from scripts import get_fb_posts

def display_facebook():
    fb_posts = get_fb_posts()
    st.header("Facebook posts")
    st.write(fb_posts)
    st.subheader("Total likes")
    st.line_chart(data=fb_posts['statistics.actual.likeCount'])