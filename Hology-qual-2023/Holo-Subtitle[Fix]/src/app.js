var express = require('express');
var path = require('path');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));
app.use(require("./midleware/sanitizer"))

const PORT = 8080;

app.use('/', require("./router/main"));

app.listen(PORT, function () {
	console.log('Listening on port ' + PORT);
});
