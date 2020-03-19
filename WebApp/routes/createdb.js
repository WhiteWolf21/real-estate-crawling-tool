var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
var tunnel = require('tunnel-ssh');
const utf8 = require('utf8');
//<script type="text/javascript">
 mongoose.connect('localhost:27017/demo2');


var dbs = mongoose.connection;
    dbs.on('error', console.error.bind(console, 'DB connection error:'));
    dbs.once('open', function() {
        // we're connected!
        console.log("DB connection successful");
    });

var Schema = mongoose.Schema;

var file3 = new Schema({
  page: String,
  link: String,
  title: String,
  post_id: String,
  message: String,
  post_date: String,
  crawled_date: String,
  score: String,
  attr_addr_number: String,
  attr_addr_street: String,
  attr_addr_district: String,
  attr_addr_ward: String,
  attr_addr_city: String,
  attr_position: String,
  attr_surrounding: String,
  attr_surrounding_name: String,
  attr_surrounding_characteristic: String,
  attr_transaction_type: String,
  attr_realestate_type: String,
  attr_potential: String,
  attr_area: String,
  attr_price: String,
  attr_price_min: Number,
  attr_price_max: String,
  attr_price_m2: Number,
  attr_interior_floor: String,
  attr_interior_room: Number,
  location_lng: Number,
  location_lat: Number,
  source: String,
  dataBank:Array,
  dataSchool: Array,
  dataBus_Stations: Array,
  dataMarket: Array,
  dataSupermarket: Array,
  dataHospital: Array
}, {collection: 'file3'});


var file1 = new Schema({
  title: {type: String, required: true},
  content: String,
  author: String
}, {collection: 'file1'});

var file2 = new Schema({
  title: {type: String, required: true},
  content: String,
  author: String
}, {collection: 'file2'});


//var dbSchema = new Schema({}, {strict: false});
var dbSchema1 = new Schema({}, {strict: false});
var dbSchema2 = new Schema({}, {strict: false});
var dbSchema3 = new Schema({}, {strict: false});

//var db = mongoose.model('db', dbSchema, 'file');
var db1 = mongoose.model('db1', dbSchema1, 'file1');
var db2 = mongoose.model('db2', dbSchema2, 'file2');
var db3 = mongoose.model('db3', dbSchema3, 'file3');

//var File = mongoose.model('File', file);
var File1 = mongoose.model('File1', file1);
var File2 = mongoose.model('File2', file2);
var File3 = mongoose.model('File3', file3);

var dataSet1 = [];
var dataSet2 = [];
var dataBank = [];
var dataBus_Stations = [];
var dataHospital = [];
var dataMarket = [];
var dataSupermarket = [];
var dataSchool = [];

