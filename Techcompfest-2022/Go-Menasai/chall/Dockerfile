FROM golang:latest

WORKDIR /

RUN useradd --create-home ctf 
USER ctf:ctf
RUN mkdir /home/ctf/app

WORKDIR /home/ctf/app/
USER root:root

COPY readflag.c .
COPY flag.txt .
RUN mv ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN rm /readflag.c
RUN chmod u+s /readflag
RUN mv ./flag.txt /root/flag.txt

COPY ./src ./src
COPY templates/ templates/
COPY upload/ upload/
RUN cd ./src && go build -o ../app

USER ctf:ctf
ENV GIN_MODE=release
CMD [ "./app" ]