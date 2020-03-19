FROM tensorflow/tensorflow:latest-py3
MAINTAINER Dang pham

# Utilities

RUN mkdir /source

ADD requirements.txt /source
RUN pip install -r /source/requirements.txt

# Copy sources
ADD ./ /source
RUN mkdir -m 777 -p /source

WORKDIR /source

# Change permission
RUN chmod 777 ./scripts/run_service.sh
