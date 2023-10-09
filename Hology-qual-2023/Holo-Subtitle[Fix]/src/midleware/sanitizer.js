const sanitize = (obj) => {
    const blackListKey = ["view options", "outputFunctionName", "escapeFunction", "localsName", "destructuredLocals", "settings", "escape", "escapeFunction", "escapeXML", "client", "debug"]
    const blackListKeyregex = []
    for (var list of blackListKey) {
        blackListKeyregex.push(RegExp(list, 'ig'))
    }
    for (var key in obj) {
        if (typeof objdata == "object") {
            obj[key] = sanitize(obj[key])
        } else {
            for (var regex of blackListKeyregex) {
                if (regex.test(key)) {
                    delete obj[key]
                }
            }
        }
    }
    return obj
}

/**
 *
 * @param {import("express").Request} req
 * @param {import("express").Response} res
 * @param {import("express").NextFunction} next
 */
function sanitizer(req, _, next) {
    req.query = sanitize(req.query)
    req.body = sanitize(req.body)
    req.params = sanitize(req.params)
    next()
}

module.exports = sanitizer
