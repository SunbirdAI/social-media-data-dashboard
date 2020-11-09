import streamlit as st
from dashboard_utils import display_facebook

FACEBOOK = 'Facebook'
TWITTER = 'Twitter'

st.title('Data Analysis Dashboard')

platform = st.sidebar.selectbox(
    'Choose a platform', [FACEBOOK, TWITTER])

if platform == FACEBOOK:
    display_facebook()
