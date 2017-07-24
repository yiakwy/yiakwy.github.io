---
layout: post
title: "Across devices HTML5-CSS3 design"
date: 2017-07-20
updated: 2017-07-24
reading_expenditure: 10
excerpt_separator: <!--more-->
thumb_img: /images/html5css3.png
---

> 通过一个周末的努力，利用移动设备连接到主机上进行dom测试，比较容易地发现了几个在移动端出现的错误，并成功地修复。这是一次宝贵的经验。
<!--more-->

## Introduction

In the last post [the essence of designing css in personal website](/blog/2017/04/15/css-design-essence), we have discussed how to create a styled website to support content expressing from scrach. That is relatively of high level of abstraction. This article, instead, takes care of implementation in details, especially for acrosss devices development. 

You are free to choose between webpack+ES6+ReactNative technology tool chain, and other technique like, vue.js+coffeScript\|TypeScript or even widely supported pure javascript based on ES6 standard as your first baby step. The real issues, however, resides in problems domain. You can a tool chain master, like seinor or even principle X language programmer. Or alternatively, as a even better choice, to be a domain knowledge expert.  

在上一篇文章[the essence of designing css in personal website](/blog/2017/04/15/css-design-essence)中，我们已经讨论了如何从无到有地，根据内容创建格式化的网页。相对来说，它是高度抽象的。本文，恰恰相反，着重具体的细节，尤其是跨设备的开发细节。你可以使用webpack+ES6+ReactNative工具链，也可以使用vue.js+coffeScript\|TypeScript甚至，原生的，目前最广泛支持的ES5标准的javascript。因为真正的问题是，实在解决方案领域里面。你可以选择成为，选择成为一个工具链的大师，某种语言的高级工程师，甚至首席工程师。或者从另一个角度，成为问题专家。

Before you read the the following conents, I strongly recommend you to wander around "HTML5 Rocks", which maintained by google fellows like Eric Bidelman, Paul Irish et al. It is officialy supported by Google. They have a post about [how HTML5 rendering engines work](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork/). It is fundamentaly important decribing context free grammer of DOM in BNF and attributed rendering flow, \(recall that in university we use Recursively Decent to parse context free gramma, right?\). Howerver, these actually not the only things determined by our browser. Our browser will extract mimetype in netio module, to decide how to deal with the contents. That is becuase HTML5 is not only about markup language parsing and layout, i.e. semantic-level specification and semantic-level scripting API, but also a media expression.

