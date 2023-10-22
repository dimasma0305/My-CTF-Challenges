const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "https://app",
    APPURLREGEX: process.env['APPURLREGEX'] || "^.*$",
    APPFLAG: process.env['APPFLAG'] || "dev{flag}",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
}

console.table(CONFIG)

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    headless: "new",
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor',
        '--ignore-certificate-errors',
    ],
    ipDataDir: '/home/bot/data/',
    ignoreHTTPSErrors: true,
});

console.log("Bot started...");

module.exports = {
    name: CONFIG.APPNAME,
    urlRegex: CONFIG.APPURLREGEX,
    rateLimit: {
        windowS: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    bot: async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createIncognitoBrowserContext()
        try {
            // Goto main page
            const page = await context.newPage();
            await page.goto(CONFIG.APPURL, { waitUntil: "domcontentloaded" })

            const title = await page.$("input[x-ref=title]")
            const description = await page.$("input[x-ref=description]")
            const button = await page.$("button")
            await title.type(CONFIG.APPFLAG)
            await description.type("This is the flag")
            await button.click()

            // Visit URL from user
            console.log(`bot visiting ${urlToVisit}`)
            let page2 = await context.newPage();
            await page2.goto(urlToVisit);

            await new Promise((v) => setTimeout(v, 10000));

            // Close
            console.log("browser close...")
            await context.close()
            return true;
        } catch (e) {
            console.error(e);
            await context.close();
            return false;
        }
    }
}
