FROM golang:latest

WORKDIR /app

COPY ./src /app

RUN go build -o main

COPY ./init.sh /app
RUN chmod +x init.sh

CMD ["./init.sh"]
