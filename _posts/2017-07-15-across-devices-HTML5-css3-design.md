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
	2. message queue based event driven implemantion
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

HTML5中定义了事件模型[Event](https://www.w3.org/TR/uievents/), 以及出发和绑定方法。一个事件绑定后\(.addEventListener方法\)，就可以在您想要触发的元素上调用dispatchEvent方法了。因为涉及非阻塞状态，从内核的角度，看成是一个IO多路复用的特例。这里是模仿一个传统的，来自[深入理解操作系统]\(\)的C IO多路复用的写法：

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

In this programme, we first start a daemon after peer threads pool ready for use and block the master until user trigger some commands to start looping. To safely run it, we wrap the codes in context manager so that whatever exception will be handled by it. The inner ioLoop will check whether there is a event registered by users and fire it. A worker will put the results generated into an output shared queue for other main process to use\(calling join method in a query\).

在这个程序中，我们首先开始在线程池准备好后，运行一个分离后的线程。该背景线程，或者服务，会一直阻塞，直到用户触发命令，释放startloop锁。为了安全地运行，我们将他放在一个上下文管理器Cursor()方法里面\(这样做，是考虑到, 我们在审查oracle客户端代码时发现，在实现 mysql PEP标准时，cursor会缓存一个可以写的数据缓存，这样，客户端‘写’就不线程安全了)\。内部的ioLoop循环，会不断查询是否有事件产生，并运行它。子线程，会不断地将生产的结果放在共享结果队列里面，以方便主执行流，可以获取。比方说，在主执行流程里面的query方法里面，执行join，并将结果读出。

### back to css3, canvas and WebGL

Understanding event loop is critical to your performance of your web app and understand how this affect your design. Considering a simple dynamic background video I am developing with four statuses:

![headline_collapsed_background-iPhone](/images/website_design/headline_collapsed_background-iPhone.png)

![headline_background-iPhone](/images/website_design/headline_background-iPhone.png)

![headline_rotate_background-iPhone](/images/website_design/headline_rotate_background-iPhone.png)

![cover_pc](/images/website_design/cover_pc.png)

To facilitate hardware acelerating, we developed animation using css on purpose. 

### UI deisgn pattern, Visual, effects and targets

## Bibliography





