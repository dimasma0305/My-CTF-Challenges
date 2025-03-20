FROM php:7.4-apache

RUN apt update && apt install -y gcc

COPY ./flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod +s /readflag
RUN rm /readflag.c

RUN a2enmod rewrite
COPY ./conf/default.conf /etc/apache2/sites-available/000-default.conf

COPY ./src/ /var/www/html/
