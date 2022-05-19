# PIMS/app.py
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
"""This module contains FastAPI application.

Example:
    >>> from PIMS.app import app
    >>> import uvicorn
    >>> uvicorn.run(app, host='0.0.0.0', port=5000)
"""

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import InvalidRequestError
from PIMS import __version__
from PIMS.datamodels import ResponseModel
from PIMS.database import PersonInfo, get_connection
from typing import List, Dict, Optional

app: FastAPI = FastAPI(title='Person Info Microservice', version=__version__)

origins: List[str] = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session, _ = get_connection()


@app.get('/{id}', response_model=ResponseModel)
async def main(id: int, response: Response) -> Optional[Dict]:
    """The main route of the microservice.
    
    Args:
        id: ID of the requested person.

    Return:
        Response in JSON-format if ID is valid, None otherwise.
    """
    try:
        session.begin()
        person: PersonInfo = session.query(PersonInfo).filter(PersonInfo.id == id)[0]
        data: Dict = {
            'id': person.id,
            'image': person.image,
            'bbox': person.bbox,
            'name': person.name,
            'surname': person.surname
        }
        session.close()
        return data
    except IndexError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
    
    except InvalidRequestError:
        session.close()
        return None
