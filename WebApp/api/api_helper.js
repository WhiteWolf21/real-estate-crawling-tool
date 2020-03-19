const request = require('request')

module.exports = {
    /*
    ** This method returns a promise
    ** which gets resolved or rejected based
    ** on the result from the API
    */
    make_API_call : function(urls,texts){
        return new Promise((resolve, reject) => {
            var options = { method: 'POST',
              // url: 'http://localhost:3005/api/v1/real-estate-extraction',
              url: urls,
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
              body: [ texts ],
              json: true };

            request(options, function (error, response, body) {
              if (error) throw new Error(error);
              resolve(body);
            });
        })
    }
}