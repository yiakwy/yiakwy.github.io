---
layout: post
title: "The Essence of Designing Css in Personal Website"
date: 2017-04-15
reading_expenditure: 6
---

> Beauty is simple and beauty is in mind

## Introduction 
Technology www helps people to connect with each other. Knowledge produced nowadays dramatically increase and shared among people. 

Being able to write an article and sharing your poin of views among peers will be very important to build your intellectual Personality. But wait, are you crazy on articles formats, pictures and visual effects? I am going to share you with some simple techniques where you can apply to your personal blogs. Moreover, if you go through my github pages, you might found, writing css is not too hard for to accomplish.

## How does it work?
The most important thing about articles is content. In content centralised media era, we will stick to the content of which the structure is carefully organized. But to digest it thoroughly, we need formats to express it. Formats in this article is implemented using *css* or *sass*. They, however, are not a panacea to all conent expressing prblems.

To make full use of it, we need have basic study on structure of conents. Conent has a topic or headline, which will be explained in serveral subtopics. They come either externally or interally. For example:

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

It is not a cure to all formatting tasks. Usually, we use it together with javascript, a simple, hash style weak dynamic typed language. But, know more about **css** will do you a great favor in diesigning a appealing web pages effectively.

With more and more complex pages, like, sing page app entering into people's eyes. Designers find that it is very hard to main **css** files because it is too verbose. **sass/scss** is developed to tackle that problem. The similar tools include **less**. CSS is not designed for programming, while sass/scss is a programming language which compiles to target language **css**. It is a little like [**Flex**](https://github.com/yiakwy/COOL-language-Compiler-Coolc/blob/master/Lexical_Analysis/cool.flex) we usually use for compiler development in C++.

Today most css framework is developed by using sass/scss and less. But to understand the target css well, sometimes, we still need to write css directly, especially for simple ones. In this article, we will start from typical css design components, and then explore some important skills to make it better. It organised as following:

1. navigation: a navigation bar is used for navigation for readers. Navigation and footers typically reside in base template pages for template enging to render so that there is no need to wirte them twise else anywhere.

## css layout
### navigation \(nav\)
### sidebar menu
### panel
### list
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
 
### official publications

## thanks to

## one more thing to add ...
...