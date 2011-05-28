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

var consoleLog=function(s){
	console.log(s);
}

var localProcess = {
	obj : {
	},

	output : 
		function(params, writeCallback){
			var net = new brain.NeuralNetwork();
			var netFileAbsPath = path.join(ABS_BASE_PATH,FILES_DIR_NAME,params.name+'.json');

			/* @process
				internal' callback 
			*/		
			this.netFileExistsCallback=function(exists){
				/* @process
					if both: 
						-	'net' GET|POST param is provided
						-	netFileAbsPath exists
					...netFileAbsPath takes precedence
				*/
				if(exists){
					net.fromJSON(JSON.parse(fs.readFileSync(netFileAbsPath, ENCODING)));
				}
				else if(params.net){
					net.fromJSON(JSON.parse(params.net));
				}

				/* @process
					NN net training data
				*/
				var data = localProcess.get.data(params)				

				/* @process
					NN net actual training process
				*/
				net.train(data);

				/* @process
					NN net save
				*/
				var ioParams = {
					file:netFileAbsPath,
					data:JSON.stringify(net.toJSON()), 
					output:'',
					_status: 1
				};
				localProcess._do.saveFile(ioParams)

				/* @process
					Output	
				*/
				var output = {"message" : "training complete, nn saved"} 
				if (ioParams._status!=1){
					output = {"message" : "training complete, error saving nn: "+ioParams.output} 
				}

				writeCallback(localProcess.get.output(output));
			};


			/* @process
				Entry point, with callback containing processing methods	
			*/
			path.exists(netFileAbsPath,	this.netFileExistsCallback);
		},

	get : { 
		data : 
			function(params){
				var data = {};
				if(params.test || !params.length){
					data = [{input: {r:1, g:0.65, b:0},  output: {orange: 1}},
							{input: {r:0, g:0.54, b:0},  output: {green: 1}},
							{input: {r:0.6, g:1, b:0.5}, output: {green: 1}},
							{input: {r:0.67, g:0, b:1},  output: {purple: 1}}];
				}
				else {
					data = JSON.parse(params.data);
				}

				return data;
			},

		output : 
			function(output){
				var output_s = '{';
				var i = 0;
				for(k in output){
					if (i>0) output_s += ', ';
					output_s += '"'+k+'"' + ' : ' + '"'+output[k]+'"';
					i++;
				}
				output_s += '}';
				return output_s;
			}
	},
	
	_do : {
		saveFile : 
			function(ioParams){
				try {
					fs.writeFileSync(ioParams.file, ioParams.data, ENCODING);
				}
				catch(e){
					ioParams._status =  0;
					ioParams.output = 'Error: '+e.message;
					consoleLog('e.message: '+e.message);
				}
			},

		response : {
			write : 
				function(output){
					setTimeout(function () {
						var response = localProcess.obj.response;
						response.writeHead(200, {'Content-Type': 'text/plain'});
						response.write(output);
						response.end();
					}, 100);
				}
		}
	}
};

http.createServer(
	/*
		THanks to: http://stackoverflow.com/questions/4295782/node-js-extracting-post-data
	*/
	function (request, response) {
		var lp = localProcess;
		lp.obj['response'] = response;		
		lp.obj['request'] = request;		

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
			
			lp.output(params, lp._do.response.write)
		}
}).listen(8011);

sys.puts('Server running at http://127.0.0.1:8011/');



