/*
 * getChildren is function implemented by customers
 * @param: node: Node
 * @param: getChildren: func
 * See usage from /js/dom_filter.js
 * author: Lei Wang (yiak.wy@gmail)
 * created on: Nov 1st, 2017
 */
function walk_dom(node, getChildren){
	if (node === null){
		return
	}
	var queue = [node], curr = undefined
	while(queue.length){
		curr = queue.shift()
		var array_ = dom_Array(curr.children)
		queue.extend(getChildren(curr, array_))
	}
	return node
}

// helper libs
function dom_Array(els){
	var array_ = []
	Array.prototype.push.apply(array_, els)
	return array_
}

function extend(array_){
	Array.prototype.push.apply(this, array_)
	return this
}
Array.prototype.extend = extend

function each(f){
	var array_ = this
	if (array_.constructor !== Array) {
		throw Error("bad binding")
	}
	return array_.map(f)
}
Array.prototype.each = each
// You might want to refer jQuery for this implemenation
// Basically you have two things to do:
//  1) verify wether the original value and the new value is equal
//  2) verify the copy mode whether is deep or not; if it is deep repeat the proc for each prop; if it is not just cover the original value
function extendOptions(target, obj) {
	var deep = false
	if (arguments.length > 2 && typeof arguments[2] === "boolean") {
		deep = arguments[2]
	} else {
		throw Error(`wrong function signature for {arguments[2]}!`)
	}
	
	if (typeof target === "boolean" ) {
		deep = target,
		target = this
	}
		
	for (name in obj) {
		original = target[name]
		repl = obj[name]
		
		if (original === repl) {
			continue
		}
	
		if (deep && (original.constructor === Object) || (original.construct === Array)) {
			// deep copy
			target[name] = extendOptions(original, repl, deep)
			
		} else {
			// shallow copy
			target[name] = repl
		}
		
	}
	return target
}
Object.prototype.extend = extendOptions

// Added on 1st Nov 2017
// In practive, I found that people (including me) might call dom walk alike routines multiple times for different purposes, which brings a lot of duplicated traversal work.
// The ruff ideas is that we can compress the search routes by compressing multi tasks in a single processor
// In the new work flow, we first register tasks to generate "walk_dom" callback, then call walk dom
// e.g.:
//   var bundel = new Bundle
//   var id = bundle.register(task) or bundle.update(id, task)
//   var getChildren = getChildrenFunc(bundle)
function getChildrenFunc(tasks) {
	
}

function* counter(){
	var index = 0
	while (1) {
		yield index++
	}
}