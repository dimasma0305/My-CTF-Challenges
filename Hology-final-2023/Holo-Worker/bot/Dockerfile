FROM node:20-alpine

ENV LANG="C.UTF-8" PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

RUN apk update
RUN apk add --no-cache zlib-dev udev nss ca-certificates
RUN apk add --no-cache chromium
# RUN apk add --no-cache xorg-server
RUN adduser -h /home/bot -D -u 10086 bot && \
    yarn cache clean && \
    rm -rf /tmp/* /etc/apk/* /var/cache/apk/* /usr/share/man

WORKDIR /home/bot

COPY ./*.json .

RUN npm install

COPY . .

CMD ["node", "/home/bot/index.js"]
