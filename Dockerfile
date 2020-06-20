FROM python:3
LABEL MAINTAINER="Iwork PLC" 
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin


RUN mkdir /src
WORKDIR /src
COPY ./ /src
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# RUN adduser -D user
# USER user

