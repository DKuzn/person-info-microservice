FROM ubuntu:latest

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

ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]