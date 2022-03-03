from db_conf import base
import sqlalchemy as sa


class Posts(base):
    """Table needed to save old posts ids to avoid duplication"""

    __tablename__ = 'Posts'
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = sa.Column(sa.String)
