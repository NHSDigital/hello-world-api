var Express = require('express');
var options = {};

Express.createServer(options)
    .setConfigFile('src/config.json')
    .start();
