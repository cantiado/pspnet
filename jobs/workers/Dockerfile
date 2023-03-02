FROM python:3.11.0

RUN pip install rq

CMD [ "rq", "worker", "--url", "redis://redis:6379"]
