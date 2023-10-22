FROM python:3.11-alpine

RUN pip3 install requests flask flask-session pydash faker gunicorn

WORKDIR /app
COPY ./app .
COPY ./flag.txt /flag.txt

USER 404

CMD [ "sh", "-c", "python3 -m gunicorn --bind 0.0.0.0:8000 -w 8 app:app" ]
