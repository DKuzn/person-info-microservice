# PIMS/app.py
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
"""This module contains FastAPI application.

Example:
    >>> from PIMS.app import app
    >>> import uvicorn
    >>> uvicorn.run(app, host='0.0.0.0', port=5000)
"""

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from PIMS import __version__
from PIMS.datamodels import ResponseModel
from PIMS.database import PersonInfo, Session
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

session = Session()


@app.get('/{id}', response_model=ResponseModel)
async def main(id: int, response: Response) -> Optional[Dict]:
    """The main route of the microservice.
    
    Args:
        id: ID of the requested person.

    Return:
        Response in JSON-format if ID is valid, None otherwise.
    """
    try:
        person: PersonInfo = session.query(PersonInfo).filter(PersonInfo.id == id)[0]
        data: Dict = {
            'id': person.id,
            'image': person.image,
            'bbox': person.bbox,
            'name': person.name,
            'surname': person.surname
        }
        return data
    except IndexError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return None
