---
layout: post
title: "Tiny Distributed Tensorflow & OCI-Series2"
date: 2017-05-13
updated: 2017-05-13
reading_expenditure: 10
excerpt_separator: <!--more-->
thumb_img: /images/Kubernetes.png
---

> "We have found having a separate systems for large scale training and small scale deployment leads to significant maintenance burdens and leaky abstraction. ..." -- Jeffrey Dean, Rajat Mongo et al
<!--more-->

<style>
div.post h2 {
  counter-reset: index2 1; }
div.post {
	counter-reset: figures 1;
}

</style>

[上一节](http://yiakwy.github.io/blog/2017/05/06/Tiny-Distributed-Tensorflow-&-OCI-Series1) ...
[下一节](http://yiakwy.github.io/blog/2017/05/06/Tiny-Distributed-Tensorflow-&-OCI-Series3) ...

## Introdcution
### Tensorflow
Google Research in 2015 published a paper ["Large-Scale Machine Learning on Heterogeneous Distributed Systems"](#bibiligraphy). They use stateful data-flow like model to build ML distributed system suitable both on cpu and gpu clusters. The normal "Tensorflow" released publicly refers to [implementation in a single machine](https://en.wikipedia.org/wiki/TensorFlow). Possibly, due to distributed version dependencies on google infrastructure underlines. 

谷歌研究院于2015年发表了论文["Large-Scale Machine Learning on Heterogeneous Distributed Systems"](#bibiligraphy)。 他们采用了“状态数据流”模型去构建分布式的ML系统，使之可以在cpu, gpu等混合硬件设备上的集群运行。通常的开源"tensorflow"实质上指，[单机版本](https://en.wikipedia.org/wiki/TensorFlow)。这很能是因为，论文宣称的分布式实现，是深度依赖谷歌的底层系统的。

In April 2017 \(Dev Tensorflow Summit 2017\), google or Alphabet Group, officially published "distributed tensorflow". We will talk about it later in [Section 4.3, deoply distributed tensorflow in a private cloud](#deploy-tensorflow-clusters-in-a-private-cloud). "Tensorflow/core/distributed_runtime", first released in <span style="text-decoration: underline">*2016 Feb*</span>, quickly graps developers' and researchers' attention. Typically you have three ways to implement distributed tensorflow:

2017年春\(Dev Tensorflow Summit 2017\)，谷歌或者Alphabet集团，正式宣布开源，在2016年2月就发布的分布式版本"Tensorflow/core/distributed_runtime"。我们将在稍后的[4.3小节, 将tensorflow部署到私有云](#deploy-tensorflow-clusters-in-a-private-cloud)。很快开发者和研究者陆续关注了这个版本的发行。一般来说，实施分布式tensorflow有三个途径

![tensorflow-distributed](/images/deploy-tensorflow-in-cloud/tensorflow-distributed.png)

1. grpc for <span style="text-decoration: underline">**data parallel**</span> based on framework <span style="text-decoration: underline">**DistBelief**</span> Google released in 2011, using parameter server interaction
2. model replica with device configuration. Each server has a complete computing graph copy. each computing graph divided into several strong connected components and been distributed into gpu cards in local machine
3. "Tensorflow-Serving", high-level api for users, with streaming and version policy management support. Tensorflow-Serving uses google <span style="text-decoration: underline">*bazel*</span> to build and export distributed ML models. Compared to gRPC version, it requires more memory to build servers.

1. 采用gRPC管理集群，并更多地用于“数据并行”阶段\(服务发送心跳，采集正在处理不同数据的响应服务器，所发回的参数更新值，并将更新好的结果返回work服务器，进行下一次的运算\）。这个工作基于2011年谷歌开展的DistBelief工作，并发表在2012NIPS论文"Large Scale Distribted Deep Networks"
2. 针对局部GPU设备的“模型并行”。每一个服务器都有一个完整计算图拷贝，每个计算图又被划分成为不同的强连通子图，并分发到GPU设备上。
3. 高级抽象的“Tensorflwo-Sering”api接口。此接口支持“流式计算”和“模型版本管理”。构建“Tensorflow-Serving”可以使用Google已经提供的，依赖于Ubuntu, 谷歌开发的构建工具Bazel等镜像的, Dockerfile直接构建； 相比于gRPC版本，构建消耗服务器更多的内存。

![bazel-compelling](/images/deploy-tensorflow-in-cloud/bazel-compelling.png)

Tensorflow implements a core data structure "tensor" to represent multi-demensional data, with precision specified by [IEEE 754 standard memory model](https://www.tensorflow.org/programmers_guide/dims_types). Then it uses computing graph to represent a task lazily executed. 

Tensorflow实现了叫做“tensor”的数据结构来表示，符合IEEE754标准的，多维数据结构。它将用来实现计算图的构建和“延迟计算”功能。

The core algorithms it use are, but not limited to: 

1. Kernel Operation for "tensor" data structure and Lazily execution
	1. Lossy Compression
2. An algorithm for server implements gRPC protocle for between servers communication under [google's cluster manager](#bibliography) 
3. Computing Grpah Optimization
	1. [common subexpression elimination](#bibliography),for edge adjustment and nodes sharing(\we will talk about later in section 3\)
	2. task scheduling: a similar problem we introduced in Chapter Motivation
4. Placement algorithm
	1. simulation stage & devices assignment by greedy heuristic searching\(think about it, nothing other than benchmark testing\)
	2. Computing Directed Weighted Graph Partition and data-flow communication \(we will talk about it later in [Section 3.2](#computing-graph)\)
5. ML optimation engine
	1. Auto differentiation. Auto differentiation can be traced back to 1964, in R. E. WENGERT's paper ["A Simple Automatic Derivative Evaluation Program"](#bibliography). This automates traditional "Backward Propagation" algrithms or equivalently, differential algorithms for system of linear algebra equations.
	2. As we have already expected, most of ML researchers use existing numeric libraries. I will give a brief introduction, and introduce possible opportunies in this field.

Tensorflow使用的核心算法包含，但不限于:

1. tensor基于硬件接口的“核计算”，和“延迟计算”
	1. 精度压缩
2. 实现了gPRC协议的服务器，并由[google's cluster manager](#bibliography)管理调度
3. 计算图优化
	1. [重复计算节点合并](#bibliography)
	2. 任务调度：和我们再上一小节讨论的问题相似
4. 替换算法
	1. 用贪婪启发式算法做设备划分
	2. 有向带权图的划分，和数据流交流算法\(设置新的**发送**，**接受**节点, 我们将在[3.2 小节](#computing-graph)讨论\)
5. ML优化引擎
	1. 自动求导。 自动求导可以追溯到 R.E.WENGERT 在1964年发表的文章["一个简单的自动求导程序"](#bibliography)。这个自动化了“反向传播算法”，或者等价地说，是线性方程组求导算法
	2. 和预想的一样，底层数值代数仍然依赖，传统的实现。我们将简要讨论在这个领域存在的潜在机会。
	

### Docker & OCI
In 2006, Amazon introduced Elastic Compute Cloud \(EC2 Platform\) into public, and EC2 get more and more porpular among industries and academics. EC2 is an implementation of Cloud Computing and [Cloud computing](https://en.wikipedia.org/wiki/Cloud_computing) commonly referring to:

2006年，Amazon推出了“弹性计算云”\(EC2 平台\)给公众。EC2随后越来越获得，企业界和学术界的青睐。EC2实际上是[云计算](https://en.wikipedia.org/wiki/Cloud_computing)的一种实现。通常指：

1. Platform as a service \(PaaS\)
2. Software as a service \(SaaS\)
3. Infrastructure as a service \(IaaS\)

<hr>

1. 平台即服务
2. 软件即服务
3. 基础设施即服务

It is a kind of internet based service designed intentionally for software, devcies, computing and data requested on demand. **Docker** is designed to support PassS, SaaS, and IaaS and shifted to open source in 2013, then later gets popularity in around 2014. Before Docker, we have already had several solutions of virtualization so that complex software or projects build and run dependencies automatically. Engineers just focus on piecies of functionality they provide:

这是一种基于互联网的专门设计的一种服务，旨在使得，软件，设备，计算能力和数据按需发放。**Docker** 被设计来支撑以上服务，并且迅速在2013年开源。在Docker之前，我们已经有了许多种虚拟化技术来，自动地，解决这个复杂的软件，工程构建，运行的依赖问题。从而，工程人员只需要专注他们提供的服务。

VMware and VirtualBox from Oracle are among the first generation of solutions of virtualization. However, Docker are doing better thanks to lightweight architecture and community efforts. 

VMware 和 来自 Oracle的VirtualBox分别是这种虚拟化技术的第一代解决方案之一。但是, 由于更加轻量级的架构和社群的努力，Docker做得更好！

![docker-vmware](/images/Docker-VMwarexml.png)

In [figure](#docker-vmware), the left refers to VMware or VirtualBox from Oracle architecture; while, the right hand side points to Docker architecture. Docker hereby enables fast launching and libraries sharing, with a comparable smaller images for Virtualization Engine, Docker, to execute.

图中，左边是VMware架构，右边是Docker架构。显然，docker使得更加小的镜像，以及依赖共享成为可能。

#### What is OCI?
[OCI](https://www.opencontainers.org/),a project led by Docker and supported by Linux Fundation begining from Jun, 2015, is short for "Open Container Initiative". The initiative defines a run-time environment for a container and image format. Some prototypes of data structures of runtime are implemented in Go language.\(That might be a plausible reason why you should learn "go" in the future, Right?\). The rest specify the configuration for each type OS portability.

[OCI](https://www.opencontainers.org/)是由Docker 2015年6月发起的，并由Linux基金会支持的项目，其全称是 “开放容器建议方案”。该建议方案，定义了容器的“运行时”，和镜像格式. 有些原型使用Go写的（\说不定这就是你以后要学习go的原因吧？\）。其余部分规定了操作系统的兼容定义方式。

OCI servers Container technology standarlization. Docker support Cloud Computing by using <span style="text-decoration: underline">**Docker Swarm**</span> as Orchestration Engine, to manage containers in different servers.

OCI为容器技术标准化服务。Docker为了支持云计算，使用了<span style="text-decoration: underline">**Docker Swarm**</span>作为容器编排引擎，来管理不同服务器节点上的容器。

In a single machine, Docker use <span style="text-decoration: underline">**runc**</span> to execute a container described by its image. In local machine, Docker Engine, including Docker Deamon, manages different container as process without OS cooperation.

在一个单独的机器上，Docker使用了<span style="text-decoration: underline">**runc**</span>来执行启动其镜像所表述的容器。在单机里，Docker Engine，包含了 Docker Deamon等组件，用于管理不同的，相当于进程的容器，而不需要操作系统干预。

Docker swarm is a little bit like <span style="text-decoration: underline">**[Kubernetes](https://kubernetes.io/docs/tutorials/kubernetes-basics/cluster-intro/)**</span> developed by Google. 

Docker swarm 有点像谷歌开发的容器编排系统<span style="text-decoration: underline">**[Kubernetes](https://kubernetes.io/docs/tutorials/kubernetes-basics/cluster-intro/)**</span>。

Kubernetes has already provided a Cloud Based Learning environment, so that beginners be able to get a glimmpse of it immediately!

Kubernetes以及提供了基于云端的学习平台环境，让新人能够快速的了解它！

![Docker-Server](/images/Docker-Server.png)

### Task Specification
The series of articles is self-contained, which means you can get bacground in this article without consulting other papers. Now you have been equiped with basic ideas of distributed tensorflow and OCI standard. We want to identify the task the series work on:

本系列文章是“自包含”，也就是说，不需要借助外部文献，应当就可以了解所需要了解的内容。现在我们已经了解了基本分布式tensorflow，和容器标准生态情况，我们定义本文研究的问题：

1. Deploy Distribted Tensorflow in A Private Cloud using existing tools, especially use docker:
	1. Dockerfile writing or choosing
	2. Bug shooting
	3. Server side and client side configuration
2. Core techniques of tensorflow in a single machine for a minimum tensorflow
3. Core techniques for a minimum distributed tensorflow
4. How make full use of Container Technology?

1. 在私有云上，利用已有工具，特别是Docker，部署分布式的tensorflow
	1. 选择或者撰写Dockerfile
	2. 问题解决
	3. 服务端与客户端的部署
2. 单机上Tensorflow的核新技术，开发一个小型tensorlfow
3. 分布式环境下Tensorflow的核心技术
4. 如何充分使用容器技术？

[上一节](http://yiakwy.github.io/blog/2017/05/06/Tiny-Distributed-Tensorflow-&-OCI-Series1) ...
[下一节](http://yiakwy.github.io/blog/2017/05/06/Tiny-Distributed-Tensorflow-&-OCI-Series3) ...