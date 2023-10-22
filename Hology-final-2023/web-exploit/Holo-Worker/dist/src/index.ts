import express from "express";
import https from "https";
import fs from "fs";

const app = express();

// setHTML api only works on secure context, so i add ssl to enable it
const options = {
  key: fs.readFileSync('RootCA.key'),
  cert: fs.readFileSync('RootCA.pem')
};

app.use((_, res, next) => {
    res.setHeader("Content-Security-Policy", "default-src 'self' 'unsafe-eval' https://unpkg.com/alpinejs https://cdn.jsdelivr.net/npm/; img-src https://media.tenor.com/MYDG91HHJ-oAAAAC/vestia-zeta-hololive.gif")
    next();
});

app.use(express.static("./static"));

const server = https.createServer(options, app);
server.listen(443)
