FROM python:3.7-slim

# DOCKER env var is to indicate the script to fetch credentials from params.json
ENV DOCKER="True"

RUN mkdir /opt/uscis-case-tracker
COPY . /opt/uscis-case-tracker

RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN cd /opt/uscis-case-tracker/lib && pip3 install --user -r requirements.txt

WORKDIR /opt/uscis-case-tracker

ENTRYPOINT ["/usr/local/bin/python", "./tracker.py"]