FROM ubuntu

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    pkg-config \
    build-essential \
    cmake \
    curl \
    git \
    python-pip \
    python-setuptools \
    python-dev \
    python-opencv

RUN pip install wheel
RUN pip install numpy
RUN pip install paho-mqtt

# Compile opencv from source
RUN cd /opt && git clone https://github.com/opencv/opencv.git
