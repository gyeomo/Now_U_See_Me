const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({extended: true}));

const controller = require('./image.controller');

router.get('/unknown/:eventTime/:filename', controller.unknown);

module.exports = router