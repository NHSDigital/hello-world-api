//var ApiMocker = require('apimocker');
var options = {};

var Express = require('express');
Express.createServer(options)
    .setConfigFile('src/config.json')
    .start();
