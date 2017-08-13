---
layout: post
title: "How does Kubernetes Auth work"
date: 2017-08-11
updated: 2017-08-11
excerpt_separator: <!--more-->
thumb_img: /images/Kubernetes.png
---

## Introduction

Kubenetes lead by google consist of master nodes in server side and clients everywhere else. In cluster, master nodes, run three important processes in individual master node. They are "kube-apiserver", "kube-controller-manager" and "kube-scheduler".  In client side, users are granted commandline tools or construct kubenetes api directly  and kube-proxy will forward requests to remove server as a unique api gateway.
<!--more-->

由谷歌领导，众多厂商参与的kubernetes的集群每一个节点运行着三个重要的进程。 他们是“kube-apiserver”， "kube-controller-manager"，以及"kube-scheduler"。kube-proxy为api入口，将转发请求到对于的集群服务上.

~~~ bash
# how k8s series of projects placed in github
k8s.io
├── api/
│       ...
├── kubernetes/
│   │   ...
│   ├──	pkg
│   │	│   ...
│   │   └── apis
│   │	    ├── abac
│   │	    ├── admission
│   │	    │   ..
│   │	    ├── authentication
│   │	    ├── authorization
│   │	    │   ..
│   │	    ├── certificates
│   │	    │   ...
│   │	    └── policy
│   ├── auth(empty)
│   ├── controller
│   │	│   ...
│   │	└── certificates
│   │       ├── approver
│   │       └── signer
│   ├── plugin
│   │		
│   └── cmd
│   	...
├── apiserver/
│   │   ...
│   └── pkg
│       │   ...
│       ├── authentiation
│       │   └── authenticator 
│       │       └── interfaces.go (token, password, )
│       │       ...
│       └── autherization
│           └── authorizaer
│               └── interfaces.go (attributes)
│               ...
└── client-go/
		...
~~~

The authentciation involved across "kubectl", "kube-proxy" and apiserver. It is centre to build connection among servcies in fast ,safe user experience. Google implement openID to grant limited access from one service to another. More details about openID or oauth is fully discussed in RFC 6749. They takes care of relationships among "resources owner", "authroization server" and "resources server". Instead of using role based authentication control model, google implementes attribute based access control (ABAC) to gain flexible and simplified access management, centralized auditing and access policy.

Authentication鉴权对于建立服务间，快速和安全的是非常重要的。谷歌基于openID实现了服务编排和通信。更多关于oauth1.0和2.0等信息，在RFC 6749里面找到；他们是关于资源拥有者，鉴权服务器，资源服务器三方的关系。谷歌自己实现以套基于abac的鉴权模型，而不是传统的基于角色的鉴权模型，用以获得更加灵活的和简单的访问管理，和中心化的审计，访问策略。

All these perpectives reflect on codes and projects themselves. We will walk though concrete codes and in cloud demos to gain deep understanding of google kubernetes auth for general micorservices architecture.

这些角度都在代码和项目上反应。我们将会分析实际的代码和和在云上的工程来获得关于google kubernetes auth更为深入的理解，并应用它去解决微服务架构的问题。

By tracing api-gateway relevent codes in kubernetes, we obtain clues that how web traffices flowing through servcies. Authentication and anthorization happen inside traffic flow, and we review secrets and abac implementation respectively. We have our tools sharpened first, so that our github page is more friendly:

通过追踪和api-gateway在kubernetes相关的代码，我们获得流量传递的线索。鉴权，就发生在web流量流动的过程中， 然后我们分别审查密匙和abac的代码实现。

1. Introduction
2. Overview of source code structure
3. Review of Microservies Architecture
	1. lyft web evolution theory
4. Request Map
	1. kubectl (L7 Level analysis)
	2. proxy (L4 Level traffic tracing)
	3. apiserver (L7 Level implementation)
	3. Authentication
	4. Authroization
		1. Atrribute Based Access Control
5. Auth UE research
6. Reference

我们首先考虑“请求转发”等apigateway在k8s中涉及的代码，找到流量通过服务流动的线索。鉴权就发生在此过程中；然后我们分别检查密令和abac的实现。 首先更新下我们的代码浏览工具，这样我们的github会更友好：

![ide1.png](/images/kubernetes/ide1.png)

![ide2.png](/images/kubernetes/ide2.png)

Some of key module implementation will be hide in Vendor directory because Kuernetes are maintained by many companies including Redhat, Huawei and so on. If you don't use tool like **souregraph**, you might suffer from doing static analysis.

