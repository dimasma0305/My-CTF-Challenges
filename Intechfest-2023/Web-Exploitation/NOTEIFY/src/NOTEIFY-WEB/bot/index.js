const puppeteer = require('puppeteer');
const express = require("express")
const app = express();
const route = express.Router()
const rateLimit = require("express-rate-limit")

app.use(express.urlencoded({ extended: false }))


const ADMIN_USERNAME = process.env['TARGET_USERNAME'] || "admin"
const ADMIN_PASSWORD = process.env['TARGET_PASSWORD'] || "admin"
const APPURL = process.env['APPURL'] || "http://172.17.0.1"

const limit = rateLimit({
    windowMs: 1 * 60 * 1000,
    max: 5
})

console.log("Bot started...");

const bot = async (noteId) => {
    /**
     * @type {puppeteer.Browser|null}
     */
    var browser = null
    try {
        browser = await puppeteer.launch({
            executablePath: "/usr/bin/google-chrome",
            headless: "new",
            args: [
                '--no-sandbox',
            ]
        });
        const urlToVisit = `${APPURL}/note/${noteId}`;
        const context = await browser.createIncognitoBrowserContext()
        const page = await context.newPage();
        console.log(`bot visiting ${APPURL}`)
        await page.goto(APPURL);
        await page.evaluateOnNewDocument((token) => {
            localStorage.setItem("bearerToken", token);
        }, btoa(`${ADMIN_USERNAME}:${ADMIN_PASSWORD}`));
        console.log(`bot visiting ${urlToVisit}`)
        await page.goto(urlToVisit, {
            waitUntil: 'networkidle2'
        });
        await page.waitForTimeout(5000);
        console.log("browser close...")
        await browser.close()
        return true;
    } catch (e) {
        console.log(e);
        await browser.close();
        return false;
    }
}

route.post("/visit", limit, async (req, res) => {
    const { noteId } = req.body;
    console.log("accessing from ip", req.ip)
    if (!noteId) {
        res.send({ "error": "Note ID is missing" });
        return;
    }
    if (!(/^[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}$/i).test(noteId)) {
        res.send({ "error": "Invalid note ID" })
        return
    }
    if (await bot(noteId)) {
        res.send({ "success": "Admin successfully visited the note URL" });
    } else {
        res.send({ "error": "Admin failed to visit the note URL" });
    }
});

route.get("/", (_, res) => {
    res.sendFile("index.html", { root: __dirname });
});

app.use("/report", route)

app.listen(8080, () => {
    console.log("Server running at http://localhost:8080");
});
