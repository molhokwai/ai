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
				var output = {"message" : "training complete, nn saved"} 
				try {
					net.train(data);
				}
				catch(e){
					output = {"message" : "Error during training. A clue: retrying with different training..."} 
				}

				if (output.message.indexOf("Error")<0){
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
					if (ioParams._status!=1){
						output = {"message" : "training complete, error saving nn: "+ioParams.output} 
					}
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

var e = exports;
e.localProcess = localProcess;

