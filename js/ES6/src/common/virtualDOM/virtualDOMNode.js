import "./utils.js" //  walk_dom


class Node {
	constructor(tagName, attrs, children){
		if (tagName === null)
			throw Error("tagName must be set")
		this.tagName = tagName
		this.attrs = attrs || {}
		
		this.children = children || []
		this.parent = null
		this.level_pos = 0
		this.depth = null
		this.key = null
	}
	
	toString() {
		return `<Node key={this.key}>`
	}
	
	setattr(attrs) {
		if (attr.constructor === Object || attr.construct === Array){
			for (key in attrs){
				this.attrs[key] = attrs[key] 
			}
		} 
	}
	
	setkey(keygen) {
		this.key = keygen.next()
	}
	
	add(child) {
		this.children.push(child)
	}
	
	set_level_pos (pos) {
		this.level_pos = pos
	}
	
	render() {
		// the most important method
		var el = document.createElement(this.tagName)
		el.setAttribute(this.attrs)
		children.each(node) {
			var child
			if (node instanceof Node) {
				child = node.render()
			}
			el.append(child)
		}
		return el
	}

}

// TO DO: Since inorder and post order can uniquely identify a binary tree, we can compare trees by inpecting their equivalent traversal traces
function binarytree_converter(tree) {
	
}

// Facebook diff algorithm will work as benchmark
// my plan is first stage: 
//  1. Nov ~ Dec: Facebook algorithm
//  2. Dec ~ Jan: Proposed traversal comparison algorithm. Just for fun!

