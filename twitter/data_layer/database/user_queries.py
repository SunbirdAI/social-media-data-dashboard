from twitter.data_layer.database.models.user import User

from twitter.data_layer.database.base import Session, engine, Base


# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()


def get_users_by_mode(mode='moh'):
    users = session.query(User).filter(User.mode == mode).all()
    return users
