var request = require("request");

var testing = 'tôi muốn mua nhà quận bình thạnh giá 20000000';

var options = { method: 'POST',
  url: 'http://localhost:3005/api/v1/real-estate-extraction',
  headers: 
   { 'cache-control': 'no-cache',
     Connection: 'keep-alive',
     //'Content-Length': '58',
     'Accept-Encoding': 'gzip, deflate',
     Host: 'localhost:3005',
     //'Postman-Token': '666173a0-9cd4-4c3f-ab58-ce7cfcf50ad7,e8c65a90-a2b3-41cd-aba8-02db50c517b9',
     'Cache-Control': 'no-cache',
     Accept: '*/*',
     'User-Agent': 'PostmanRuntime/7.20.1',
     'Content-Type': 'application/json' },
  body: [ testing ],
  json: true };

request(options, function (error, response, body) {
  if (error) throw new Error(error);
  console.log(body[0]);
  // resolve(body);
});


// var request = require('request');
// var options = {
//   'method': 'POST',
//   'url': 'localhost:3005/api/v1/real-estate-extraction',
//   'headers': {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify(["quận gò vấp giá 5000000"])
// };
// request(options, function (error, response) { 
//   //if (error) throw new Error(error);
//   console.log(response.body);
// });


