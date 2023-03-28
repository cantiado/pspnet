FROM python:3.10.9

RUN pip install rq

CMD [ "rq", "worker", "--url", "redis://redis:6379"]