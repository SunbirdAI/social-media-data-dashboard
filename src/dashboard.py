import streamlit as st
from scripts import get_fb_posts

st.title('Data Analysis Dashboard')

if st.checkbox('Facebook'):
    fb_posts = get_fb_posts()
    st.write(fb_posts)
