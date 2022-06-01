from setuptools import setup
from PIMS import __version__

setup(
    name='PIMS',
    version=__version__,
    packages=['PIMS'],
    url='https://github.com/DKuzn/person-info-microservice',
    license='GPLv3',
    author='Dmitry Kuznetsov',
    author_email='DKuznetsov2000@outlook.com',
    description='Microservice for getting person info during face recognition',
    install_requires=['fastapi', 'SQLAlchemy', 'numpy', 'psycopg2-binary', 'mysqlclient', 'uvicorn']
)