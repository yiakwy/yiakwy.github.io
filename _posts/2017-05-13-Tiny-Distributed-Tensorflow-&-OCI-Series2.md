---
layout: post
title: "Tiny Distributed Tensorflow & OCI-Series2"
date: 2017-05-13
updated: 2017-05-13
reading_expenditure: 10
excerpt_separator: <!--more-->
thumb_img: /images/devices.png
---

> "We have found having a separate systems for large scale training and small scale deployment leads to significant maintenance burdens and leaky abstraction. ... -- Jeffrey Dean, Rajat Mongo et al"
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
Google Research in 2015 publish a paper ["Large-Scale Machine Learning on Heterogeneous Distributed Systems"](#bibiligraphy). They use stateful data-flow like model to build ML distributed system suitable both on cpu and gpu clusters. The normal "Tensorflow" released publicly refers to [implementation in a single machine](https://en.wikipedia.org/wiki/TensorFlow). Possibly, due to distributed version dependencies on google infrastructure underlines. 

In April 2017 \(Dev Tensorflow Summit 2017\), google or Alphabet Group, officially published "distributed tensorflow". We will talk about it later in [Section 4.3, deoply distributed tensorflow in a private cloud](#deploy-tensorflow-clusters-in-a-private-cloud). "Tensorflow/core/distributed_runtime", first released in 2016 Feb, quickly graps developers' and researchers' attention. Typically you have tow choices to implement distributed tensorflow:

![tensorflow-distributed](/images/deploy-tensorflow-in-cloud/tensorflow-distributed.png)

1. grpc for <span style="text-decoration: underline">**data parallel**</span> based on framework <span style="text-decoration: underline">**DistBelief**</span> Google released in 2011, using parameter server interaction
2. model replica with device configuration. Each server has a complete computing graph copy. each computing graph divided into several strong connected components and been distributed into gpu cards in local machine
3. "Tensorflow-Serving", high-level api for users, for streaming and version policy management support. Tensorflow-Serving uses google <span style="text-decoration: underline">*bazel*</span> to build and export distributed ML models. Compared to gRPC version, it requires more memory to build servers.

![bazel-compelling](/images/deploy-tensorflow-in-cloud/bazel-compelling.png)

Tensorflow implements a core data structure "tensor" to represent multi-demensional data, with decision specified by [IEEE 754 standard memory model](https://www.tensorflow.org/programmers_guide/dims_types). 




