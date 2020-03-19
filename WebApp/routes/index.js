var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var tunnel = require('tunnel-ssh');
const utf8 = require('utf8');
process.env.MONGODB_URI
mongoose.connect(process.env.MONGODB_URI);
// mongoose.connect('mongodb://localhost:27017/local');
// mongoose.connect('localhost:27017/demo2');
//mongoose.connect('localhost:27017/tutorial');
const api_helper = require('../api/api_helper')

/*
var config = {
    username:'root',
    host:'localhost',
    agent : process.env.SSH_AUTH_SOCK,
    privateKey:require('fs').readFileSync('/Users/myusername/.ssh/id_rsa'),
    port:27017,
    dstPort:8000,
    password:''
};


var server = tunnel(config, function (error, server) {
    if(error){
        console.log("SSH connection error: " + error);
    }
    mongoose.connect('localhost:27017/demo');

    var dbs = mongoose.connection;
    dbs.on('error', console.error.bind(console, 'DB connection error:'));
    dbs.once('open', function() {
        // we're connected!
        console.log("DB connection successful");
    });
});
*/

var dbs = mongoose.connection;
    dbs.on('error', console.error.bind(console, 'DB connection error:'));
    dbs.once('open', function() {
        // we're connected!
        console.log("DB connection successful");
    });

var Schema = mongoose.Schema;

var file = new Schema({
  title: {type: String, required: true},
  content: String,
  author: String
}, {collection: 'file'});

var dbSchema = new Schema({}, {strict: false});
var db = mongoose.model('db', dbSchema, 'file');

var File = mongoose.model('File', file);

// function findAllMembersCursor() {
//     return db.find().cursor();
// }

// async function test() {
//     const membersCursor = await findAllMembersCursor();
//     let N = 0;
//     await membersCursor.eachAsync(member => {
//         N++;
//         console.log(`${member}`);
//     });
//     console.log(`loop all ${N} members success`);
// }

/* GET home page. */
router.get('/', function(req, res, next) { 
  // if (req != undefined){  
  var price = req.query.price;
  if (req.query.textsrc != undefined && req.query.textsrc != ''){
    //console.log(req.query.textsrc);
    const text = req.query.textsrc.toString();
    //console.log(text);
    api_helper.make_API_call('http://localhost:3005/api/v1/real-estate-extraction',text)
    .then(response => {
        // res.json(response);
        body = response;
        var district_tb;
        var price_tb;
        var type_tb;
        var floor_tb;
        var room_tb;
        var street_tb;
        for (var i = 0; i < body[0].tags.length; i++){
          if (body[0].tags[i].type == 'addr_district'){
            district_tb = body[0].tags[i].content.toLowerCase();
          
          }
          if (body[0].tags[i].type == 'price'){
            price_tb = body[0].tags[i].content;
          }
          if (body[0].tags[i].type == 'realestate_type'){
            type_tb = body[0].tags[i].content;
          } 
          if (body[0].tags[i].type == 'interior_floor'){
            floor_tb = body[0].tags[i].content;
          }
          if (body[0].tags[i].type == 'addr_street'){
            street_tb = body[0].tags[i].content;
          } 

        }
        console.log(district_tb);
        console.log(price_tb);
        console.log(type_tb);
        console.log(street_tb);
        if(price_tb == undefined || price_tb == '' || price_tb == NaN)
        {
          console.log(1);
          price_tb = parseInt(price_tb);
           db.find({attr_addr_district:new RegExp(district_tb, 'i'), attr_addr_street:new RegExp(street_tb, 'i'),
            attr_realestate_type:new RegExp(type_tb, 'i')})
            .limit(1000).then(function(doc) {
            res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""),textsrc: text, district: 'Quận', type: 'Loại', price: 'Giá'});
           });
        }
        else{
          console.log(2);
          price_tb = parseInt(price_tb);
          db.find({attr_addr_district:new RegExp(district_tb, 'i'), attr_price_min:{$lte:price_tb},
            attr_realestate_type:new RegExp(type_tb, 'i'), attr_addr_street:new RegExp(street_tb, 'i')})
            .limit(1000).then(function(doc) {
              res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""),textsrc: text, district: 'Quận', type: 'Loại', price: price_tb});
             });
        }
    })
    .catch(error => {
        res.send(error);
    })
    
    // db.find({$and: [{attr_addr_district:{$in:[district_tb]},
    // {attr_realestate_type:{$lte:price_tb}}] })



  }
  else 
  if (price == undefined || price == ''){
    console.log(1);
    if (req.query.district == 'quận 1')
    {
      db.find({attr_addr_district:'quận 1',
    attr_realestate_type:new RegExp(req.query.type, 'i')})
    .limit(1000).then(function(doc) {
         res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""),textsrc: 'tìm kiếm', district: req.query.district, type: req.query.type, price: 'Chọn Giá'});
       });
    }
    else{
    db.find({attr_addr_district:new RegExp(req.query.district, 'i'),
    attr_realestate_type:new RegExp(req.query.type, 'i') })
    .limit(1000).then(function(doc) {
        var test1 = JSON.stringify(doc);
        // var final1 = JSON.parse(test1.replace(/(\\n)+/g, ""));
         res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""),textsrc: 'tìm kiếm', district: req.query.district, type: req.query.type, price: 'Chọn Giá'});
       });
     }
  }
   
  else{
    console.log(2);
    price = parseInt(price);
    console.log(price)
    if (req.query.district == 'quận 1')
    {
      db.find({attr_addr_district:'quận 1',
    attr_realestate_type:new RegExp(req.query.type, 'i'), attr_price_min:{$lte:price}})
    .limit(1000).then(function(doc) {
         res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""),textsrc: 'tìm kiếm', district: req.query.district, type: req.query.type, price: 'Chọn Giá'});
       });
    }
    else{
    db.find({attr_addr_district:new RegExp(req.query.district, 'i'),
      attr_realestate_type:new RegExp(req.query.type, 'i'), attr_price_min:{$lte:price}})
      .limit(1000).then(function(doc) {
           res.render('test', {items: JSON.stringify(doc).replace(/(\\n)+/g, ""), textsrc: 'tìm kiếm', district: req.query.district, type: req.query.type, price: price});
         });
       }
   }



  // db.find()
  //     .then(function(doc) {
  //       console.log(doc.toString());
  //       // res.render('datatable', {items: doc });
  //     });

});

/* GET chart page. */
router.get('/chart', function(req, res, next) {
  //res.render('index');
  res.render('chart');
});

/* GET data table page. */
router.get('/datatable', function(req, res, next) {
  db.find()
      .then(function(doc) {
        //console.log(doc.toString());
        res.render('datatable', {items: doc });
      });
  //res.render('datatable', {tests: dataSet});
});

router.get('/get-data', function(req, res, next) {
  UserData.find()
      .then(function(doc) {
        res.render('index', {items: doc});
      });
});

router.post('/insert', function(req, res, next) {
  var item = {
    title: req.body.title,
    content: req.body.content,
    author: req.body.author
  };

  var data = new UserData(item);
  data.save();

  res.redirect('/');
});

router.post('/update', function(req, res, next) {
  var id = req.body.id;

  UserData.findById(id, function(err, doc) {
    if (err) {
      console.error('error, no entry found');
    }
    doc.title = req.body.title;
    doc.content = req.body.content;
    doc.author = req.body.author;
    doc.save();
  })
  res.redirect('/');
});

router.post('/delete', function(req, res, next) {
  var id = req.body.id;
  UserData.findByIdAndRemove(id).exec();
  res.redirect('/');
});

module.exports = router;
