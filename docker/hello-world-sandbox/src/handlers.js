"use strict";


async function status(req, res, next) {
    res.json({
        status: "pass",
    });
    res.end();
    next();
}

async function hello_world(req, res, next) {
    res.json({ message: "Hello World!" });
    res.end();
    next();
}

async function hello_application(req, res, next) {
    res.json({ message: "Hello Application!" });
    res.end();
    next();
}

async function hello_user(req, res, next) {
    res.json({ message: "Hello User!" });
    res.end();
    next();
}


module.exports = {
    status: status,
    hello_world: hello_world,
    hello_application: hello_application,
    hello_user: hello_user
};
