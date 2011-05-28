/* brain library installed with npm 
    source : http://harthur.github.com/brain/
*/
ABS_BASE_PATH = '/home/herve/development/workspaces/learning/ai/brain.js';
FILES_DIR_NAME = 'files';
ENCODING = 'UTF8'

var sys = require('sys');
var http  = require('http');
var qs = require('querystring');
var url = require('url');
var fs = require('fs');
var path = require('path');

var brain = require('brain');

var saveFile=function(params){
	try {
		fs.writeFileSync(params.file, params.data, ENCODING);
	}
	catch(e){
		params.output = 'Error: '+e.message;
		console.log('e.description: '+e.message);
	}
};

var localProcess = {
	getOutput : 
		function(params){
			var net = new brain.NeuralNetwork();
			var netFileAbsPath = path.join(ABS_BASE_PATH,FILES_DIR_NAME,params.name+'.json');
			var data = {};

			/* @process
				internal' callback 
			*/		
			this.netFileExistsCallback=function(exists){
				console.log(exists.toString());
			};

			/* @process
				if both: 
					-	'net' GET|POST param is provided
					-	netFileAbsPath exists
				...netFileAbsPath takes precedence
			*/
			var netFileExists = null;
			path.exists(netFileAbsPath,	this.netFileExistsCallback);
			var i=0;

			console.log(netFileExists.toString());
			if(netFileExists){
				net.fromString(fs.readFileSync(netFileAbsPath, ENCODING));
				console.log(net.toString());
			}
			else if(params.net){
				net.fromString(params.net);
			}

			if(eval(params).test || !params.length){
				data = [{input: {r:1, g:0.65, b:0},  output: {orange: 1}},
						{input: {r:0, g:0.54, b:0},  output: {green: 1}},
						{input: {r:0.6, g:1, b:0.5}, output: {green: 1}},
						{input: {r:0.67, g:0, b:1},  output: {purple: 1}}];
				
			}
			else {
				data = JSON.parse(params.data);
			}

			net.train(data);
			var res = {
				file:path.join(netFileAbsPath),
				data:JSON.stringify(net.toJSON()), 
				output:''
			};
			saveFile(res);

			output = {"message" : "training complete, nn saved"} 
			if (res.output.indexOf('Error')==0){
				output = {"message" : "training complete, error saving nn: "+res.output} 
			}
			output_s = '{';
			var i = 0;
			for(k in output){
				if (i>0) output_s += ', ';
				output_s += '"'+k+'"' + ' : ' + '"'+output[k]+'"';
				i++;
			}
			output_s += '}';
			return output_s;
		}
};

http.createServer(
	/*
		THanks to: http://stackoverflow.com/questions/4295782/node-js-extracting-post-data
	*/
	function (request, response) {
		var params = {};
		if (request.method == 'POST') {
			var body = '';
			request.on('data', function (data) {
				body += data;
			});
			request.on('end', function () {
				params = qs.parse(body);
			});
		}
		else{
			/*Obscure 'true' parameter means: 'make key 'query' query string a dictionary object' */
			params = url.parse(request.url, true).query;
		}

		setTimeout(function () {
			response.writeHead(200, {'Content-Type': 'text/plain'});
			response.write(localProcess.getOutput(params));
			response.end();
		}, 100);
}).listen(8011);

sys.puts('Server running at http://127.0.0.1:8011/');

