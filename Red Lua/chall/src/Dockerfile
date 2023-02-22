FROM python:3.7.16-alpine

WORKDIR /app
COPY . .

RUN rm Dockerfile
RUN adduser  ctf ; echo 'ctf:123' | chpasswd
RUN python3 -m pip install -r requirements.txt

USER ctf:ctf

CMD [ "flask", "run", "--port=8080", "--host=0.0.0.0"]