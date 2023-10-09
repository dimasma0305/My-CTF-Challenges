FROM python:alpine

WORKDIR /app

COPY ./server/requirements.txt .
RUN pip install -r requirements.txt

RUN adduser -D ctf
COPY ./server /app
RUN find /app -type d -exec chown ctf:ctf {} +

COPY flag.txt /flag.txt
RUN mv /flag.txt /`python -c "import os; print(os.urandom(16).hex(),end='')"`.txt

USER ctf
EXPOSE 8000
CMD ["./run.sh"]
