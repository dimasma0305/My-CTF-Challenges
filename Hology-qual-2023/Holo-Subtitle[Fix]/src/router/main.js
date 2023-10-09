const express = require("express")

var router = express.Router();

router.get('/', (req, res) => {
    const { message } = req.query
    if (!message) {
        return res.render("index", {
            message: "Welcome to Holo Subtitle!"
        })
    }
    return res.render('index', req.query);
});

module.exports = router
