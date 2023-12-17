
module.exports = {
    /**
     *
     * @param {string} url
     * @returns {Function|Object}
     */
    hackerURLParser(url) {
        if (url.startsWith("json:")) {
            return JSON.parse(url.substring(5))
        } else if (url.startsWith("func:")) {
            return Function(url.substring(5))
        } else if (url.startsWith("obj:")) {
            return Object(JSON.parse(url.substring(5)))
        } else if (url.startsWith("data:")) {
            return JSON.parse(url.substring(url.indexOf(",") + 1))
        } else {
            return url
        }
    },
    isSave(arr) {
        return new Promise((resolve) => {
            arr.forEach((val) => {
                if (val.startsWith("-") &&
                    !(
                        val == "--preserve-permissions" ||
                        val == "-O"
                    )) {
                    resolve(false)
                }
            })
            resolve(true)
        })
    }
}
