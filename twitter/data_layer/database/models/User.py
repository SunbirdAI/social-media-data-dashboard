from sqlalchemy import Column, String, Integer, DateTime

from twitter.data_layer.database.base import Base


class User(Base):
    __tablename__ = 'users'

    author_id = Column(String, primary_key=True)
    name = Column(String)
    username = Column(String)
    description = Column(String)
    mode = Column(String)
    location = Column(String)
    created_at = Column(DateTime)
    following_count = Column(Integer)
    followers_count = Column(Integer)

    def __init__(self, author_id, name, username, description, mode, location,
                 created_at, following_count, followers_count):
        self.author_id = author_id
        self.name = name
        self.username = username
        self.description = description
        self.location = location
        self.created_at = created_at
        self.following_count = following_count
        self.followers_count = followers_count
        self.mode = mode

    def save_user(self, session):
        session.add(self)
