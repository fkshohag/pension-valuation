FROM python:3.7.4-alpine

LABEL MAINTAINER="Fazlul Kabir Shohag<shohag.fks@gmail.com>"

# set work directory
WORKDIR /usr/src/pension/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy && \
    pip3 install pandas

COPY requirements.txt /var/www/pension/app/requirements.txt
WORKDIR /var/www/pension/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# copy project
COPY . /var/www/pension/app

