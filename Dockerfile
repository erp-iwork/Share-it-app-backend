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
<<<<<<< HEAD
    gdal-bin\
    gcc
   
=======
    gdal-bin \
    gcc \
    libc-dev \
    libjpeg-dev \
    zlib1g-dev




>>>>>>> f879c5d8a83e90ccdd18763c909845ac7add9d08
RUN mkdir /src
WORKDIR /src
COPY ./ /src
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

