from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy import orm

base = declarative_base()
engine = sa.create_engine('sqlite:///fbtelebot.db', echo=True)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)
