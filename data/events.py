import sqlalchemy
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = "events"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("events_types.id")
    )
    date_start = sqlalchemy.Column(sqlalchemy.DateTime)
    date_end = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.Boolean)
    link = sqlalchemy.Column(sqlalchemy.String)
