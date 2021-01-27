"""
Display graphs of the data
"""

import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from facebook.processing.process_data import (
    process_posts,
    highest_performing_posts,
    group_post_metrics_by_date,
    process_covid_predicitions
)


def display_facebook(start_date, end_date, mode):
    """
        Display Facebook posts data
    """
    posts = process_posts(start_date, end_date, mode)
    summary(len(posts))

    with st.beta_expander("Graphs of likes and total interactions per day"):
        st.markdown("""_Total interactions = sum of all reactions
            (like, comment, share, love, wow, haha, care, 
            thankful, sad, angry_)
        """)
        grouped_posts = group_post_metrics_by_date(posts)
        line_graph(grouped_posts)

    with st.beta_expander("Top posts for this time period"):
        metric = st.radio(
            "Choose a metric for displaying top posts:",
            (
                "total interactions", "like",
                "comment", "share", "angry"
            )
        )
        top_posts = highest_performing_posts(posts, metric)
        st.markdown(
            f"""<div style='padding-top: 1rem;'>
                <strong>
                    Showing top posts by the <em>{metric}</em> metric:
                </strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        post1, post2 = st.beta_columns(2)
        with post1:
            display_post(top_posts, metric, "Highest", 0)
        with post2:
            display_post(top_posts, metric, "Second highest", 1)

    with st.beta_expander("Covid posts"):
        display_covid_predictions(posts)


def summary(number_of_posts, accounts = None):
    st.write(f"Number of posts: {number_of_posts}")
    st.write(
        """
        Accounts
        - Ministry of Health Uganda
        """
    )


def display_post(top_posts, metric, subheader, position):
    st.subheader(subheader)

    link = top_posts.at[position, "link"]
    display_link = f"[Link to post]({link})"

    st.markdown(display_link, unsafe_allow_html=True)

    post_type = top_posts.at[position, "type"]
    date = top_posts.at[position, "date"]
    metric_info = top_posts.at[position, metric]

    st.markdown(
        f"""<div style='margin: 1 rem; padding: 1rem;
            border: 1px solid #eee; border-radius: 1%;'>
                <div><strong>{metric.title()} count</strong>: 
                    {metric_info}
                </div>
                <div style='padding-top: 1rem;'>
                    <p>
                        <strong>Post type</strong>: 
                        {post_type.title()}
                    </p>
                    <p><strong>Date</strong>: {date}</p>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    text = top_posts.at[position, "message"]

    st.markdown(
        f"""<div style='margin: 1 rem; padding: 1rem; height: 400px; 
                border: 1px solid #eee; border-radius: 1%;'>
                <div>{text}</div>
            </div>
        """,
        unsafe_allow_html=True
    )


def line_graph(data):
    st.line_chart(
        data,
        height=500,
        use_container_width=True
    )


def display_covid_predictions(posts):
    with st.spinner('Loading predictions for COVID posts...'):
        covid_predictions = process_covid_predicitions(posts)

        pred_plot, pred_table = st.beta_columns(2)
        with pred_plot:
            st.subheader("Plot of COVID vs Non-COVID posts:")
            fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(3, 2))
            sns.set_theme(style="darkgrid")
            ax = sns.countplot(
                x="classification",
                data=covid_predictions
            )
            st.pyplot(fig)
        with pred_table:
            st.subheader("More details:")
            st.dataframe(covid_predictions[[
                "text",
                "classification",
                "confidence"
                ]]
            )








