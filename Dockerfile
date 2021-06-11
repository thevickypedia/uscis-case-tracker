FROM python:3.8-slim

ENV DOCKER="True"

RUN mkdir /opt/uscis-case-tracker
COPY . /opt/uscis-case-tracker

RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN cd /opt/uscis-case-tracker/src && pip3 install --user -r requirements.txt

WORKDIR /opt/uscis-case-tracker

ENTRYPOINT ["/usr/local/bin/python", "./src/tracker.py"]