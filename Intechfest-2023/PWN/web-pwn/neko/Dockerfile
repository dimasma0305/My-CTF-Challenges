FROM ubuntu AS app

RUN apt-get update && apt-get install -y gcc make

WORKDIR /app

COPY ./http.c ./http.h ./main.c ./Makefile ./
COPY ./public/ ./public/

RUN make

RUN rm *.o *.c *.h Makefile

COPY ./flag.txt .
RUN mv ./flag.txt /$(cat /proc/sys/kernel/random/uuid).txt

RUN useradd -m app
USER app

CMD ["./neko", "80"]
