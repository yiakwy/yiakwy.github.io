---
layout: post
title: "Across devices HTML5-CSS3 design"
date: 2017-07-15
updated: 2017-07-15
reading_expenditure: 10
excerpt_separator: <!--more-->
thumb_img: /images/html5css3.png
---

> 通过一个周末的努力，利用移动设备连接到主机上进行dom测试，比较容易地发现了几个在移动端出现的错误，并成功地修复。这是一次宝贵的经验。
<!--more-->

## Introduction

In the last post [the essence of designing css in personal website](/blog/2017/04/15/css-design-essence), we have discussed how to create a styled website to support content from scrach. That is relatively of high level of abstraction. This article, instead, takes care of implementation in details, especially for acrosss devices development. You are free to choose between webpack+ES6+ReactNative technology tool chain, and other technique like, vue.js+coffeScript\|TypeScript or even widely supported pure javascript based on ES6 standard as your first baby step. The real issues are in problems domain. You can either be a problem expert or a tool chain master, like seinor or even principle X language programmer. I perfer you to think in the perspecive of the second career choice.  

在上一篇文章[the essence of designing css in personal website](/blog/2017/04/15/css-design-essence)中，我们已经讨论了如何从无到有地，根据内容创建格式化的网页。相对来说，它是高度抽象的。本文，恰恰相反，着重具体的细节，尤其是跨设备的开发细节。你可以使用webpack+ES6+ReactNative工具链，也可以使用vue.js+coffeScript\|TypeScript甚至，原生的，目前最广泛支持的ES5标准的javascript。因为真正的问题是，实在解决方案领域里面。你可以选择成为，一个问题专家，也可以选择成为一个工具链的大师，某种语言的高级工程师，甚至首席工程师。但是我更喜欢，站在第二种职业选择的角度。

Before you read the the following conents, I strongly recommend you to wander around "HTML5 Rocks", which maintained by google fellows like Eric Bidelman, Paul Irish et al. It is officaly supported by Google. They have a post about [how HTML5 rendering engines work](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork/). It is about baiscialy context grammer of DOM in BNF, \(recall we use Recursively Decent to parse it in university, right?\). Howerver, this actually not the only stage for our browser. Our browser we in netio module will extract mimetype, to decide which how to deal with the contents. That is becuase HTML5 is not only about markup language parsing and layout, i.e. semantic-level specification and semantic-level scripting API, but also a media expression.

在您开始阅读之前，我希望能够浏览下“HTML5 Rocks”。 它是由谷歌官方支持，并由谷歌开发者维护的专业技术博客。比较有名的人物有Eric Bidelman, Paul Irish等人。他们有一篇比较有名的文章，是关于浏览器如何工作的[how HTML5 rendering engines work](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork/)\(回顾下，我们再大学就是用BNF形式进行递归下降解析的，对吧？\)。但事实上，这不是我们浏览器，做的唯一的事情。在netIO模块，我会读取，相应的消息提取mimetype, content-length用来决定，采用什么解码方式应对。这是因为HTML5不仅仅是关于标签语言的解析和布局，比如语义层面的声明，语义层面的脚步API，还是媒体资源的表达。

If the content is complex enough, server might decide to use multipart mimetype to transfer contents.