var center ;
var radius ;
var location;
  db1.find() .then(function(doc){
        doc.forEach(function(element) {
            var test1 = JSON.stringify(element);
            var final1 = JSON.parse(test1);
          //  console.log(final1);
            dataSet1.push([final1["page"], final1["link"], final1["title"],final1["post_id"],final1["message"],
                final1["post_date"], final1["crawled_date"],final1["score"], final1["attr_addr_number"],
                final1["attr_addr_street"],final1["attr_addr_district"],final1["attr_addr_ward"],final1["attr_addr_city"],final1["attr_position"],final1["attr_surrounding"],
                final1["attr_surrounding_name"],final1["attr_surrounding_characteristics"], final1["attr_transaction_type"], final1["attr_realestate_type"],
                final1["attr_potential"],final1["attr_area"], final1["attr_price"], final1["attr_price_min"], final1["attr_price_max"],
                final1["attr_price_m2"], final1["attr_interior_floor"], final1["attr_interior_room"],
                final1["location_lng"], final1["location_lat"], final1["source"]]);
        });
      //  console.log(dataSet1);
        db2.find() .then(function(doc1){
              doc1.forEach(function(element) {
                  var test2 = JSON.stringify(element);
                  var final2 = JSON.parse(test2);
                  //console.log(final2);
                  dataSet2.push([final2["type"]["0"], final2["name"], final2["address"], final2["location"]["lat"],
                  final2["location"]["lng"]]) ;
              });
          //console.log(dataSet2);
        // for(var i = 0; i < 2; i++) {

        function test(i){
            for(var j = 0; j < dataSet2.length; j++){
              radius = 1; // radius đơn vị km
            var bool = Distance(distanceInKmBetweenEarthCoordinates(parseFloat(dataSet1[i][28]),parseFloat(dataSet1[i][27]),
                      parseFloat(dataSet2[j][3]),parseFloat(dataSet2[j][4])), radius)
             console.log(i.toString() + '---' + j.toString() + '---' + bool.toString());

            if (bool == true){
                if(dataSet2[j][0].match(/bank/g)) {
                  dataBank.push([dataSet2[j][0],dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
              //    console.log(dataBank);
                };

                if(dataSet2[j][0].match(/school/g)){
                  dataSchool.push([dataSet2[j][0], dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
                //  console.log(dataSchool);
                };

                if(dataSet2[j][0].match(/bus/g)){
                  dataBus_Stations.push([dataSet2[j][0], dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
                  //console.log(dataBus_Stations);
                };

                if(dataSet2[j][0] == "market"){
                  dataMarket.push([dataSet2[j][0], dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
                //  console.log(dataPark);
                };
                if(dataSet2[j][0] == "supermarket"){
                  dataSupermarket.push([dataSet2[j][0], dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
                //  console.log(dataPark);
                };

                if(dataSet2[j][0].match(/hospital/g)){
                  dataHospital.push([dataSet2[j][0], dataSet2[j][1], dataSet2[j][2], dataSet2[j][3], dataSet2[j][4]]);
                //  console.log(dataHospital);
                };
            }

          }
          var item = { page: dataSet1[i][0], 
                             link: dataSet1[i][1], title: 
                             dataSet1[i][2],post_id: dataSet1[i][3],
                             message: dataSet1[i][4],
                            post_date: dataSet1[i][5],
                            crawled_date: dataSet1[i][6],
                            score: dataSet1[i][7],
                            attr_addr_number: dataSet1[i][8],
                            attr_addr_street: dataSet1[i][9],
                            attr_addr_district: dataSet1[i][10], 
                            attr_addr_ward: dataSet1[i][11],
                            attr_addr_city: dataSet1[i][12],
                            attr_position: dataSet1[i][13],
                            attr_surrounding: dataSet1[i][14],
                            attr_surrounding_name: dataSet1[i][15], 
                            attr_surrounding_characteristics: dataSet1[i][16],
                            attr_transaction_type: dataSet1[i][17],
                            attr_realestate_type: dataSet1[i][18],
                            attr_potential: dataSet1[i][19],
                            attr_area: dataSet1[i][20],
                            attr_price: dataSet1[i][21], 
                            attr_price_min: dataSet1[i][22],
                            attr_price_max: dataSet1[i][23],
                            attr_price_m2: dataSet1[i][24],
                            attr_interior_floor: dataSet1[i][25],
                            attr_interior_room: dataSet1[i][26],
                            location_lng: dataSet1[i][27],
                            location_lat: dataSet1[i][28],
                            source: dataSet1[i][29],
                            dataBank: dataBank, 
                            dataSchool: dataSchool, 
                            dataBus_Stations: dataBus_Stations,
                            dataMarket: dataMarket,
                            dataSupermarket: dataSupermarket, 
                            dataHospital: dataHospital}

          var data = new File3(item);
          dataMarket = [];
          dataSupermarket = [];
          dataSchool = [];
          dataBank = [];
          dataBus_Stations = [];
          dataHospital = [];
          data.save(function(error){
                 console.log(1)
                  if(error)
                      console.error(error);
              });
            
            setTimeout(test, 2000,++i);
      }
            setTimeout(test, 2000, 6128);

    });
  });

  function Distance (dis, radius){
  if(dis <= radius){  
    return true;
  }
  else {
     return false;
  }
}
function degreesToRadians(degrees) {
  return degrees * Math.PI / 180;
}

function distanceInKmBetweenEarthCoordinates(lat1, lon1, lat2, lon2) {
  var earthRadiusKm = 6371;

  var dLat = degreesToRadians(lat2-lat1);
  var dLon = degreesToRadians(lon2-lon1);

  lat1 = degreesToRadians(lat1);
  lat2 = degreesToRadians(lat2);

  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  return earthRadiusKm * c;
}

