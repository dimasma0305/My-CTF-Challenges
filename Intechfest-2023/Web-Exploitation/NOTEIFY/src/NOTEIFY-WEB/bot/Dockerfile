FROM ghcr.io/puppeteer/puppeteer:latest

WORKDIR /app

COPY ./package.json .
RUN npm install

COPY . .

CMD [ "node", "index.js" ]
