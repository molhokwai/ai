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


http.createServer(
    /*
        THanks to: http://stackoverflow.com/questions/4295782/node-js-extracting-post-data
    */
    function (request, response) {
        var m = url.parse(request.url).pathname.split('/')[1];
		m = require('./'+m);

        var lp = m.localProcess;
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
        }
		
        lp.output(params, lp._do.response.write)
}).listen(8011);


sys.puts('Server running at http://127.0.0.1:8011/');

