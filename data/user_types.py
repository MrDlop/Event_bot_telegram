import sqlalchemy
from .db_session import SqlAlchemyBase


class UserTypes(SqlAlchemyBase):
    __tablename__ = "user_types"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
