FROM oven/bun:latest as base
WORKDIR /app

FROM base as install
COPY ./src/package.json .
RUN bun install

FROM base as release
RUN apt update -y
RUN apt install -y wget

COPY ./flag.txt /flag.txt
RUN mv /flag.txt /flag_`cat /proc/sys/kernel/random/uuid`.txt

WORKDIR /app
COPY --from=install --chown=ctf:ctf /app .

COPY ./src .

EXPOSE 8080
CMD ["bash", "-c", "Hacker_Token=`cat /dev/urandom | head -c 32 | base64` bun run index.tsx"]
