# PIMS/database.py
#
# Copyright (c) 2021 Дмитрий Кузнецов
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""This module contains the classes to work with the database.

Note:
    Set the environment variable DATABASE_URL to correct work of this module.
"""

from sqlalchemy import Column, Integer, Text, PickleType, create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from typing import List
import os

DATABASE_URL: str = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)


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


def create_table() -> None:
    """Creates the table in the database.

    Return:
        None
    """
    Base.metadata.create_all(engine)
    table: str = PersonInfo.__tablename__
    print(table)


if __name__ == '__main__':
    create_table()
