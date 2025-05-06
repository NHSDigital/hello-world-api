const express = require('express');
const cors = require('cors');

const app = express();
app.disable("x-powered-by");

const corsOptions = {
    origin: 'https://digital.nhs.uk',
    allowedHeaders: [
      'origin',
      'x-requested-with',
      'accept',
      'content-type',
      'Authorization',
      'apikey'
    ],
    maxAge: 3628800,
    methods: ['GET', 'PUT', 'POST', 'DELETE']
  };
  

app.use(cors(corsOptions));

const PORT = process.env.PORT || 9000;


app.get('/hello/world', (req, res) => {
    res.status(200).json({ "message": "Hello World!" });
});

app.get('/hello/application', (req, res) => {
    res.status(200).json({ "message": "Hello Application!" });
});

app.get('/hello/user', (req, res) => {
    res.status(200).json({ "message": "Hello User!" });
});

app.get('/_status', (req, res) => {
    res.status(200).json({ "status": "pass" });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