不少核心代码\(auth\），反向代理会隐藏到Vendor，以及其他在k8s.io旗下的项目里面，如果您没有采纳我的建议，做静态代码分析时候，可能会十分痛苦。

Here I used Sourcegraph. Sourcegraph is a handys static analytic toolkit for navigating through a large project hosted in github. Anlyzing codes can't be easier wit it.

这里我使用了Sourcegrpah这个Chrome插件。它是一个非常容易上手的github代码静态分析工具。拥有它，分析代码不能更简单了。

Favorite skills to finish article reading

1. familar with go and python \(reading tests to see usage case senario\)
2. familiar with SOA or micorservcies architecture
3. familiar L7 web development achitecture
4. basic understanding of L4 socket level usage

## Overview of source code structure

Most functionality of kubenestes written in "pkg", "plugin", "cmd" and "cluster". "cmd" defines a collection of commandline tool in clientside using cobra framework, while "pkg" and "plugin" includes most of authentication logics.

k8s大多数功能，写在"pkg", "plugin", "cmd" 和 "cluster"包下。其中"cmd"是在用户端，采用cobra架构定义了一族，命令行工具。“pkg”和“plugin”包含了大多数的鉴权实现。

## Review of Microservies Architecture

A k8s based microservices architecture:

一个基于kubernetes的微服务架构，根目录包含了以下文件：

~~~ yaml
Dockerfile : defines dependencies a src porject need to build; Kubernetes will build it first then upload it to remote image repositroy. This image will be reused in each cluster node to build distributed services in a cloud envrionment.

development.yaml: create a cluster based services specified in services.yaml. Include replicas, image place and so on.
services.yaml: A single Service instance definition in a k8s pod. Include service label, port, selector for commandline tool and so on.
router.yaml: api gateway; load balancing.
otheres: other valid files accepted by k8s.

src: project inside codes.
third_party: crawler, client or some other things here.
api: expose services to outside
services_entry file: where docker execute the image
~~~

![deployment](/images/kubernetes/deploy.png)

you can mixed them up in a single yaml file followed by executing command to make it in effect:

您可以将这些文件混在一个文件里书写，为了平滑进行版本过渡，我们会维持一个虚拟机池子，动态使用kubectl apply -f 更新池子里的配置文件，并将旧版本从服务中剥离，添加。

~~~ bash
autologin.sh # see kubectl login, and bash interactive automation
kubectl apply -f # make .yaml into effect
~~~

To check your services in cluster local network, run a command like this:

为了在容器上检查服务，你可以执行以下命令：

![check-health](/images/kubernetes/check_health.png)

Additional reading: 

额外阅读：

1. Lyft "envoy"
2. istio
3. ambassador


![why you want to use envoy developed by Lyft](/images/kubernetes/why_envoy.png)

### lyft web evolution theory

This is my study log of Lyfters' speech when I carried out research on Lyft envoy in 2017.

这是我的学习lyft发布会时候的记录：

Before:

![lyft 3 years ago](/images/kubernetes/lyft-3yrsago.png)
![lyft 2 years ago](/images/kubernetes/lyft-2yrsago.png)

After:

![lyft-now](/images/kubernetes/lyft.png)

## Request Map

> Users access api using kubectl by making REST api.

![access control overview from Kubernetes Docs](/images/kubernetes/k8s_oidc_login.svg)

By inspecting imeplementation in apisever, we found that, in kubernetes, objects be authenticated in kubernetes be classified:

通过检查在apiserver上的实现，我们发现，被鉴权的对象分为：

1. user
2. serviceaccount
	1. SystemPriviliegeGroup, master nodes in cluster \(Since it is ABAC based, not role based\)
	2. NodesGroup, nodes
	3. AllUnauthenticated
	4. AllAuthenticated
	5. Anonymous
	6. APIServerUser
	7. KubeProxy
	8. KubeControllerManager
	9. KubeScheduler
	
And we also need find out at which traffic level the authentication happens, L4 or L7? We need trace traffic flow.

Now we are **ready** to explore more about k8s auth! 
我们现在可以探索更多k8s auth了！

### kubectl

When kubernetes set up in server side, for example using "k8s.io/kubernetes/cluster/kube-up.sh", a certificate, key pair *.ca/*.key is generated. User now are able to download the certificate and credentials. Goolge provide users a handy utility to configure clusters by using "gcloud auth login". After successfully logined into gcloud using **Oath2** procdure, user gain full access to gcloud SDK.

Initially, kubernetes should use ${USER}/.kube/config provided by user to set cluster credentials. With gCloud SDK, client can download config file generated by server automatically and connect to them. If you deploy application other than GCE, you might want to refer to this doc [TLS details](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

当Kubernetes在服务器端启动的时候，比如使用了"k8s.io/kubernetes/cluster/kube-up.sh"脚本，一堆证书和口令就会生成。通过使用gCloud SDK "gcloud auth login", 谷歌提供了用户一个非常方便的功能来部署集群。使用Oauth2成功登陆远端后，用户就获得了sdk的完整访问功能。

最开始， kubernetes通过使用用户提供的${USER}/.kube/config 文件来配置集群。但使用了gCloud SDK后，客户端就可以下载服务器自动生成的集群配置文件，和远端连接。如果您是在GCE以外的环境，部署kubernetes，可以参考这篇文档[TLS的详细信息](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/)

> gcloud container clusters get-credentials ...

![fetch credentials from remote cluster](/images/kubernetes/fetch_credentials.png)

By combining cloud administration SDK, with kubernetes, cloud users‘ user experience (UE) is far more better than configuring or downloading cluster credentials manually. 

将云管理界面SDK和kubernetes结合，云用户的远远比手动配置要好。

In this case google is identity provider. The framework also applied to other auth providers like Aure, Amazon EC2 platform. Identity provider provides us with *access_token*, *id_token* and "refresh token". User can also inject id_token in reverse proxy or using kubectl proxy command to visity kubernetes cluster through proxy server. Root Certificate Autherizor\(CA\) validates certificates kubelet or kubectl client certificates to build a connection。

在这个例子，谷歌是身份验证提供者。这个框架同样适用于其他身份提供者比如 Azure, Amazon EC2 平台。身份提供者给我们提供"access_token", "id_token" 和 “refresh_token”。用户还可以将 id_token 加入到反向代理中，或者使用 kubernetes 命令行工具，通过代理服务器访问集群。根证书鉴权验证由kubectl客户端发来的证书，来建立联系。

![k8s_oidc_login](/images/kubernetes/k8s_oidc_login.svg)

A token or JWT token might be look like:
~~~ go
// k8s.io/kubernetes/pkg/kuberctl/serviceaccount/jwt.go
// codes abstraction from k8s developers for analysis, only for education purpose

type jwtTokenGenerator struct {
	privateKey interface{}
}

func (j *jwtTokenGenerator) GenerateToken(serviceAccount v1.ServiceAccount, secret v1.Secret) (string, error) {
	var method jwt.SigningMethod
	switch privateKey := j.privateKey.(type) {
	case *rsa.PrivateKey:
		method = jwt.SigningMethodRS256
	case *ecdsa.PrivateKey:
		switch privateKey.Curve {
		case elliptic.P256():
			method = jwt.SigningMethodES256
		case elliptic.P384():
			method = jwt.SigningMethodES384
		case elliptic.P521():
			method = jwt.SigningMethodES512
		default:
			return "", fmt.Errorf("unknown private key curve, must be 256, 384, or 521")
		}
	default:
		return "", fmt.Errorf("unknown private key type %T, must be *rsa.PrivateKey or *ecdsa.PrivateKey", j.privateKey)
	}

	token := jwt.New(method)

	claims, _ := token.Claims.(jwt.MapClaims)

	// Identify the issuer
	claims[IssuerClaim] = Issuer

	// Username
	claims[SubjectClaim] = apiserverserviceaccount.MakeUsername(serviceAccount.Namespace, serviceAccount.Name)

	// Persist enough structured info for the authenticator to be able to look up the service account and secret
	claims[NamespaceClaim] = serviceAccount.Namespace
	claims[ServiceAccountNameClaim] = serviceAccount.Name
	claims[ServiceAccountUIDClaim] = serviceAccount.UID
	claims[SecretNameClaim] = secret.Name

	// Sign and get the complete encoded token as a string
	return token.SignedString(j.privateKey)
}

~~~

Here is the main associated methods for jwtToken. 

~~~ go

// jwt.go#L117-121
type jwtTokenAuthenticator struct {
	keys   []interface{}
	lookup bool
	getter ServiceAccountTokenGetter
}

// jwt.go#L125-250
// this method relates to token.go, parser.go to get toekn form signed token string
// you also noticed that user info can be extracted from the token
func (j *jwtTokenAuthenticator) AuthenticateToken(token string) (user.Info, bool, error)
{ .. }
	
~~~

According to parser imeplementation, a token in this stage consists of three parts: header\(typically provided in HTTP header Authorization\), **claims** and **signaure**. The signanture part should be similar to package here I developed for authentication purpose. [CLICK HERE FOR DETAILS](https://github.com/yiakwy/Siganture-Authentication-Package/blob/master/api/auth/authentication.py). THE claims including:

根据parser的实现，一个令牌在本阶段，由三部分组成：报文头部\(通常来自http头部Autorization\)，**声明**， 和**签名**。签名部分应该和我之前开发的一个签名工具类似。[点击这里查看详细情况](https://github.com/yiakwy/Siganture-Authentication-Package/blob/master/api/auth/authentication.py)。声明则包含：

1. sub claim
2. namespace claim
3. secretName
4. serviceAccountName
5. serviceAccountUID

Kubectl uses auth provider include Azure defined in "k8s.io/client-go/plugin/pkg/client/auth" module. Here is its specification:

Kubectl使用了包括Azure的鉴权提供者，他们定义在"k8s.io/client-go/plugin/pkg/client/auth"模块中。这里是一些相关的代码声明：

~~~ go
// k8s.io/kubernetes/cmd/kuberctl/app/kubectl.go
// as a tool obey cobra famework, this is the centrl moduel
package app
// most of logics implemented "k8s.io/kubernetes/pkg/kubectl/cmd"
import (
	"os"

	_ "k8s.io/client-go/plugin/pkg/client/auth"         // kubectl auth providers.
	_ "k8s.io/kubernetes/pkg/client/metrics/prometheus" // for client metric registration
	"k8s.io/kubernetes/pkg/kubectl/cmd"
	cmdutil "k8s.io/kubernetes/pkg/kubectl/cmd/util"
	"k8s.io/kubernetes/pkg/util/logs"
	_ "k8s.io/kubernetes/pkg/version/prometheus" // for version metric registration
)
...

// k8s.io/kubernetes/pkg/kubectl/cmd/util
// K8s uses Cobra command line framekwork to develop commandline to face to core utilites

~~~

One thing we need be aware of is that kubenetes auth IS FOR kubernetes account servcie and APPLIATION related screts should be handled in kubernetes based APPLICATION like api-gateway ENVOY.

值得注意的是，kubenetes auth是针对kubernetes账户服务。应用相关的秘令，应当在基于k8s的应用上处理，比如基于k8s的API-GATEWAY ENVOY。

An very important approach in L7 level form client side, is to use the token to construct bearToken authentication for consumers:

客户端有一个重要的方法，来通过构建bearToken请求，来访问集群：

~~~ python
TOKEN = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read()
END_POINT = "https://kubernetes/api/v1/namespaces/default/endpoints/%s" % SERVCIE
// http traffic
req = requests.get(url, headers={"Authorization": "Bearer " + TOKEN}, verify=False)
~~~

### proxy

This is extremely important, that because production is very very complex. You **must** brear it mind to remind yourself what they are doing.

Proxy is a service forward requests from one end point to another endpoint for central audit and simplified implementation.

始终记住自己在做什么非常重要，因为实现非常复杂。 代理是一个将求请，从一个节点发送到另一个节点的服务，这样就可以做集中式审计，并且实现方便。

~~~ go
// Author Lei Wang, created on 11 Aug 2017, All Rights Reserved
// Created on Aug 9 2017
// Last updated on Aug 10  2017

// please refer to
// k8s.io/kubernetes/pkg/proxy/iptables/proxier.go, newest
// k8s.io/kubernetes/pkg/proxy/userspace/proxier.go, old


package proxier

import (
    "fmt"
    "net"
)

// in a real application you might implement several related moduels
// to check, validate, construct IPv4, IPv6, url and binding ascyn loop
// This structure is designed in such way, so that it is the minimum requirements to set up a proxy server or reverse prox server.
// You can distribute codes in different locations like util, pkg/cmd, server and so on so forth. The codes will be quickly poplated from 100 lines to 100000 lines!
type TCPProxier struct {
	// LoadBalancer not implemented yet
	listenIP net.IP // need logics to check loopback address
    hostIP net.IP
}

// each server should already implement loop methods to wait for connection
func NewProxySocket(protocol string, ip net.IP, port int){
	sock, err = net.Listen(protocol, net.JoinHostPort(host, Iota(port))))
	if err != nil {
		return nil, err
	}
	return &sock
}

func (proxier *TCPProxier) addSericeOnPort(protocol string, port int) {
	// k8s will use socket defiend in k8s.io/pkg/proxy/userspace/proxysocket.go
	sock_in, err := NewProxySocket(protocol, proxier.listenIP, port)
	if err != nil {
		CLEAN_UP(sock)
		reutrn nil, err
	}
	// get endpoint from loadBalancer
	// endpoint, err := loadBalancer.Get(strategy)
	endpoint = proxier.hostIP
	// provide loadBlancer if necessary
	sock_out, err = connect_to(protocol, endpoint)
	// all connection will be wrapped in a <ServiceInfo> object in k8s
	go func() {
	// basically the loop implements logics copy data from sock_in to sock_out and verse vera 
		Loop(sock_in, sock_out)
	}
}

// for http proxy, simply use
// in k8s.io/simpage-apiserver you might frequently see codes below
prox:=net.http.httputils.NewSingleHostReverseProxy(targetUrl) for specific targetUrl
// in side proxy server request controller method, simply do
// prox.ServeHTTP(repWriter, req)
~~~

The above exampel in L4 level. Once connection is built, you can CGI related controls to create HTTP requests and response. In go, we just let httpClient to accept the L4 connection

以上是L4级别的。一旦连接建立。我们将使用类似CGI的代码区从IP创建HTTP请求和响应。在GO中，我们通过让一个HTTP客户端程序，接受一个TCP连接来实现。

### apiserver

api server impelments request at L7 level\(i.e. HTTP level, confront with RFC5925 standard which introduces L4 level implementation\) in following steps: 

1) Each time a request comes in, dispatched by a container's HTTPServe "dispatch" method and be routed into specific mehtod in the container; Auth might or might happens here.

应用入口服务器在L7水平\(也就是说HTTP水平上，这和RFC5925标准所对应的L4水平相呼应，读到这里，您应该知道我后面回去分析什么了吧？\)，通过以下步骤实现 request handling：

1) 每次请求来了，我们在容器的路由方法"dispatch"里面，将用由动态绑定容器服务的方法来处理，请求\(至少我写路由，会进行动态绑定\)。这个过程中，Auth可能会，也可能不会发生；
~~~ go

// k8s.io/apiserver/pkg/server/serve.go#L93-148
// codes abstraction from k8s developers for analysis, only for education purpose

func RunServer(server *http.Server, network string, stopCh <-chan struct{}) (int, error) { ... }

// k8s.io/apiserver/pkg/server/handler.go#L129-162
// codes abstraction from k8s developers for analysis, only for education purpose

// The server uses go http.Server, here is the apiHandler which implements
// Handler interface. Hence here is the entrance where codes business logics happens. Lei commented on Aug 12 2017. The http Server setup as a HTTP2 connection and is used by a TCP connection.
func (d director) ServeHTTP(w http.ResponseWriter, req *http.Request) {...}


// k8s.io/apiserver/vendor/github.com/emicklei/go-restful/container.go#L203-279
// codes abstraction from k8s developers for analysis, only for education purpose

func (c *Container) dispatch(httpWriter http.ResponseWriter, httpRequest *http.Request) {
···
	func() {
		c.webServicesLock.RLock()
		defer c.webServicesLock.RUnlock()
		webService, route, err = c.router.SelectRoute(
			c.webServices,
			httpRequest)
	}()
...
	if len(c.containerFilters)+len(webService.filters)+len(route.Filters) > 0 {
		// compose filter chain
		allFilters := []FilterFunction{}
		allFilters = append(allFilters, c.containerFilters...)
		allFilters = append(allFilters, webService.filters...)
		allFilters = append(allFilters, route.Filters...)
		chain := FilterChain{Filters: allFilters, Target: func(req *Request, resp *Response) {
			// handle request by route after passing all filters
			route.Function(wrappedRequest, wrappedResponse)
		}}
		chain.ProcessFilter(wrappedRequest, wrappedResponse)
	} else {
		// no filters, handle request by route
		route.Function(wrappedRequest, wrappedResponse)
	}
}
~~~

Here curlyRouter gives definition of Router. It is necessary to discuss it becasue services determined by a compound score computed over a pathToken list. Filter is used to choose correct path to route, where is authentciation happens. Let see codes:

这里Router是由curlyRouter定义的。讨论它的实现是非常必要的，因为k8s是通过计算服务路径上的每个节点的分数，来选取最匹配的服务. 过滤器会选择，合适的路径，这就是auth发生的时刻。让我们来看一组方法：

~~~ go
// k8s.io/apiserver/vendor/github.com/emicklei/go-restful/curly.go#L19-44
// codes abstraction from k8s developers for analysis, only for education purpose

func (c CurlyRouter) SelectRoute(
	webServices []*WebService,
	httpRequest *http.Request) (selectedService *WebService, selected *Route, err error) { ... }


// k8s.io/apiserver/vendor/github.com/emicklei/go-restful/curly.go#L47-57
// codes abstraction from k8s developers for analysis, only for education purpose

// Note that requestTokens should be named pathTokens. In a matter of fact, the token should be short yet unique. Because it has no relationship with Auth. Unique hash method is good for it. I am goint to summit a PR to moidify it. Lei commented on Aug 12 2017.
func (c CurlyRouter) selectRoutes(ws *WebService, requestTokens []string) sortableCurlyRoutes { ... }


// k8s.io/apiserver/vendor/github.com/emicklei/go-restful/curly.go#L47-57
// codes abstraction from k8s developers for analysis, only for education purpose

// pathTokens = strings.Split(strings.Trim(httpRequest.URL.Path, "/"), "/"), don't confuse with auth token which parsed from http bodies or headers!
func (c CurlyRouter) computeWebserviceScore(requestTokens []string, tokens []string) (bool, int) { .. }
~~~

These methods tell us how a request is determined. Morover, ernestmicklei has blog about go REST details and [design philosophy](http://ernestmicklei.com/2012/11/go-restful-api-design/).

selectRouters will use Filter to get correct path to compute scores and in apiserver, authentication is implemente as a filter:

~~~ go
// k8s.io/apiserver/pkg/endpoints/filters/authentication.go#L54-83
// codes abstraction from k8s developers for analysis, only for education purpose

func WithAuthentication(handler http.Handler, mapper genericapirequest.RequestContextMapper, auth authenticator.Request, failed http.Handler) http.Handler { 
...
// Heihei, we found it!!!
user, ok, err := auth.AuthenticateRequest(req)
...
}


// k8s.io/apiserver/pkg/endpoints/filters/authorization.go#L32-62
// codes abstraction from k8s developers for analysis, only for education purpose
func WithAuthorization(handler http.Handler, requestContextMapper request.RequestContextMapper, a authorizer.Authorizer, s runtime.NegotiatedSerializer) http.Handler {
...
// haha, ABAC test, we got it!!!
authorized, reason, err := a.Authorize(attributes)
...
}
~~~

2) Each time a request dispatched, we retrieve request conext \(very simple, a hashmap\), and update request context with the current request. Conext will used by apiserver and third party auditing. Other context servcies conprise of Prometheus Monitoring services. Requests will be monitored by Prometheus Monitoring services, -- a quite famouse third party project. And they are also grouped into two generes: resoured and non-resourced. It is easy to understand in on openID conext:

2) 每次请求被路由了，我们提取访问上下文，其实就是一个hashmap，并将本次请求添加到hashmap中。上下文会被应用入口服务器和第三方的审计系统使用。其他上下文服务，还包括了，普罗米修斯监控系统。请求都会普罗米修斯监控，一个非常著名的项目；还被分成两大类：资源请求，非资源请求。这比较容易在openID上下文下理解：

> Valid authenticated tokens reqired when request forwared to resources server! 当请求路由到资源服务器时候，就需要授权令牌。

It is strange that apiserver didn't implement a generic router in sperated module. I am going to sumit a request to rewrite codes about it. 

A typical go request handler being of function signautre as

~~~ go
import (
	"net/http"
)

// you also define functional pointer type. Like C, go is very behavior oriented.
func WhateverResourceHandler(w http.ResponseWriter, req *http.Request){ ... }
~~~

3) Now a requesnt enter into a handler. Handler Check meida type from request info first. This is a standard procedure in HTML5 context. I have a post about it before, you might want to check it for the details. Sometimes the server might need to negotiate with client about content type. It frequent happens for RESTful api in a browser environment. 

3) 现在请求进入了一个处理流程。处理流程会首先从请求读取响应类型。这在HTML5是一个标准过程。我之前有一篇相关的文章，有详细信息。有时候，服务器需要和客户端进行“谈判”来确认最终的响应类型。这对浏览器环境下的RESTful api非常常见。

### Authentication

Different types of authentication implemented in apiserver.authentication.request in L7 level. Here is a example for bearToekn authentication:

不同的鉴权策略，在apiserer.authentication.reuqesat模块中实现。下面是一个令牌请求的例子：

~~~ go
// k8s.io/apiserver/pkg/authentication/request/bearertoken/bearertoken.go#L38-58
// from kubernetes developers, only education purpose

func (a *Authenticator) AuthenticateRequest(req *http.Request) (user.Info, bool, error) {
	auth := strings.TrimSpace(req.Header.Get("Authorization"))
	if auth == "" {
		return nil, false, nil
	}
	parts := strings.Split(auth, " ")
	if len(parts) < 2 || strings.ToLower(parts[0]) != "bearer" {
		return nil, false, nil
	}

	token := parts[1]

	// Empty bearer tokens aren't valid
	if len(token) == 0 {
		return nil, false, nil
	}

	user, ok, err := a.auth.AuthenticateToken(token)
	// if we authenticated successfully, go ahead and remove the bearer token so that no one
	// is ever tempted to use it inside of the API server
	if ok {
		req.Header.Del("Authorization")
	}

	// If the token authenticator didn't error, provide a default error
	if !ok && err == nil {
		err = invalidToken
	}

	return user, ok, err
}

// k8s.io/apiserver/pkg/authentication/request/headerreqeust/requestheader.go#L38-58
// from kubernetes developers, only education purpose

func (a *requestHeaderAuthRequestHandler) AuthenticateRequest(req *http.Request) (user.Info, bool, error) {
	name := headerValue(req.Header, a.nameHeaders)
	if len(name) == 0 {
		return nil, false, nil
	}
	groups := allHeaderValues(req.Header, a.groupHeaders)
	extra := newExtra(req.Header, a.extraHeaderPrefixes)

	// clear headers used for authentication
	for _, headerName := range a.nameHeaders {
		req.Header.Del(headerName)
	}
	for _, headerName := range a.groupHeaders {
		req.Header.Del(headerName)
	}
	for k := range extra {
		for _, prefix := range a.extraHeaderPrefixes {
			req.Header.Del(prefix + k)
		}
	}

	return &user.DefaultInfo{
		Name:   name,
		Groups: groups,
		Extra:  extra,
	}, true, nil
}

// k8s.io/apiserver/pkg/authentication/request/x509/x509.go#L60-92
// from kubernetes developers, only for education purpose

// AuthenticateRequest authenticates the request using presented client certificates
func (a *Authenticator) AuthenticateRequest(req *http.Request) (user.Info, bool, error) {
	if req.TLS == nil || len(req.TLS.PeerCertificates) == 0 {
		return nil, false, nil
	}

	// Use intermediates, if provided
	optsCopy := a.opts
	if optsCopy.Intermediates == nil && len(req.TLS.PeerCertificates) > 1 {
		optsCopy.Intermediates = x509.NewCertPool()
		for _, intermediate := range req.TLS.PeerCertificates[1:] {
			optsCopy.Intermediates.AddCert(intermediate)
		}
	}

	chains, err := req.TLS.PeerCertificates[0].Verify(optsCopy)
	if err != nil {
		return nil, false, err
	}

	var errlist []error
	for _, chain := range chains {
		user, ok, err := a.user.User(chain)
		if err != nil {
			errlist = append(errlist, err)
			continue
		}

		if ok {
			return user, ok, err
		}
	}
	return nil, false, utilerrors.NewAggregate(errlist)
}
~~~

Authenticateion implementation introduces ["x509"](https://en.wikipedia.org/wiki/X.509), bearer token, anonymous, headerreqeust and websocket.

鉴权包含x509, 令牌请求，匿名请求，http头请求, 和基于证书的websocket。

### Authorization

#### Atrribute Based Access Control

This originally not a CS terminology and originates from Enterprice Management. Let 's see two examples from National Institute of Standards and Technology \(NIST\):

Linda and its teamates want to access some projects after assigned to appropiate roles and groups:

ABAC原本不是CS的术语，它起源于企业管理。让我们看两个来自“美国国家标准技术局”例子：

Linda和团队成员，变更了角色和组信息后，想获取对应项目权限：

![Role Based Access Control, from NIST](/images/kubernetes/RBAC.png)

When projects and team members grow, a very complicate network produced eventually. Well in ABAC, we create some policy agents to inspect employ's attributes not people them self to issue access or deny, a nice relationship management network is asscoated:

当项目和成员变大的时候，就会收敛到一个非常复杂的管理网络。这是传统的RABC管理方式。在ABAC中，我们会创建“策略”组，检查每个雇员的属性，而不是雇员人；并根据属性得分批准或拒绝。这样会收敛到一个非常漂亮的管理网络。

![ABAC, from NIST](/images/kubernetes/ABAC.png)

So the core aprt of ABAC are **policies** and **attributes**. The most part of policies specified in "k8s.io/kubernetes/pkg/auth/authorizer/abac/abac.go" and "k8s.io/apiserver/pkg/authorization/authorizer/interfaces.go"

~~~ go
// k8s.io/kubernetes/pkg/apis/abac/v0/types.go
// from kubernetes developers, only education purpose


// Multiple verison defined here: v0, v1beta1
type Policy struct {
	metav1.TypeMeta `json:",inline"`

	// User is the username this rule applies to.
	// Either user or group is required to match the request.
	// "*" matches all users.
	// +optional
	User string `json:"user,omitempty"`

	// Group is the group this rule applies to.
	// Either user or group is required to match the request.
	// "*" matches all groups.
	// +optional
	Group string `json:"group,omitempty"`

	// Readonly matches readonly requests when true, and all requests when false
	// +optional
	Readonly bool `json:"readonly,omitempty"`

	// Resource is the name of a resource
	// "*" matches all resources
	// +optional
	Resource string `json:"resource,omitempty"`

	// Namespace is the name of a namespace
	// "*" matches all namespaces (including unnamespaced requests)
	// +optional
	Namespace string `json:"namespace,omitempty"`
}


// k8s.io/kubernetes/pkg/auth/authorizer/abac.go#L116-129
// from kubernetes developers, only education purpose

// Here is a typical c++ onsite project
// We first load policies from files, then then do matches as callee

func matches(p api.Policy, a authorizer.Attributes) bool {
	if subjectMatches(p, a) {
		if verbMatches(p, a) {
			// Resource and non-resource requests are mutually exclusive, at most one will match a policy
			if resourceMatches(p, a) {
				return true
			}
			if nonResourceMatches(p, a) {
				return true
			}
		}
	}
	return false
}
~~~

这些policy由kubeapiserver的config.go动态加载到服务器里面。配置文件大致长这个样子：

~~~ json
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user":"bob",       "namespace": "projectCaribou", "resource": "*",         "apiGroup": "*", "readonly": true }}
~~~

#### Other control scheme

When kubenetes server setup, there are up to 5 choices besides ABAC to choose from:

在k8s master节点启动后，除了ABAC共有5个鉴权选项：

1. Node Access Control
2. AlwaysAllow
3. AlwaysDeny
4. [WebHook](https://kubernetes.io/docs/admin/authorization/webhook/): An HTTP post based callback when some even triggered. This is used in Kubernetes to query an outsite REST to determine user privileges.
5. RBAC

Enabling ABAC and WebHook modes are required for authorization process. 只有ABAC, Webhook是必须的。

## Conclusion

Kubernetes impelements its auth mostly in L7 level routing process. While throtling, IP whitelist and ip router can be done in L4 level. In future， we might be able enhance it in L4 level.

Kubernetes在L7路由上实现了它的鉴权流程。同时呢，流量控制，IP白名单，IP路由还可以在L4水平做。未来，我们在L4水平上进行加强。

## Acknowledgement

Thanks to Senior Engieer from Huawei， also previous engieers in RedHat, Ning Jiang , through the process we disscuss a lot of questions together. Without him, I might not be in the endeavour to finish the task. Thanks to him again

感谢来自华为的高级工程师，之前也是红帽子的工程师，姜宁。工程中，我们讨论了很多问题。没有他，我就没有动力完成这个工作。再次感谢。

Lei @ Peking, 12 Aug 2017

## references
1. https://www.youtube.com/watch?v=cgTa7YnGfHA by National Institute of Standards and Technology
2. https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/
3. ABAC, Wikipedia, https://www.axiomatics.com/attribute-based-access-control/

X. Pending ... I will add additional literatures later to maintain research complete. But this will take me some time to do it but if I refer to someone's work, I certainly mentioned them in my articles. The current Bibparse system not finished yet and I have to manually add them. This article is my origianl work. You should not cite it without my concent or authorizaiton in any form inlcude but not limited to SNS posts, papers, publication of codes. ALL Rights Reversed by Lei.
