# PIMS/datamodels.py
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
"""This module contains the data validation models.

The data validation provided by Pydantic.
"""

from pydantic import BaseModel
from typing import List


class ResponseModel(BaseModel):
    """Response format of the microservice.
    
    Attributes:
        id: ID of the person.
        image: Base64 image of person face.
        bbox: Coordinates of the bounding box, top left and bottom right corners.
        name: The name of the person.
        surname: The surname of the person.
    """
    id: int
    image: str
    bbox: List[int]
    name: str
    surname: str
