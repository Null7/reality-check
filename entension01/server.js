const request = require("request");
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) =>  {
  res.send("it works");
});

app.get('/api/parse/', (req, res) => {
  const url = req.query.url;

  const options = {
    method: 'GET',
    url: 'https://document-parser-api.lateral.io/',
    qs: { "url": url},
    headers: {
      'content-type': 'application/json',
      'subscription-key': '0b8b238af3bae8b43e6b8f27e0b76377'
    }
  };

  request(options, function (error, response, body) {
  if (error) throw new Error(error);

  res.send(body);
  });
});

app.listen(port, (err) => {  
  if (err) {
    return console.log('something bad happened', err);
  }

  console.log(`server is listening on ${port}`);
});