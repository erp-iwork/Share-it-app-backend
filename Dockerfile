FROM python:3.7-slim
LABEL MAINTAINER="Iwork PLC" 
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN apt-get update && apt-get install   -y \
    build-essential\
    python3.7-dev\
    libpq-dev\
    binutils \
    libproj-dev \
    gdal-bin \
    gcc \
    libc-dev \
    libjpeg-dev \
    zlib1g-dev
RUN mkdir /src
WORKDIR /src
COPY ./ /src
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt


