"""
    Implement the main dashboard user interface
"""

import streamlit as st
import datetime
from facebook.visualizations.graphs import display_facebook
from twitter.visualizations.render_graphs import display_twitter


FACEBOOK = 'Facebook'
TWITTER = 'Twitter'
MODES = ['Ministry of Health', 'KCCA', 'Influencers', 'Engagers']

st.set_page_config(layout='wide')
st.sidebar.title("SunbirdAI Social Media Data Analysis Dashboard")

platform = st.sidebar.selectbox(
    'Choose a platform', [FACEBOOK, TWITTER])
mode = st.sidebar.selectbox('Choose a mode', MODES)
about = st.sidebar.beta_expander("About Dashboard")
about.write(
    """
    This dashboard presents perspectives from Uganda social media data on COVID-19 measures...
    """
)

st.markdown(f"<h1 style='text-align: center;'>{platform} Analysis for {mode}</h1>",
            unsafe_allow_html=True)
st.write('*Select a time period for the analysis*')
start, end = st.beta_columns(2)
start_date = start.date_input("Start date", datetime.date(2020, 11, 30))
end_date = end.date_input("End date", datetime.date.today())


if platform == FACEBOOK:
    display_facebook(start_date, end_date, mode)
elif platform == TWITTER:
    display_twitter(mode, start_date, end_date)
