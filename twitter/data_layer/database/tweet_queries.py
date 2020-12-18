from datetime import datetime

from twitter.data_layer.database.models.tweet import Tweet

from twitter.data_layer.database.base import Session, engine, Base

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()


def get_tweets_by_mode_and_date(mode='moh', from_date=datetime(2000, 1, 1), to_date=datetime(2100, 1, 1)):
    return session.query(Tweet) \
        .filter(Tweet.mode == mode) \
        .filter(Tweet.created_time >= from_date) \
        .filter(Tweet.created_time <= to_date) \
        .all()
