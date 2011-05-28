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

	output : function(params, writeCallback){
		var net = new brain.NeuralNetwork();
		var netFileAbsPath = path.join(ABS_BASE_PATH,FILES_DIR_NAME,params.name+'.json');

		/* @process
			NN net from repository
		*/
		net.fromJSON(JSON.parse(fs.readFileSync(netFileAbsPath, ENCODING)));

		/* @process
			NN net run
		*/
		if(eval(params).test || !params.length){
			output = net.run({r:1, g:1, b:0});
		}
		else{
			params = eval('('+params+')');
			for(k in params){
				params[k] = parseInt(params[k]);
			}
			output = net.run(params);
		}

 		writeCallback(localProcess.get.output(output));
	},

	get : {
		output : 
			function(output){
				/* @process
					Output
				*/
				var output_s = '{';
				var i = 0;
				for(k in output){
					if (i>0) output_s += ', ';
					output_s += '"'+k+'"' + ' : ' + output[k];
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



