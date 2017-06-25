const request = require("request");
const express = require('express');
const PythonShell = require('python-shell');
const app = express();
const port = 3000;

app.get('/api/python/:title', (req, res) => {
  const options = {
    mode: 'text',
    pythonPath: 'C:/Users/jpdhe/AppData/Local/Programs/Python/Python36-32',
    pythonOptions: ['-u'],
    scriptPath: './pyfiles/titledetection.py',
    args: [req.params.title]
  };

  PythonShell.run("titledetection.py", options, (err, results) => {
    res.send(results);
  });
});

app.listen(port, (err) => {  
  if (err) {
    return console.log('something bad happened', err);
  }

  console.log(`server is listening on ${port}`);
});