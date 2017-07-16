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
		EMAIL = 'yiak.wy@gmail.com',
	
	var $YiLetter = function (settings) {
			_classCallCheck(this, $YiLetter)
			_init(settings)
        },
        global = (0, eval)('this')
	
	if (isCommonJS) {
		// $ = require("jQuery")
		// gapi = require("gapi")
	} else {
		$ = global.jQuery
		gapi = global.gapi
	}
	
	var defaultSettings = {
			clientId: '<YOUR_CLIENT_ID>',
			discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"],
			scope: 'https://www.googleapis.com/auth/drive.metadata.readonly',
		}
	
	function gDrive(meta) {
		this.name = meta.name
		this.mimeType = meta.mimeType
	}
	
	var $YiLetter.prototype = {
		_init: _init,
		_classCallCheck: _classCallCheck,
		check_support: check_support,
		isMobile: isMobile,
		get_env: get_env,
		handleClientLoad: handleClientLoad
		}
	
	$.fn.YiLetter = $YiLetter
	$.fn.extend($YiLetter)
	
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
	}

	function handleSignedIn(isSignedIn) {
		if (isSignedIn) {
			
		} else {
			alert("client connect to google cloud not successful!")
		}
	}
		
	function initClient() {
		gapi.client.init(this.settings).then(authenticate)
	}
	
	function create(target) {
		var drive = gapi.client.drive
		drive.files.create({
			resource: target,
			fields: 'id'
						    }, function(err, file) {
									if (err) {
										console.log(err)
									} else {
										console.log('Crated Fold ID:', file.id)
									}
								})
	}
		
	function delete(target) {
		
	}
		
	function get(target) {
	
	}
	
	return $YiLetter

})