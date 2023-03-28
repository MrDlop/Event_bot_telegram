import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    distribution = sqlalchemy.Column(sqlalchemy.Boolean)
    type = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("user_types.id")
    )
