# PIMS/database.py
#
# Copyright (C) 2021-2022  Дмитрий Кузнецов
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""This module contains classes and functions to work with the database.

Note:
    Set the environment variable DATABASE_URL to correct work of this module.

Example:
    >>> from PIMS.database import get_connection, PersonInfo
    >>> session, _ = get_connection()
    >>> for person in session.query(PersonInfo)
    ...     print(person)
"""

from sqlalchemy import Column, Integer, Text, PickleType, create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import List, Tuple
import os


def get_connection(database_url: str = '') -> Tuple[Session, Engine]:
    """Gets session and engine to connect to database.

    Args:
        database_url: Database connection string.

    Return:
        Session and Engine classes instances.
    """
    try:
        DATABASE_URL: str = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')
    except KeyError:
        DATABASE_URL: str = database_url

    engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    session: Session = sessionmaker(bind=engine)
    return session(), engine


Base: DeclarativeMeta = declarative_base()


class PersonInfo(Base):
    """The class to work with the table 'person_info'.
    
    Args:
        image: Base64 image of person face.
        bbox: Coordinates of the bounding box, top left and bottom right corners.
        name: The name of the person.
        surname: The surname of the person.

    Attributes:
        id: ID of the person (sets automatically).
        image: Base64 image of person face.
        bbox: Coordinates of the bounding box, top left and bottom right corners.
        name: The name of the person.
        surname: The surname of the person.
    """
    __tablename__ = 'person_info'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    image: str = Column(Text)
    bbox: List[int] = Column(PickleType)
    name: str = Column(Text)
    surname: str = Column(Text)

    def __init__(self, image: str, bbox: List[int], name: str, surname: str) -> None:
        self.image = image
        self.bbox = bbox
        self.name = name
        self.surname = surname

    def __repr__(self) -> str:
        return f'<PersonInfo({self.id}, {self.name}, {self.surname})>'


def create_table(database_url:str = '') -> None:
    """Creates the table in the database.

    Args:
        database_url: Database connection string.

    Return:
        None
    """
    _, engine = get_connection(database_url)
    Base.metadata.create_all(engine)
    table: str = PersonInfo.__tablename__
    print(table)


if __name__ == '__main__':
    create_table()
