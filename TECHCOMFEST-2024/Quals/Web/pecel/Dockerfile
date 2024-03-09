FROM php:8.1.0-fpm
COPY ./mikutap /
COPY ./flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt
RUN gcc -o /readflag /readflag.c && rm /readflag.c
RUN chmod +rxs /readflag
