import sqlalchemy
from .db_session import SqlAlchemyBase


class EventTypes(SqlAlchemyBase):
    __tablename__ = "events_types"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
