from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from twitter.data_layer.database.base import Base


class Tweet(Base):
    __tablename__ = 'tweets'

    tweet_id = Column(String, primary_key=True)
    author_id = Column(String, ForeignKey('users.author_id'))
    user = relationship("User", backref='tweets')
    mode = Column(String)
    created_time = Column(DateTime)
    text = Column(String)
    retweet_count = Column(Integer)
    reply_count = Column(Integer)
    quote_count = Column(Integer)
    like_count = Column(Integer)

    def __init__(self, tweet_id, author_id, mode, created_time, text,
                 retweet_count, reply_count, quote_count, like_count):
        self.tweet_id = tweet_id
        self.author_id = author_id
        self.mode = mode
        self.created_time = created_time
        self.text = text
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.quote_count = quote_count
        self.like_count = like_count

    def save_tweet(self, session):
        session.add(self)
