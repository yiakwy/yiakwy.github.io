/**
 * Created by wangyi (yiak.wy@gmail.com) on 2015.
 * Updated by wangyi (yiak.wy@gmail.com) on April 23, 2017
 */

(function (factory) {
   if (typeof define === 'function' && define.amd) {
      // Loading from AMD script loader. Register as an anonymous module.
      define(["jquery"], factory)
   } else if (typeof define === 'function' && define.cmd){
      // CommonJS, for seajs users
       define("jsInj",(function (factory){
           // tradeoff between factory and CJ standard
           return function(require, exports, module){
               return factory(true, null, require, exports, module)
           }
       })(factory));
   } else if (typeof exports === 'object') {
      // CommonJS
      var jsInj = module.exports = factory(true, require);
      jsInj.trigger_func = function(){}
   } else {
      // Browser using plain <script> tag, test environment
      factory(false);
   }
} (function (isCommonJS, fs) {
	// fs is for node users
	isCommonJS = isCommonJS === true;
	// ============================= plugin def  =============================
	var VERSION = '0.1.0',
		NAME = 'jsInj',
		AUTHOR = 'Lei Wang',
		EMAIL = 'yiak.wy@gmail.com';

	var $jsInj = function (settings) {
			_classCallCheck(this, $jsInj);
			_init(settings);
        },
        global = (0, eval)('this');
	
	$jsInj.prototype = {
		_init: _init,
		_classCallCheck: _classCallCheck,
		check_support: check_support,
		get_env: get_env,
		walk_dom: walk_dom,
		remove_scripts: remove_scripts,
		wrap: wrap,
		add_click_me: add_click_me,
		bibitexParse: bibitexParse
	}
	
	// update interface
	
	// register to $ name space
	
	var defaultSettings = {};
	
	// global function
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

	if (isCommonJS && !fs) {
		var _args = Array.prototype.slice.call(arguments);
		require = _args[2];
        exports = _args[3];
        module  = _args[4];
	} else if (!isCommonJS) {
		$ = global.jQuery;
	}
	
	$.fn.jsInj = $jsInj;
	
	function walk_dom(node, getChildren){
		if (node === null){
			return
		}
		var queue = [node], _curr = undefined
		while(queue.length){
			_curr = queue.shift()
			var _array = dom_Array(_curr.children)
			queue.extend(getChildren(_curr, _array))
		}
		return node
	}

	// helper libs
	function dom_Array(elements){
		var _array = []
		Array.prototype.push.apply(_array, elements)
		return _array
	}

	function extend(_array){
		Array.prototype.push.apply(this, _array)
		return this
	}
	Array.prototype.extend = extend

	// ================================ application ================================
	function remove_scripts(){
		var node = walk_dom(document, function(parent, 
												children) {

			var selected = []
			for (child of children) {
				if (child.nodeName === "SCRIPT" || child.nodeName === "STYLE") {
					parent.removeChild(child)
				}
				else {
					selected.push(child)
				}
			}
		   	return selected
		})
		// for interprocess communication 
		console.log(node)
		bodyText = node.body.innerText, 
		body = node.body.innerHTML
		bodyText = bodyText.split('\n').filter(function(node){
			if (node === "" ){return 0} return 1})  
		return "success"
	}
	
	function wrap(tag, cls) {
		var doc = document,
			root = doc.querySelector("div.post")
		var node = walk_dom(root, function(parent,
										   children) {
			
			var selected = [];
			for (child of children) {
				if (child.tagName == tag.toUpperCase()) {
					var ori = child.outerHTML
					child.outerHTML = '<div class="' + cls + '" alt="' + child.alt + '">' + ori + '</div>'
					parent.children[0].id = child.alt
				} else {
					selected.push(child)
				}
			}
			return selected
		})
	}
	
	function add_click_me() {
		var doc = document,
			root = doc.querySelector("div.post section>ol")
		var node = walk_dom(root, function(parent,
										   children) {
			var selected = [];
			for (child of children) {
				if (child.tagName == "OL" || child.tagName == "UL") {
					var template = doc.createElement('TEMPLATE')
					template.innerHTML = "<span style=text-decoration:underline;font-size:small;color:red;>click me</span>"
					var click_me = template.content.firstChild
					parent.insertBefore(click_me, child)
					break;
				} else 
				if (child.tagName == "LI") {selected.push(child)}
			}
			return selected				
		})
	}
	
	function bibitexParse() {
		var fmt = "";
		return fmt;
	}
	
	return $jsInj;

}))