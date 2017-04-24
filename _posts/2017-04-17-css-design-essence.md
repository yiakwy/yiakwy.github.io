---
layout: post
title: "The Essence of Designing Css in Personal Website"
date: 2017-04-15
reading_expenditure: 6
excerpt_separator: <!--more-->
---

> Beauty is simple and beauty is in mind

## Introduction 
Technology www helps people to connect with each other. Knowledge produced nowadays dramatically increase and shared among people. 
<!--more-->
Being able to write an article and sharing your poin of views among peers will be of great values to build your intellectual Personality. But wait, are you crazy on articles formats, pictures and visual effects? I am going to share you with some simple techniques where you can apply to your personal blogs with simple moderate coding. Moreover, if you go through my github pages, you might have found, that writing css is not too hard for u to accomplish.

## How does it work?
The most important thing about articles is content. In content centralised media era, we will stick to the content of which the structure is carefully organized. But to digest it thoroughly, we need formats to express it. Formats in this article is implemented using *css* or *sass*. They, however, are not a panacea to all conent expressing prblems.

To make full use of it, we have to carry out basic study on structure of conents. Conent has a topic or headline, which will be explained in serveral subtopics. They come either externally or interally. For example:

1. External contents: typically called as **blockquote**.
	1. non-official references
	2. bibliography
	3. convention or best practices
2. Interal contents: frequently refered as author's point of views.
	1. intro
	2. body
		- introduction
		- theory
		- example
		- instance
		- extension
		- conclusion
	3. conclusion
	
After we establish conents sources, it is our duty to list evidence to support them. These will be expressed inside __paragraph__. A __paragraph__ has margins, margins to borders, margins inside. there are thousands of Hamlet residing thousands of readers. They are different from people to people.

All these structures now will be implemented by writing *css* and *sass*.

## What is css and sass?
CSS is short for **Cascading Style Sheets**. It origins from Oct, 1994 by [Håkon Wium Lie](https://en.wikipedia.org/wiki/H%C3%A5kon_Wium_Lie), when "he is working with [Tim Berners-Lee](https://en.wikipedia.org/wiki/Tim_Berners-Lee) at  Conseil Européen pour la Recherche Nucléaire (CERN)." ([wikipedia](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)). After two years preparation, the first standard was released in 1996. 

The current popular CSS standard is CSS3. It is used for defining visual effects of html documents. It contains:

1. **css** selectors: Vsual effects will be grouped by class names, tag names, id names or even pyseudo element names. It defines namespaces and algorithms to find them. 
2. key-value attributes: including box-model, layouts, colors or any other attributes even dynamic anmiation functions which affects visual effects.
3. media query: targeted on devices type used to expressing html documents, like tv, mobile, screens and their width and height.

It is not a cure to all formatting tasks. Usually, we use it together with javascript, a simple, hash style weak dynamic typed language. But, knowing more about **css** will do you a great favor in diesigning appealing web pages effectively.

With more and more complex pages, like, sing page app entering into people's eyes. Designers find that it is very hard to main **css** files because it is too verbose. **sass/scss** is developed to tackle that problem. The similar tools include **less**. CSS is not designed for programming, while sass/scss is a programming language which compiles to target language **css**. It is a little like [**Flex**](https://github.com/yiakwy/COOL-language-Compiler-Coolc/blob/master/Lexical_Analysis/cool.flex) we usually use for compiler development in C++.

Today most css framework is developed by using sass/scss and less. But to understand the target css well, sometimes, we still need to write css directly, especially for simple ones. In this article, we will start from typical css design components, and then explore some important skills to make it better. It organised as following:

1. navigation: a navigation bar is used for navigation for readers. 
2. sidbar menu: this is intensively used by mobile first design to utilize larger spaces.
3. list: tiny logical coponent in every css components. With aid of "float" attribute, it makes side bar menu and nav into realities.
4. css diary: css design for mark up, which design especially for writing html articles.
5. css animation: a sexy lady in css.
6. bibliography: to maintain **Research Integrity**. It is very very important!!!

## css layout

![css-layout](/images/css-layout.svg)

The picture shows a canonical css layout \(or html layout, but I personally believe that html focuses on logics not visual effects\). In HTML, it might look like:

~~~ html
   <body>
        <div id="wrapper">
            <nav>
                <ul class="navbar">
                    <li><a href="/">Base</a></li>
                    <li><a href="/about.html">About</a></li>
                    <li><a href="/cv">CV</a></li>
                </ul>
            </nav>

            <div class="row">{% raw% } { something } {% endraw %}</div>

            <footer> ... </footer>     
        </div>
   </body>
~~~

I am currently using *rouge* to hight codes above, but in the future I will develop a toolkit to support lineno in pure javascript. **css** grids here refer to *width* and *position* that whehter they are bump to bump or overlapped.

### grids
	
**css** grids system consists of three important attributes: position, display type, width. Every element can be devided into two categroies: **positioned** and **non-positioned**. Non-positioned elements refer to elements with position attribute value equal to either **'relative'**, **'absolute'**, **'fixed'** or **'sticky'**. Since they are positioned, a box model will be attached to them. 

![boxmodel](/images/boxmodel.png)

~~~ css
sample-css {
	position: relative;
	padding-direction: x;
	margin-direction: y;
}
~~~
	
### navigation with sidebar menu \(nav\)
Navigation and footers typically reside in base template pages for template enging to render so that there is no need to wirte them twice anywhere else. To control it, we focus on four attributes:

~~~ css
parent {
	position: it must be positioned property
}

wrapped-ul {
	list-style: usually set to none
}

parent li {
	float: valid or none
}

parent li > a {
	text-decorator: none
}
~~~

Our design is of course dependent on devices. If we want to combine different design together, we need variables to track devices status. Here comes media query part. 

~~~ css
@media device-type and conditions {
	your design here !
}
~~~

Once we have media query, we can have "vertical nav" and "horizontal nav" simutaneously!

1. Vertical Nav: when float set to none
2. Horizontal Nav: when float is everything but none

Horizontal bar wil be easy to deal with. Vertical is much harder. We need animation and movement to implement begin and end postions and their connections kinetic movements. To make possible, in historical approaches, we have two solutions:

1. margin movement with animation (works well with relative positioned elements)
2. postion movements when the parent is absolute positioned.
	
I personally prefer the second plan because I don't need to change parent position style.

### pseudo elements & inhertantce

In HTML standard we have various kinds of elements, pseudo elements refer to elements cannot be manipulated by DOM standard. Pseudo elements can only work on normal elements which have children definition. For example, you must not sepcify them upon "img", "hr" tags and so on. They have two operators

#### pseudo insert
```css
selector:before {
	content: "must valid"
	display: table, block ...
}

selector:after {
	content: "must valid"
	display: table, block ... 	
}
```
The codes above will insert a pseudo element with style specified.

#### pseudo selector
```css
selector::after {
	/* change styles here */
}
```
The codes above will change pseudo elements with style specified. 

```javascript
/* these codes are invalid because pseudo elements can not be manipulated by DOM */
query = "selector::before"
doc = document
pseudo = doc.querySelector(query)
```
The codes above in javascript are invalid.

### css diary
#### auto indexing
#### paragraph optimization
### css animation
### bibliography & latex
#### bibliography
#### latex
### combine them in mark down post
## references
### internet sources \(Retrived on 23th Aug 2017\)

 1. https://www.w3.org/Style/CSS20/history.html
 2. https://en.wikipedia.org/wiki/Cascading_Style_Sheets
 3. https://github.com/mojombo/tpw/blob/master/css/syntax.css
 
### official publications

## thanks to

## one more thing to add ...
...