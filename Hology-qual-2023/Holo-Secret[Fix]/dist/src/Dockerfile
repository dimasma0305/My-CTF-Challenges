FROM php:fpm-alpine

WORKDIR /app

COPY start.sh .
RUN chmod +x ./start.sh

COPY ./flag.txt .
RUN mv ./flag.txt /flag_`cat /proc/sys/kernel/random/uuid`.txt

EXPOSE 9000

CMD [ "./start.sh" ]
