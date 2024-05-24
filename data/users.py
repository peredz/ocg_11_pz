import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin):

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           nullable=False, primary_key=True)
    reg_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)


class City(SqlAlchemyBase, SerializerMixin):

    __tablename__ = 'cities'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    county = sqlalchemy.Column(sqlalchemy.String, unique=False)
    region = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    street_with_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    house = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Subscribe(SqlAlchemyBase, SerializerMixin):

    __tablename__ = 'subscribe'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ct_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time_gr = sqlalchemy.Column(sqlalchemy.Integer)
