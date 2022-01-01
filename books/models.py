import datetime
import enum

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Enum)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class GenderEnum(enum.Enum):
    Male = 'Male'
    Female = 'Female'


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)


class Author(DeclarativeBase):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)


class Book(DeclarativeBase):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(
        Integer,
        ForeignKey("authors.id", name="fk_books_author"),
        nullable=False
    )
    author = relationship("Author", backref="books")
    title = Column(String)
