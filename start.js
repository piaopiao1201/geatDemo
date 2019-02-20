const iconv = require('iconv-lite');
var spawn = require('child_process').spawn;
var stategy=1;
var data={
	orderSum:4500,
	faInfo:[
		{
			"No":3,
			"P":53,
			"C":34,
			"Q":93,
			"O":57,
			"L":68,
			"minAccept":460
		},
		{
			"No":1,
			"P":46,
			"C":23,
			"Q":95,
			"O":67,
			"L":45,
			"minAccept":600
		},
		{
			"No":8,
			"P":70,
			"C":30,
			"Q":96,
			"O":58,
			"L":35,
			"minAccept":1100
		},
		{
			"No":2,
			"P":67,
			"C":43,
			"Q":97,
			"O":92,
			"L":23,
			"minAccept":1300
		},
		
		{
			"No":6,
			"P":58,
			"C":28,
			"Q":96,
			"O":75,
			"L":51,
			"minAccept":750
		},
	]
}
var ls = spawn('python',['run.py',JSON.stringify(data),stategy]);
var dataAll=[];
ls.stdout.on('data',function(data){
	// console.log(iconv.decode(data, 'gbk'))
	dataAll.push(data)
})
ls.stdout.on('end',function(data){
	// console.log(iconv.decode(data, 'gbk'))
	// console.log(Buffer.concat(dataAll));
	console.log(iconv.decode(Buffer.concat(dataAll), 'gbk'))
})