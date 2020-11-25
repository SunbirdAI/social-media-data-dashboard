"""
    Implement the main dashboard user interface
"""

import streamlit as st
from facebook.visualizations.graphs import display_facebook

FACEBOOK = 'Facebook'
TWITTER = 'Twitter'

st.title('Data Analysis Dashboard')

platform = st.sidebar.selectbox(
    'Choose a platform', [FACEBOOK, TWITTER])

if platform == FACEBOOK:
    display_facebook()
