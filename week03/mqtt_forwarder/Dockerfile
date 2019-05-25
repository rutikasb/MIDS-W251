FROM alpine:latest

RUN apk update && apk add mosquitto-clients

RUN apk add python \
    python-dev \
    py-pip

RUN pip install paho-mqtt
