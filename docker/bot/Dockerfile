FROM python:3.10


RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . /usr/src/app/
COPY ./requirements.txt .

RUN pip install -r requirements.txt
