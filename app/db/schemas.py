from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    register_date = Column(Date, nullable=False)
    birthday = Column(Date)
    sex = Column(String)
    nick_name = Column(String)


class Dictionary(Base):
    __tablename__ = 't_dictionary'

    key = Column(String, primary_key=True, nullable=True)
    value = Column(String)