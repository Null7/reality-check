var extractor = require('article-extractor');
 
extractor.extractData('http://www.cnn.com/2017/06/24/politics/trump-pentagon-shift-war-power-military/index.html', function (err, data) {
  console.log(data);
});