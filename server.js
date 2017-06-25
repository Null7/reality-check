const request = require("request");
const express = require('express');
const PythonShell = require('python-shell');
const app = express();
const port = 3000;

app.get("/api/script/:text", (req, res) => {

});

app.get('/api/title/:title', (req, res) => {


  res.send(body);

});

app.listen(port, (err) => {  
  if (err) {
    return console.log('something bad happened', err);
  }

  console.log(`server is listening on ${port}`);
});