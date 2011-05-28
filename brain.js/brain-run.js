/* brain library installed with npm 
    source : http://harthur.github.com/brain/
*/
var sys = require('sys');
var http  = require('http');
var qs = require('querystring');
var url = require('url');

var brain = require('brain');
var net = new brain.NeuralNetwork();

var getOutput = function(params){
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

	output_s = '{';
	var i = 0;
	for(k in output){
		if (i>0) output_s += ', ';
		output_s += '"'+k+'"' + ' : ' + output[k];
		i++;
	}
	output_s += '}';
	return output_s;
}

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
			response.write(getOutput(params));
			response.end();
		}, 100);
}).listen(8011);

sys.puts('Server running at http://127.0.0.1:8011/');

