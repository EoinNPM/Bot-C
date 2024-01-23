FROM python:3.9.6-alpine

ADD . /botc


RUN apk update && \
  apk add python3-dev gcc libc-dev && \
  pip install python-dotenv py-cord

WORKDIR /botc

ENTRYPOINT python /botc/bot.py
