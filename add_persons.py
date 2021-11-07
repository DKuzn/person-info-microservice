# add_persons.py
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
"""This file contains the script to fill the database of a person info.

Note:
    Set the environment variable DATABASE_URL to correct work of this script.

Example:
    >>> python add_persons.py path/to/dataset path/to/metadata.csv
"""

from PIMS.database import PersonInfo, Session, create_table
from facenet_pytorch import MTCNN
from PIL import Image
import pandas as pd
from typing import List, Tuple
import pathlib
import base64
import torch
from tqdm import tqdm
import numpy as np
import argparse
import os


def get_data(mtcnn: MTCNN, image_path: str) -> Tuple[str, List[int]]:
    """Finds the face on given image and encodes image to base64.
    
    Args:
        mtcnn: The instance of MTCNN class.
        image_path: The path to the image.

    Return:
        Base64 string and bounding box of the face.
    """
    image_file: bytes = open(image_path, 'rb').read()
    encoded_string: bytes = base64.b64encode(image_file)
    img: Image.Image = Image.open(image_path).convert('RGB')
    bboxes, _ = mtcnn.detect(img, landmarks=False)
    if bboxes is not None:
        bbox = list(np.int32(np.round(bboxes[0], 0)))
    else:
        raise RuntimeError(f'Any face cannot be found in the file {image_path}')
    return encoded_string.decode('utf-8'), bbox


def fill_database(path_to_dataset: str, path_to_metadata: str) -> None:
    """Fills the database of a person info.
    
    Args:
        path_to_dataset: The path to a dataset root directory.
        path_to_metadata: The path to a metadata CSV file.

    Return:
        None
    """
    mtcnn: MTCNN = MTCNN(
            image_size=160, margin=0, min_face_size=20,
            thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
            device=torch.device('cpu')
        )
    session: Session = Session()
    names: pd.DataFrame = pd.read_csv(path_to_metadata)
    for idx, i in tqdm(enumerate(names['Name']), total=len(names['Name'])):
        long_name: List[str] = i.split('_')
        name: str = ' '.join(long_name[0:-1])
        surname: str = long_name[-1]
        path: str = str(pathlib.Path(f'{path_to_dataset}/{idx + 1}').rglob('*/').__next__())
        data: Tuple[str, List[int]] = get_data(mtcnn, path)
        session.add(PersonInfo(*data, name=name, surname=surname))

    session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to fill the database of a person info.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('path_to_dataset', metavar='path/to/dataset', type=str, 
                        help="""The path to the dataset with a faces images.
Dataset format:
|--root/
    |--1
        |--somename.jpg
    |--2
        |--somename.jpg
    ...................
    |--N
        |--somename.jpg""")
    parser.add_argument('path_to_metadata', metavar='path/to/metadata.csv',
                        help="""The path to CSV file with a person metadata.
The metadata file must contain the column 'Name' in a format:
 - 'Name_Surmane';
 - 'Surname';
 - 'Firstname_Secondname_Surname'.""")

    args = parser.parse_args()

    if not os.path.exists(args.path_to_dataset):
        raise FileNotFoundError('The path to the dataset is incorrect.')
    elif not os.path.exists(args.path_to_metadata):
        raise FileNotFoundError('The path to the metadata file is incorrect.')

    create_table()
    fill_database(args.path_to_dataset, args.path_to_metadata)
