FROM denoland/deno:1.46.2

RUN apt update && apt install -y gcc

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod +s /readflag
RUN rm /readflag.c

# RUN apt install -y gdb

WORKDIR /app
COPY main.ts deno.json start.sh ./
CMD ["bash", "start.sh"]
