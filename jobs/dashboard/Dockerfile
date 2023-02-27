FROM python:3.11

RUN pip install rq-dashboard

ENTRYPOINT [ "/bin/bash", "-c", "rq-dashboard -H redis" ]