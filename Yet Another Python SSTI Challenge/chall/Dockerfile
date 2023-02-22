FROM python:alpine

WORKDIR /app
COPY src/* .

RUN python3 -m pip install -r requirements.txt
RUN rm /bin -rf

USER 404:404
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=0

CMD [ "flask", "run", "--port=8080", "--host=0.0.0.0"]