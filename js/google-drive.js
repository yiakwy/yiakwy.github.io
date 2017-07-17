(function(factory) {
	if (typeof define === 'function' && define.amd) {
		define(factory)
	} else if (typeof define === 'function' && define.cmd){
		define("YiLetter", factory(require, exports, module))
	} else if (typeof exports === 'object') {
		var YiLetter = module.exports = factory(require)
	} else {
		var global = (0, eval)('this')
		global.YiLetter = factory(null)
	}
}(function (require){
	var isCommonJS = true
	if (require === null) {
		isCommonJS = false
	}
	// ============================= plugin def  =============================
	var VERSION = '0.1.0',
		NAME = 'YiLetter',
		AUTHOR = 'Lei Wang',
		EMAIL = 'yiak.wy@gmail.com'
	
	var $YiLetter = function (settings) {
			_classCallCheck(this, $YiLetter)
			_init(settings)
        },
        global = (0, eval)('this')
	
	if (isCommonJS) {
		// $ = require("jQuery")
		// gapi = require("gapi")
	} else {
		if (global.jQuery !== undefined) {
			$ = global.jQuery
		}
		var $ = $ || {}
	}
	
	var defaultSettings = {
			clientId: '1009352751052-3kn4v3g9terh3t2q7gu5octboksb806q.apps.googleusercontent.com',
			discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"],
			scope: 'https://www.googleapis.com/auth/drive.file'
				/*['https://www.googleapis.com/auth/drive.metadata.readonly',
				   'https://www.googleapis.com/auth/drive.appdata',
				   'https://www.googleapis.com/auth/drive.file']*/
		}
	
	function gDrive(meta) {
		this.name = meta.name
		this.mimeType = meta.mimeType
	}
	
	$YiLetter.prototype = {
		_init: _init,
		_classCallCheck: _classCallCheck,
		check_support: check_support,
		isMobile: isMobile,
		get_env: get_env,
		handleClientLoad: handleClientLoad
		}
	
	if ($ != undefined && $.fn !== undefined) {
		$.fn.YiLetter = $YiLetter
		$.fn.extend($YiLetter)
	}
	
	// global functions
	function _init(settings) {
		this.settings = $.extend({}, defaultSettings, settings)
	}
	
	function _classCallCheck(instance, Constructor) {
		if (!(instance instanceof Constructor)) {
			throw new TypeError("Cannot call a class as a function");
		}
	}

	function get_env() {
		var nav = global.navigation;
		return {appName: nav.appName, version: nav.appVersion}
	}
	
	function check_support() {
		var tips = '<p class="ieTips">for better experience, please use chrome!<a href="javascript:;" class="close"><img src="/assets/images/icon/ie_tips_close.png"/></a></p>';
		var userAgent = window.navigator.userAgent.toLowerCase();
		$.browser.msie9 = $.browser.msie && /msie 9\.0/i.test(userAgent);
		$.browser.msie8 = $.browser.msie && /msie 8\.0/i.test(userAgent);
		$.browser.msie7 = $.browser.msie && /msie 7\.0/i.test(userAgent);
		$.browser.msie6 = !$.browser.msie8 && !$.browser.msie7 && $.browser.msie && /msie 6\.0/i.test(userAgent);
		if ($.browser.msie8 || $.browser.msie7 || $.browser.msie6 || $.browser.msie9) {
			$(tips).insertBefore('.container');
			$(tips).insertBefore('.login_logo');
			$('.close').click(function () {
				$('.ieTips').slideUp();
			})
			return true
		} else {
			return false
		}
	}
	
	function isMobile() {
		var mobile = /iPhone|Android|iPad|iPod/i
		if( mobile.test(navigator.userAgent))
		{
			return true;
		}
		else {
			return false;
		}
	}
	
	// google drive
    function handleClientLoad() {
        gapi.load('client:auth2', initClient);
    }
		
	function authenticate() {
		gapi.auth2.getAuthInstance().isSignedIn.listen(handleSignedIn)
		gapi.auth2.getAuthInstance().signIn()
		if (gapi.auth2.getAuthInstance().isSignedIn.get()){
			// for signed in events here! Lei
			test()
		}
	}

	function handleSignedIn(isSignedIn) {
		if (isSignedIn) {
			alert("successful, we can navigate through google drive now!")
		} else {
			alert("client connect to google cloud not successful!")
		}
	}
		
	function initClient() {
		gapi.client.init(this.settings).then(authenticate, function(err) {
			console.log(err)
			alert(err)
		})
	}
	
	// google
	function modify(target, callback, method) {
		// Implements RFC 2387 Multipart content type for google REST api
		const boundary = '--MultiBoundary';
    	const delimiter = "\r\n--" + boundary + "\r\n";
    	const close_delim = "\r\n--" + boundary + "--";
		const end = "\r\n\r\n"
		var mimeType = target.mime_type
		var multipart_body = delimiter +  'Content-Type: application/json' + end +
        					 JSON.stringify({
								 				'mimeType': mimeType, 
								 				'name': target.name
							 				}) +
							 delimiter + 'Content-Type: ' + mimeType + end +
        					 target.contents +
        					 close_delim	
		if (method == 'POST') {
			return gapi.client.request({
				'path': '/upload/drive/v3/files/',
				'method': method,
				'params': {'uploadType': 'multipart'},
				'headers': {'Content-Type': 'multipart/mixed; boundary=' + boundary},
				'body': multipart_body,
				'callback': callback || function(file){console.log(file)}
			})
		} else {
			for (var i=0; i < target.files.length; i++) {
				   gapi.client.request({
				'path': '/upload/drive/v3/files/' + target.files[i].id,
				'method': method,
				'params': {'uploadType': 'multipart'},
				'headers': {'Content-Type': 'multipart/mixed; boundary=' + boundary},
				'body': multipart_body,
				'callback': callback || function(file){console.log(file)}
				})
			}
		}
	}
	
	function create(target, 
					callback) {
		
		function success(response) {	
			console.log(" find " + response.result.files.length + " files ")
			target.files = response.result.files
			modify(target, callback, "PATCH")
		}
		
		function error(reason) {
			modify(target, callback, "POST")
		}
		
		query_ob("name+=+" + "%27" + target.name + "%27", success, error)
	}
	
	function _delete(target) {
		
	}
		
	function get(target, callback) {
		return gapi.client.request({
			'path': "/drive/v3/files/" + target.fileId,
			'method': "GET",
			'callback': callback || function(file){console.log(file)}
		})
	}
	
	function query_ob(selector, success, error) {
		return gapi.client.request({
			'path': "/drive/v3/files/?q=" + selector,
			'method': "GET",
		}).then(success, error)
	}
	
	function test() {
		var target = {
				name: "SimpleTest.txt",
				contents: "Hello World! This is a test message!",
				mime_type: "text/html"
			}
		create(target, function(file){
				var ret = get({fileId: file.id})
				console.log("fetched file " + file.name + ":")
				console.log(ret)
				})
	}
	
	return $YiLetter

}))