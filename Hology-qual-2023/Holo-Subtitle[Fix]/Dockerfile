FROM oven/bun:alpine
RUN addgroup -S ctf
RUN adduser -S ctf -G ctf app
WORKDIR /opt/app
RUN mkdir -p /opt/app

COPY src/ /opt/app/
COPY ./flag.txt .
RUN mv ./flag.txt /flag_`cat /proc/sys/kernel/random/uuid`.txt

USER ctf
EXPOSE 8000
ENTRYPOINT ["bun", "app.js"]