在您开始阅读之前，我希望能够浏览下“HTML5 Rocks”。 它是由谷歌官方支持，并由谷歌开发者维护的专业技术博客。比较有名的人物有Eric Bidelman, Paul Irish等人。他们有一篇比较有名的文章，是关于浏览器如何工作的[how HTML5 rendering engines work](https://www.html5rocks.com/en/tutorials/internals/howbrowserswork/)\(回顾下，我们在大学就进行递归下降解析的上下文无关的语法，对吧？\)。但事实上，这不是我们浏览器，做的唯一的事情。在netIO模块，客户端程序会读取请求消息的mimetype, content-length用来决定，采用什么解码方式应对。这是因为HTML5不仅仅是关于标签语言的解析和布局，比如语义层面的声明，语义层面的脚本API，还是媒体资源的表达方式。

If the content is complex enough, servers might decide to receive multipart mimetype for exchanging contents. If that happens, we need to implement a "multipart" content structure for different midia in client side. A client side might verify the mimetype sent by server like movie and audio.

Each html element obeys event driven UI programing model. And Each frame in browser will check whether there is a certain event matched then fire it. For example, a media element like "xhr" will use onreadystatechange as a callback to monitor readystate status. Concretely, Travis Leithead \(Microsoft\) together with Gary Kacmarcik \(Google\) published HTML UI Events draft in 04 Aug 2016, to extend their work on Dom Events released in 2015. They defined life circle as event specification, dispatch methods and executing order in a tree traverse when acesters have registered a same event, 

如果内容足够复杂，服务器，会决定接受multipart的媒体类型，用于交换数据. 如果这发生了，我们还会在客户端针对不同媒体实现multipart内容结构。相反，客户端也，可以验证服务器发送的媒体资源是有效的。每一个HTML元素遵循事件驱动U的I编程模型, 每一帧渲染都会检查是否有事件触发。比如，媒体资源都会想xhr一样通过onreadystatechange来检查readystate的编码并执行相关代码。由来自微软Travis Leithead \(Microsoft\)和谷歌的Gary Kacmarcik \(Google\)编辑的[UI Events](https://www.w3.org/TR/uievents/)是关于Dom Events的一个扩展，详细解释了Event的声明，dispatch，listen以及remove的生命周期。在一些特殊的场景下，如果祖先元素也注册相同的事件，还会涉及事件执行顺序问题。

This article described a typical UI programming model then discuss problems running javascripts in diffent devices. Issues include media acessibility, style sepcification and coding. Coding aspect is what we just mentioned about Event driven model and how different version of browsers support programming features. By utilizing proper tools, we are able to adjust them in a early statge

本文首先大致刻画下，一个UI编程架构的模型，并然后讨论其在不同设备上运行javascript的问题。这种问题包含三个层面，媒体资源支持，样式层面和代码层面。代码层面，就是我们刚刚提到的事件驱动模型，以及浏览器不同版本对于编程脚本的支持程度。通过利用合适的测试工具，我们就能够将上述问题，及早发现，并作出调整。

1. Client side UI programming Model Intro
	1. A simple C IO handler for kernel to process: event driven
	2. message queue based event driven implementaion
	3. back to css3, canvas and WebGL
	4. UI deisgn pattern, Visual, effects and targets
2. Event Supported across devices
	1. click, hover
	2. load, onreadystate
	3. touch, rotate
	4. mediaPlayer
3. Deveoper references
	1. tempalte rendering engine
	2. es6 gramma and asynchronous programming
	3. ES widget
		1. jquery style widget \& compatibility
		2. ES6 webpack widget \& testing environment construction

## Client side UI programming Model Intro

UI in HTML is part of Human Computer Interaction\(HCI\) because HTML constrains how human interact with computers. Back to years before 1964, personal computers can only react to "keyboard" events because, mouse has not been invented and various researches focus on this part, like keyboard design in Statisitcal Journals. Then, later Dr. Douglas Engelbart\(https://en.wikipedia.org/wiki/Douglas_Engelbart\) invented the mouse when he was a member of Stanford Research Insititute\(https://en.wikipedia.org/wiki/Computer_mouse\) in 1968. Then mouse then later began to be commercialized in Apple PC. 

The influence upon us is that, our interaction events are expanded to "click", "mouse over", "mouse leave", etc. Now in mobile first era, we have a new understanding of HCI, a natural way for human to interact with computer. These devices include but not limited to "multi touch screen", "logitech optical camera", and "mechanical traking system", which widely used in mobile, research and movie industries. 

UI在HTML里面，是人机交互的一部分\(HCI\) 因为 HTML 限制了人与电脑的交互。回到1964年前，个人电脑，或者民用电脑仅针对键盘事件响应，是因为鼠标还没有被发明 ，并且各种研究人员注意力还在键盘上，比如统计报刊关于键盘布局的文章。然后，Douglas Engelbart博士 \( https://en.wikipedia.org/wiki/Douglas_Engelbart \)在他还是斯坦福研究院成员的时候，在1968年，发明了民用鼠标，并迅速被苹果公司商业化。

对于我们的影响，就是，交互事件被扩展到了，“点击”，“鼠标掠过”，“鼠标离去”等等。现在，移动第一的时代，我们有了全新的HCI定义，用人类自然的方式和机器交互。这些设备包含, 不限于，“多控点触摸屏幕”， “logitech光学照相机”，“机械跟踪设备”。他们广泛地应用在，手机，科研，以及电影工业。因此，我们在设计一个基于UI事件驱动的过程中，我们需要仔细考虑。

### A simple C IO handler for kernel to process using select and message queue based implementation

HTML5 defines [Event model](https://www.w3.org/TR/uievents/), and how they bind to elements. Once you use method "addEventListener", you can call dispatchEvent method upon the element you want. Since it deals with blocking status in kernel side, a multiplexing IO technique could be applied. Here is the codes mimicking tradition multiplexing IO from textbook [Computer Systems: A Programmer's Perpective, 3rd Edition](#bibliography)

HTML5中定义了事件模型[Event](https://www.w3.org/TR/uievents/), 以及出发和绑定方法。一个事件绑定后\(.addEventListener方法\)，就可以在您想要触发的元素上调用dispatchEvent方法了。因为涉及非阻塞状态，从内核的角度，看成是一个IO多路复用的特例。这里是模仿一个传统的，来自[深入理解操作系统](#bibliography)的C IO多路复用的写法:

~~~ c++
//
//  select.cpp
//  SimpleHTTPServer
//
//  Created by Wang Yi on 20/7/17, updated on 24/7/17, mimick codes developed by Randal E. Bryant and David R. O'Hallaron in their book "Computer System: A programmers' perspective, 3rd Edition" published in 2016. This book describe OS in latest x86 archtecutre
//  Copyright © 2017 Wang Lei. All rights reserved.
//

#include "select.hpp" 
int select_server(int argc, char **argv)
{
    fd_set fd_pool, ready_set;
    struct sockaddr_storage client_addr;
    int max_conn;
    init_fdPool(&fd_pool);
    while (1) {
        ready_set = fd_pool;
        int ready_evt = select(max_conn, &ready_set, nullptr, nullptr, nullptr);
        struct Event* ets = get_evt(&ready_set);
        struct Event* curr = ets;
        while (curr != nullptr) {
            curr->handler(); curr++;
        }
    }
    
    return 1;
}
~~~

我们可以清楚地看到，在程序的18行的时候，程序会发生阻塞等待一个事件触发；对于UI程序，会有一个默认的"draw"每一帧都会触发, 以免程序阻塞。这里Event会维持一个文件或者事件描述符动态查询表。现代的设计中，往往会专门使用一个**消息队列**，或者**消息服务器**，或者第三方**消息服务**来进行事件的注册，查询，解绑操作。

Message queue based is a little bit complicated but basically they are the same. Instead of using "select" to check whether buffer is ready from kernel, we use a thread safe queue shared by peer threads and detach them from the main executing flow. Here is an [example](https://github.com/yiakwy/DBManagement/blob/master/src/core/DAO/Database.py) I wrote several years ago: 

~~~ python
# -*- coding: utf-8 -*-
'''
Created on 20 Oct, 2014
@author: wangyi
'''

# -- sys --
import contextlib
import queue
import re
import sys
import threading

...
# the basic database is used for querying or non-transaction based database interacting
# the database alwasy returns Json style data in python             
class Database(Connector): 
    
    def __init__(self, **config):
        super(Database, self).__init__(**config)
        
        self._input = queue.Queue()
        self._output = queue.Queue()
## -- interface for user --    
    def query(self, sql, *args, **hint):
        
        self.basic(sql, self.onQuery, *args, **hint)

        list = []
        while True:
            try:
                list.append( self._output.get(block=False) )
            except queue.Empty:
                break
        
        if   list.__len__() == 1:
            return list[0]
        elif True:
            return list         
    
    def insert(self, sql, *args, **hint):
        if  hint != {}:
            # db sharding mode 
            try:        
                status = self.query(self.sqlMapping['query']['_?_table'], hint['db'], hint['table'])
                    
                if  not status:
                    self.onAlter(hint['create'], hint['table']) 
            except Exception as e:
                pass   
         
        self.basic(sql, self.onAlter, *args, **hint)

class DataNode(Database, threading.Thread):

    def __init__(self, **config):
        Database.__init__(self, **config)
        
        self.config = config
        
        threading.Thread.__init__(self)     

        self.stoprequest = threading.Event()
        self.startloop = threading.Event()
        self.conlock = threading.Condition()
        
        self.cursor_setup = False
        self.cursor_close = True
        
        self.input_status = True
        self.daemon = True
        self.cursor = None
        
        self.counter= 0
       
        self.start()

...

    def ioLoop(self):
                
        while not self.stoprequest.isSet():
            try:
                # sql event loop
                job = self._input.get(True, 0.05)
                # callback
                self.execl(job)
                
            except queue.Empty:
                continue
            except mysql.connector.Error as err:
                self.input_status = False
                self.stoprequest.set()
                print( 'runtime error ' + self.name + ' : ' + err.__str__() )
                raise mysql.connector.Error('master capture an err event:' + err )

    def run(self):
        
        while True:
            # wait for signal to start task-querying loop
            self.startloop.wait()
            
            with self.Cursor(): # open cursor management
                # sql event loop
                self.ioLoop()
~~~

![web-workers_from Erin Swenson-Healey's article in 2013](/images/web-workers.png)

In this programme, we first start a daemon after peer threads pool ready for use and block the master until user trigger some commands to start looping. To safely run it, we wrap the codes in context manager so that whatever exception will be handled by it. The inner ioLoop will check whether there is a event registered by users and fire it. A worker will put the results generated into an shared queue for read by other threads executing flow\(calling join method in a query\).

在这个程序中，我们首先开始在线程池准备好后，运行一个分离后的线程。该背景线程，或者服务，会一直阻塞，直到用户触发命令，释放startloop锁。为了安全地运行，我们将他放在一个上下文管理器Cursor()方法里面\(这样做，是考虑到, 我们在审查oracle客户端代码时发现，在实现 mysql PEP标准时，cursor会缓存一个可以写的数据缓存，这样，客户端‘写’就不线程安全了\)。内部的ioLoop循环，会不断查询是否有事件产生，并运行它。子线程，会不断地将生产的结果放在共享结果队列里面，以方便主执行流，可以获取。比方说，在其他指令CPU流水线里面的query方法里面，执行join，并将结果读出。

Understanding event loop is critical to your performance of your web app and affect your design. Considering a simple dynamic background video I am developing with four statuses:

理解事件循环，对于网站的性能是十分重要的， 并影响你的设计。 考虑下面一个我们正在设计的动态视频背景：

![headline_collapsed_background-iPhone](/images/website_design/headline_collapsed_background-iPhone.png)

![headline_background-iPhone](/images/website_design/headline_background-iPhone.png)

![headline_rotate_background-iPhone](/images/website_design/headline_rotate_background-iPhone.png)

![cover_pc](/images/website_design/cover_pc.png)

They respond to different events: rotate, compress，mobile, pc. And the most important of all, suppose we want to **modfiy css using javascript**, we have to monitor "onreadystate" event because dom attributes vary while loading, rendering. Taditional ways to deal with it, are:

它对应着四个事件：旋转，压缩，移动，PC. 最重要的是，如果我们想通过JS修改CSS的话，我们需要监控"onreadystate"事件，因为dom属性会随着，加载，渲染变化。我们传统有三种处理方式：

1. setTimeout, not robust when codes grow, not easy to debug
2. load event, this works for listener binding but not effectively for css adjsuting.
3. listen to onreadystate and check **readyState** value. This is robust. 

I recommend to use the third method, because , that sometimes, it takes long time before dom rendering finished. To make procedure smooth, we need call rendering method per frame. 

我推荐使用第三种方式，因为，有时候，dom需要很长时间才能完成渲染。未来让这个过程更加光滑，我需要在每一帧上渲染。

### back to css3, canvas and WebGL

To facilitate hardware acelerating, we develop animation procedures using css on purpose. As for canvas and GL, a typical GL programme, after perspective projection\(glMatrixMode(GL_PROJECTION), glPerspective(mtx)\), global camera\(glLookAt(mtx)\) set up, we push motion matrix calc by scale, rotation, translation parameters into matrix stack, before we draw connected components together. But primitive graphics with textures by 3d reconstruction algorithms like B-Spine curve gen is not enough for a real world application. We build 3d world using [scene graph](https://webglfundamentals.org/webgl/lessons/webgl-scene-graph.html). There are two ways to define a scene graph:

为了利用硬件加速，我们通常有意识地使用css来完成动画。对于canvas和GL来说，一个典型的GL程序，在设置完投影视角\(glMatrixMode(GL_PROJECTION), glPerspective(mtx)\)，全局照相机视点\(glLookAt(mtx)\)，我们就将通过参数计算出来的，刚性运动矩阵，压入矩阵栈中, 然后画连通图形。但是仅仅是有着纹理的图形还是不够的。我们实际上使用[scene graph](https://webglfundamentals.org/webgl/lessons/webgl-scene-graph.html)来构建应用

1. explicitly build a tree 
2. implicitly using a configure file, like xml or json, which widely used in productive env. 

By using gl scene grpah, we can build stuning, heavy interactive web application. We will build a **articles gallery**, 3d tag cloud and timeline later as vivid examples to show how 3d interactive mode affacts our UI appearance. 

通过使用，gl scene graph，我们就可以构建一个令人震惊的，重交互的网络应用。我们稍后，会在个人网站上构建**文章长廊**， **3d 标签云**和时间轴，作为真实的例子展示3d交互模式，是如何改变我们的UI的。

Instead of using as graphics container, canvas can also be used as a movie player to run in background no matter what devices you are using. 

除了作为图形的容器外，canvas还可以当做2d的背景播放器使用。不管您使用什么设备，都可以在背景处悄无声息的运行。

~~~ javascript
	// On every time update draws frame
	this.video.addEventListener('timeupdate', cvpHandlers.videoTimeUpdateHandler = function() {
		self.drawFrame();
		if (self.options.timelineSelector) {
			self.updateTimeline();
		}
	});
	
	CanvasVideoPlayer.prototype.drawFrame = function() {
		this.ctx.drawImage(this.video, 0, 0, this.width, this.height);
	};
~~~

This is tremendous!

css3 material design is one way comes 3d design. We add support for material design proposed by creating "material-sim.css" recently. css3 uses Key frames algorithms developed in Digital Movie industry in around 1980 when Pixal founded. We recommend you to use "cubic-bezier" named by French Engineer Pierre Bezier. This kind of curves will envolved into B-Spines curves which palys a great important role in 3D reconstruction. We record the curve a timming function. You might have already used it without notification, say Windows Office pen curves. To implement it, we use dvide and conque strategy:

这非常棒!

css3材料设计是和3d结合的一种方式。我们最近增加了材料设计的支持。css3使用在数字电影工业界发展的 Key-Frame 技术来渲染动画。那个时候，1980年，Pixar也成立了。它整个数字动画产业有着不可估量的影响。我推荐你们使用由法国工程师Pierre Bezier命名的"cubic-bezeier"来计量css。这种曲线最后发展成为B-Spines曲线。我们用它作为计时器。您可能已经用过它，但却从来都没有注意到：比方说windows Office的钢笔曲线。未来实施它，我们采用了divide & conque的策略。

~~~ c
//============================================================
void plotBezier(Point2d* bez, int deg)
{
	// TODO:  add your own codes 
	// project tempalte created in Aug 2009 by NTU, filled by Lei(lwang019@e.ntu.edu.sg) as part of requirements of the project
	double height = maxDistance(bez, deg);

	if(height < tessEps){
		glColor3f(0, 0, 0);
		glBegin(GL_LINES);
		glVertex2f(bez[0].x, bez[0].y);
		glVertex2f(bez[deg].x, bez[deg].y);
		glEnd();
	}
	else{
		Point2d *leftBez,*rightBez;

		leftBez = (Point2d*)malloc( (deg + 1) * sizeof(Point2d) );
		rightBez = (Point2d*)malloc( (deg + 1) * sizeof(Point2d) );
		midSubdivide(bez, leftBez, rightBez, deg);
		plotBezier(leftBez, deg);
		plotBezier(rightBez, deg);

		free(leftBez);
		free(rightBez);
		leftBez = NULL;
		rightBez = NULL;
	}
}
~~~

### UI deisgn pattern: Visual, effectiveness and targets

![pixar-studio](/images/pixar.png)

The theory partly comes from animation. For a simple webUI design, we don't need to design a storyboard but some concepts are still important!

1. Visual: cold vs warm, determined by our theme
2. effectiveness: is the design really reflecting what our requirements are
3  targets: How people feel or use it in an end point

理论部分来自于动画理论。对于一个简单的webUI设计，我们不需要故事板，但是有些概念还是重要的：

1. 视觉：冷色调 vs 暖色调，由主题决定
2. 有效性: 该设计是否反映了，我们的需求？
3. 目标：终端用户如何感知该设计

## Event Supported across devices

This part centers arround heterogenous design problems and how to deal with them. 

这部分将详细讲述，几个事件，在各种设备上的异同以及处理办法
### click, hover

<div style="overflow:auto">
<table>
  <thead>
    <tr>
      <th style="text-align: center">device</th>
      <th style="text-align: right">click</th>
      <th style="text-align: right">hover</th>
      <th style="text-align: right">replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center">browser</td>
      <td style="text-align: right">supported</td>
      <td style="text-align: right">supported</td>
      <td style="text-align: right">&nbsp;</td>
    </tr>
    <tr>
      <td style="text-align: center">ios, safari</td>
      <td style="text-align: right">supported</td>
      <td style="text-align: right">not supported</td>
      <td style="text-align: right">focus, touch</td>
    </tr>
  </tbody>
</table>
</div>

one listen to click event. Alternatively, css "focus" and "active" and mimic the "click" effects. Due to lack of mouse like interactive tool, there is no hover defined for mobile. The side effect is that we have to define multiple actions to cover undescribed behavior.

click, 可以通过Javascrip来监听，也可以通过css的 focus和active来模拟。由于移动设备，没有鼠标这种形式的交互，并没有hover效果，和对应的Mouse over事件等。因此在移动端，我们需要进行多重定义，来覆盖不被支持的效果：

~~~ css
.leave, 
div.post section>ol>li:not(:hover) ol, div.post section>ol>li:not(:focus) ol,
div.post section>ul>li:not(:hover) ul, div.post section>ul>li:not(:focus) ul {
	opacity: 0.3;
	max-height: 0;
	visibility: hidden;
	/*transform: translateX(130%);*/
	transform: scale3d(0);
  	transition: all 1.2s ease;
	background: inherit;
	color: inherit;
}

.touch,
div.post section>ol>li:hover ol, div.post section>ol>li:focus,
div.post section>ul>li:hover ul, div.post section>ul>li:focus {
	opacity: 1;
	max-height: 1000px;
	visibility: visible;
	transform: scale3d(110%);
	transition: all 1.8s ease;
	background: lightgrey;
	color: black;
}
~~~

A alias will be used to mark events transfering in case of use.

我们会用一个别名，去标记它，这是因为，未来我们可能会用javascript来标记这些状态转移。

### load, onreadystate

Load event happens when dom semantic node constructed. For example, you inspecting "offsetHeight" or "offsetTop", you might end up with different values. Sometimes they change fast but sometimes not. If the process is slow, we have wrap codes in onreadystate event to check whether they are ready.

load是文档被解析后，加入到dom树的事件标志，此时它并不一定渲染完成。比如如果您监控offsetHeight, offsetTop并输出日志，您会发现，他们在改变；只不过有时候快，有时候慢。我们通常用这个来绑定一些监听事件。如果他们过慢改变，我们就需要进一步绑定onreadystate，并检查状态变量是否准备就绪：

~~~ javascript
var adjustStyle = function() {
	var self = this
	if (doc.readyState === 'complete') {
		adjustMovieStyle()
	} else {
		doc.onreadystatechange = function () {
			if (self.doc.readyState === "interactive" ) {
				self.adjustMovieStyle()
			} else 
			if (self.doc.readyState === "complete" ) {
				self.adjustMovieStyle()
			}
		}
	}
}
doc.addEventListener("DOMContentLoaded", adjustStyle, false)
~~~

### touch, rotate

"touch" and "rotate" are central to mobile first application. Boris Sums has a wonderful [post]((https://www.html5rocks.com/en/mobile/touch/)) about it. I will focus on rotate event instead. The codes might look like:

touch, rotate是移动专属事件。touch是唯一可以模仿鼠标设备的事件。Boris Smus有一篇非常棒的关于[touch事件的文章](https://www.html5rocks.com/en/mobile/touch/)。我会详细讨论下rotate事件。Rotate事件，可以通过监控“orientationchange”和window.orientation触发，代码，大概长这个样子：

~~~ javascript
window.addEventListener("orientationchange", function(){
	switch(window.orientation) {
		case 270 || -270:
		case 90 || -90:
		// do something
		break
		case 0:
		// do something else
	}
}, false)
~~~

Transition is added for event status transfering.

执行事件状态转移时，我们当然需要加下过渡：

~~~ css
.kls {
	transition: 0.6s;
	-webkit-transform: translateZ(0);
	transform: translate3d(0,0,0);
	-webkit-transform: translate3d(0,0,0);
}
~~~



### mediaPlayer

HTMl5 supports audio and video. But that is not enough. Once html5 video loaded into page, if "mute" option set to be false, an audio tag will be inserted into page before video tag. They obeys media api protocol:

HTML5是支持视觉和音频的。但是，实际工作告诉我们，这远远不够。一旦html5 video, 被载入，如果mute设置为false，浏览器会在video前面插入一个audio标签用来播放声音。他们遵循一个共同的多媒体协议接口：

~~~ javascript
/* please refer to this report, thanks for his or her efforts */
/* https://gist.github.com/ufologist/50b4f2768126089c3e11 */
function audioPlayer() {
	var doc = document,
		audio = doc.querySelector("audio")

	var self = this
	self.audio = audio
	function forceSafariPlayAudio() {
		audio.load(); // iOS 9   还需要额外的 load 一下, 否则直接 play 无效
		audio.play(); // iOS 7/8 仅需要 play 一下
	}

	function log(info) {
		console.log(info)
	}

	audio.addEventListener('loadstart', function() {
		log('loadstart');
	}, false);
	audio.addEventListener('loadeddata', function() {
		log('loadeddata');
	}, false);
	audio.addEventListener('loadedmetadata', function() {
		log('loadedmetadata');
	}, false);
	audio.addEventListener('canplay', function() {
		log('canplay');
	}, false);
	audio.addEventListener('play', function() {
		log('play');
		// remove event handler
		window.removeEventListener('touchstart', forceSafariPlayAudio, false);
	}, false);
	audio.addEventListener('playing', function() {
		log('playing');
	}, false);
	audio.addEventListener('pause', function() {
		log('pause');
	}, false);

	// mimick event due to safari ios developer policy
	window.addEventListener('touchstart', forceSafariPlayAudio, false);
	var videoSource = doc.querySelector("video > source")
	if (wechat_re.test(navigator.userAgent) && 
	   $.fn.jsInj.prototype.isMobile()) {

	} else {
		// audio.src = videoSource.src
	}
}
~~~

load event tells browsers that we can download the media and decode it. Once "canplay" event ready, we can play medias. Here are three things we should at least consider：

1. play media, should we replace them in a new container
2. Overlay: parent node sytle like "z-index", "background-color" place no impact upon mdeia elements. We can only affect media elements overlay attributes through sibling elements
3. dynamic size

load函数告诉浏览器，可以下载相应的资源，并根据媒体类型进行解码。一旦"canplay"时间触发，就可以执行play操作，进行播放了。至少有三件事我们需要考虑：

1. 播放资源，有无必要替换，比如之前提到的canvas代替video
2. OverLay，其父元素的背景设置，和z-index设置，对video无效。只能通过兄弟节点的背景涉及来进行层次覆盖。
3. 动态大小

## Deveoper references

Pending

## Bibliography

Pending




