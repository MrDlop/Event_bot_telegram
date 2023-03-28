import sqlalchemy
from .db_session import SqlAlchemyBase


class Offer(SqlAlchemyBase):
    __tablename__ = "offers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ref = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    is_event = sqlalchemy.Column(sqlalchemy.Boolean)  # 0 - ref, 1 - event
