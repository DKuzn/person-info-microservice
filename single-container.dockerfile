FROM ubuntu:22.04

RUN apt-get update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential
RUN apt install -y pip
WORKDIR /root/
RUN mkdir person-info-microservice
WORKDIR /root/person-info-microservice
COPY PIMS /root/person-info-microservice/PIMS
COPY main.py /root/person-info-microservice
COPY requirements.txt /root/person-info-microservice
RUN pip install -r requirements.txt
RUN pip cache purge
RUN apt-get clean

ENTRYPOINT ["gunicorn", "main:app", "-b 0.0.0.0:80", "-w 4", "-k uvicorn.workers.UvicornWorker", "-t 0"]