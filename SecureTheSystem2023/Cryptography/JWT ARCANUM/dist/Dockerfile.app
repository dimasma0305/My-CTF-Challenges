FROM php:8.1-fpm

RUN apt-get update && \
    apt-get install -y \
    curl \
    libzip-dev \
    unzip

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /srv/app

COPY ./src/*.lock .
COPY ./src/*.json .

RUN composer install --no-scripts

COPY ./src/ /srv/app/

RUN chown -R www-data:www-data ./storage/

USER www-data
