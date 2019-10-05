const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

app.use('/users', require('./api/users'));
app.use('/event', require('./api/event'));
// app.use('/image/unknown', express.static('../unknown'));
// app.use('/image/unknown/', express.static(path.join(__dirname, '../unknown/2019-9-30-22-4-24-744577')));
app.use('/image', require('./api/image'))

module.exports = app;