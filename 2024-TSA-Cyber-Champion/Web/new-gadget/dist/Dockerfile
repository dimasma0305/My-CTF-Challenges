FROM oven/bun:latest

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    app

WORKDIR /opt/app
RUN mkdir -p /opt/app

COPY app/ /opt/app/
RUN bun install
RUN chown -R 1001:1001 /opt/app && chmod -R 755 /opt/app

COPY ./flag.txt /flag.txt

USER 1001
EXPOSE 8000
ENTRYPOINT ["bun", "run", "start"]
