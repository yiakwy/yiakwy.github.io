---
layout: post
title: "Natual Philosophy of Supervised or Semisupervised Model Generalization"
date: 2017-05-31
updated: 2017-06-01
reading_expenditure: 10
excerpt_separator: <!--more-->
thumb_img: /images/aristotle.png
---

![bayesian-as-graph](/images/VC.png)

## Introduction
Data-Model joint distribution is exactly process that we engineers find a model fitting beyond what we have in sampling data
<!--more-->
“数据-模型”的联合分布，恰恰使我们工程师寻找, 一个不仅仅是, 能够拟合采样数据的模型。

[Figure1](#bayesian-as-graph) shows hwo marginal distribution and joint distribution affected our sampling data and corresponding learned modle. Our first approach is to discuss basis of generalization of a supervised or semisupervised model from bayesian perpectives. The bayesian perpective estimates hwo good a model we should get from a sampled data. Then we dive into a specific approach widely employed by researchers and engineers in daily work \-\- Batched SGD. We uncover the true properties of randomness that weaken our generalization. To this end, we present a future model concept we are working on which might achieves state of the art in the future.

## Basics of generalization of a model along data set
Researchers use "VC demension model" in [Vladimir Vapnik and Alexey Chervonenkis's paper](#bibliography) published in 1971 to describe the relationship between hepothetic function and maximum sampling instances. This is becoming dramatically important especially when we have gorwing number of data. However, the concept of VC demensioni is weakened to some extend by the fact that modern hepothetic function is complex enough to leverage its both variation eror and bias error for extremely large set of data.

研究人员, 使用VC维模型来[1971 两位俄罗斯数学家的样本收敛性研究](#bibliography) 描述“假设函数”和最大采样数据的关系。这个变得越来越重要尤其是我们的数据持续增长。然而, 由于我们的假设函数足够复杂，来均摊variance和bias\(稍后将详细描述这两个概念\)，某种程度上.

Generlaization of a model is so important that we have to be cautious about "data flow process".

![bayesian-formula](/images/formula.gif)

<hr>

模型的泛化能力是如此重要，以至于，搞清我们所处理的采样数据，远远比采用具体的模型，更为重要。

But, we believe that Bayesian Method itself is clear enough to tell us relationship between the learned model from sampling data and sampling space \(All possible data\).

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$ p(model {\text{ }}M = m{\text{ }}|{\text{ }}sampling{\text{ }}dataset{\text{ }}D = d){\text{ }} = {\text{ }}\dfrac{{p(D = d{\text{ }}|{\text{ }}M = m){\text{ }} \cdot {\text{ }}p(M = m{\text{ }}learned{\text{ }}by{\text{ }}all{\text{ }}D){\text{ }}}}{{p(D = d)}} $$
{% endraw %}
</div>

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$ p(M = m{\text{ }}|{\text{ }}D = d) $$
{% endraw %}
</div>

Simplly tell us that given data set D, the possibility that the M assigned to m.

> e.g: we have ten sampling D belongs to {d1, d2, ..., d10}, we got models m1 9 times, m2 1 time. Then 

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$ P(M = m1{\text{ }}|{\text{ }}D = some{\text{ }}d) \approx 1/9 $$
{% endraw %}
</div>

If we already know d2 produced learned model m2 (m2 ≠ m1), we say
<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$ P(M = m1{\text{ }}|{\text{ }}D = some{\text{ }}d2) = 0 $$
$$ P(M = m2{\text{ }}|{\text{ }}D = some{\text{ }}d2) = 1 $$
{% endraw %}
</div>

For The right hand side of the equation, if this is a classification problem, the nominator presents multiplication of correctly detected instance ratio by a model and possibility that is a true model.

If we perform a uniform sampling, the denomitor should always be a constant, which means

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}$$ \max p(m) \propto \dfrac{{P(m|d)}}{{P(d|m)}} $${% endraw %}
</div>

When m is a variable \(we are in the learning process\), the formula above requires us that prediction for the current data set might not **need to be the best** \(a smaller value\). While, when d is a variable, We want P\(m\|d\) or P(d\|m) should not change too large. We call it variance.

Suppose we have two models, an estimated model on dataset d, a true model m<sup>*</sup> we never touched, to measure our estimation m with respect to the sampling dataset D of size N, we have **sampling variance Var(m)** and **sampling error Bias\(m<sup>*</sup>, m\)**. These two concepts already being well documented in a normal statistic textbook [Introduction to Machine Learning](#bibliography).

## Batched sgd & data expansion
The normal process is sampling the best classifier m we computed over a sampled data set. If the variance of parameters of the m is large, we increase sampling size. People usually use bached sgd, if they use gradient descent strategy, making a model touch as large data as possible computationaly cheaper. But this mehthod didn't solve the problem faced when we carry out validation process:

> The variance could be large when feeding different data into a same model

The reason why it has typically good generalization might be the learned model are not the best estimation for each data set as we talked in the last chapter.

## Stacked model and one true model
In industry we can employ "stacked model" to resolve our problems in a more natural manner, while a large group people, believe that if a single deep learning model complex enough, they eventually equivalent to stacked model:

![stack-model](/images/stack-model.png)

> Argument: Unfortunately, "Stacked models" are not equivalent to a single complex model. This argument is true especially when from one selection model like decision tree to another model \(function f1 to function f2\) are not uniform convergent.

Modern model solvers, in optimization theory, tightly dependence on Continuouse Differentiation Assumption. But their "differentiable definition" based on limit theory and **Not Valid For Infinite Value**. In arround 1930, researchers studied on Quantum Theory and Partial Differential Equation, introduced a new concept called "general differentiable" for Heaviside function. In Mathematics and Physics, Heaviside step function which is a difference of absolute value function, could be written in an integral form. In generaly differentiable case, if one can be written in an integral form, we name it generally differentiable\(think about it, an integral should be differentiable right?\). The theory is about density estimation just like what we do in unsupervised learning.

Then reason why mentioned here is , in traditional methodology, to solve an optimization like

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$\min \sum\nolimits_i {|{x_i} - x|} $$ 
{% endraw %}
</div>

Solution is
<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$\min \{ {x_i},local optimal\;{\text{points}}\;searched\;by\;sgd\} $$
{% endraw %}
</div>

These exotic points will be discarded in a large model becuase by no means they become exotic again. If consider in a general differentiable case, I am exited found that they might deeply embeded into an underlying unsupervised learning -- density estimation. They participate in algorithms by no means one phase but multiple phases.

<hr> 

> philosophy behind is: 

## Metrics to measure a model produced by data of randomness 
Randomness is essentially important to success of a model. Suppose we have a query "q", which accepted by a model m, we preform nearest search in dataset space [hashed by its features](http://www.ee.columbia.edu/~wliu/WeiLiu_thesis.pdf), and found that each time we use a model to predict value, they have an error, but the E(e)≠0 > c and Var(e) is large. Noticed that the query is similar, we have following adjugement:

1. Bayesian theroy assumes that we have sampling data from one truely process. The error of model measures randomness. However such randomness might come from different groups of data even though they have similar features.
2. A truely random variable's value cannot be predicted with 100% confidence. That means you might get a very small error but with confidence 0. It does nothing good for your model. This ocurr frequently for complicated data from real world.
3. Gaussian Mixture Model, Quantile Regression, NNS, Density Estimation are among the most commonly used good tools to carry out Randomness research and testing

Usually, a model has a constant called bias which applied to all participated training samplings. Imagine it, that is nothing other than systematic error in physics like instrumental error, feature sampling error in product evironment. But empirical data, systematic error, according to my research in real projects in industry, is not simply a constant but a selection function:

<div class="formula container" style="width: 95%" onload = "UpdateMath(this.value)">
{% raw %}
$$\chi (x \in samping\;space\;U) = \left\{ {{c_i}|x \in {D_i},\;U = \bigcup\limits_i {{X_i}} } \right\}$$
{% endraw %}
</div>

**Step function is not differentiable in common sense!**. For truely random data, we focus on trend with specific confidence. Let me show you a concrete example to illustrate the theory.

> There is a company X. They want to get a model from data collected in different cities to predict how people use their products. 

> They found that, if they analyse in a district level, the result is evident and coinsides with the common sense; if they analyze in a city level, only few cities show significant results; 

> well, if you analyze in street level, the result is unpredictable and of hight variance in cross validation process, even though they could get a very small bias in training dataset because their model is complex enough. 

<div class="panel" style="background-color:green;color:white;">
<i class="fa fa-question-circle-o fa-4" aria-hidden="true"></i> Question, what happened to the data and model?
</div>

In 2014 I wrote a simple data structure called "SeriesNode" in python to tackle above problem raised from an IoT project supported by NTU and government. I was supervised by Professor Teddy from Geogia Tech.

![series](/images/series.png)
![series-details](/images/series2.png)

Here is the minimum version of the codes:

~~~ python
# -*- coding: utf-8 -*-
'''
Created on 3 Nov, 2014
@author: wangyi
'''

from pandas import DataFrame, to_datetime
from core.Scheduler.delta import delta

## ---- Core Methods ----

class Node(object):
    
    def __init__(self, name, data):
        self.name = name
        self.data = data
        
        self.father = None
        self.children = list()
   
    def __str__(self):
        return str(self.data)
   
    def add_child(self, child):
        self.children.append(child)  
    
    def add_children(self, children):
        self.children = self.children.extend(children)
        
    def set_children(self, children):
        self.children = children
    
    def set_father(self, father):
        self.father = father
        father.childer.add_child(self)
        
    def get_children(self):
        for child in self.children:
            print(child)
        return self.children
    
    def get_father(self):
        return self.father

class SeriesNode(Node):
    
    class seriesIterator(object):
        def __init__(self, SeriesNode, start, end, delta):
            self.SeriesNode = SeriesNode
            self.counter = self.__counter__()
            self.start = start
            self.end = end
            self.delta = delta
            
        def __iter__(self):
            return self
        
        def __counter__(self):
            start = self.start
            end   = start + self.delta
            while True:
                if  start >= self.end:
                    break        
                yield (start, end)
                
                start = end
                end   = start + self.delta
        
        def __next__(self):
            try:
                start, end = next(self.counter)
                return (start, end, self.SeriesNode.data[start:end])
            except StopIteration as err:
                raise(err)
    
    def __init__(self, startdatetime, enddatetime, data, type='json'):
        if  type == 'json':
            ## initialization       
            self.data = DataFrame(data)
            ## set index
            self.data.set_index('timestamp_utc', inplace=True)
            ## verbose
            self.data.index = to_datetime(self.data.index.astype(int), unit='s')
                      
        elif type == 'dataframe':
            self.data = data
        
        super(SeriesNode, self).__init__(startdatetime.strftime("%Y%m%d%H%M"), self.data)
            
        self.startdatetime = startdatetime
        self.enddatetime = enddatetime
        self.treeIndex = {'monthly':[], 'weekly':[], 'dayly':[], 'daytime':[], 'nighttime':[], 'hourly':[]} 

    def __iter__(self):
        return self.seriesIterator(self, 
                                   self.startdatetime, 
                                   self.enddatetime, 
                                   self.span) 
               
    def setup(self):        
        self.treeIndex['monthly'].clear()
        self.treeIndex['weekly'].clear()
        self.treeIndex['dayly'].clear()
        self.treeIndex['daytime'].clear()
        self.treeIndex['nighttime'].clear() 
        
        return self
    
        # vertical grouping
    @staticmethod
    def up2down(self, child):
        raise NotImplementedError()
    
    # horizontal groupign
    @staticmethod
    def left2right(self, child):
        raise NotImplementedError() 
    
    def buildtree(self):
        raise NotImplementedError()
    
    def aggregate(self, obj, *callback, **keywords):
        it = self.__iter__()
        #elegant loop
        while True:
            try:
                # get data
                start, end, data = it.__next__()
                # create a child
                child = obj(start, end, data, 'dataframe', self.treeIndex)

                for call in callback:
                    call(self, 
                         child
                         )
                
            except StopIteration as err:
                break        
              
    def statistic(self):
        Peaks = {}        
        means = None
#       stds  = None #standard deviation
        ubds  = None #unbiased deviation
        
        columns = self.data.columns.values
        
        ids = [self.data[col].idxmax() for col in columns]
        Peaks['Max'] = [self.data.loc[ids[i]][col] for i, col in enumerate(columns)]#[self.raw.loc[ids[i]][col] for i, col in enumerate(columns)]
        Peaks['Max_Time'] = [self.data.loc[ids[i]].name for i, col in enumerate(columns)]#[self.raw.loc[ids[i]]['timestamp_utc'] for i, col in enumerate(columns)]

        ids = [self.data[col].idxmin() for col in columns]
        Peaks['Min'] = [self.data.loc[ids[i]][col] for i, col in enumerate(columns)]#[self.raw.loc[ids[i]][col] for i, col in enumerate(columns)]
        Peaks['Min_Time'] = [self.data.loc[ids[i]].name for i, col in enumerate(columns)]#[self.raw.loc[ids[i]]['timestamp_utc'] for i, col in enumerate(columns)]
        
        means = [self.data[column].mean() for column in columns]     
        ubds  = [self.data[column].std() for column in columns]
        
        param = {
                 'peaks':Peaks,
                 'means':means,
                 'ubds' :ubds,
                 }
        
        self.value = means[0]
        self.std = ubds[0]
        self.max = Peaks['Max'][0]
        self.min = Peaks['Min'][0]      
        self.dt_max = Peaks['Max_Time'][0]#datetime.utcfromtimestamp(Peaks['Max_Time'][0])
        self.dt_min = Peaks['Min_Time'][0]#datetime.utcfromtimestamp(Peaks['Min_Time'][0])
        
        return param        

## ---- Aggregation Nodes ----

class Month(SeriesNode):
    span = delta(weeks = 1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Month,self).__init__(startdatetime, enddatetime, data, type=type)
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex 
            
        self.id = self.startdatetime.strftime("%y%m") 
        
    def __str__(self):
        return 'Month ' + self.id + ':'
    
    def buildtree(self):
        self.aggregate(Week, self.up2down, self.left2right)
        
        return self
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        ## up2down
        child.statistic()
        child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(self, child):
        self.treeIndex['weekly'].append(child)        

class Week(SeriesNode):
    span = delta(days=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}): 
        super(Week, self).__init__(startdatetime, enddatetime, data, type=type)
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex
            
        self.id = self.startdatetime.strftime("%y%V")
        
    def __str__(self):
        return 'Week ' + self.id + ':' 
    
    def buildtree(self):
        self.aggregate(Day, self.up2down, self.left2right)
        
        return self    
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        
        ## up2down
        child.statistic()
        child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(self, child):
        self.treeIndex['dayly'].append(child)  
        
class Day(SeriesNode):
    span = delta(hours=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Day, self).__init__(startdatetime, enddatetime, data, type=type) 
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex
            
        self.id = self.startdatetime.strftime("%y%m%d")
            
    def __str__(self):
        return 'Day ' + self.id + ':'
    
    def buildtree(self):
        self.aggregate(Hour, self.up2down, self.left2right)
        
        return self 
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        ## up2down
        child.statistic()
        ## uncomment the following line if it is not leaf ADS
        #child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(self, child):
        self.treeIndex['hourly'].append(child)              

class Hour(SeriesNode):
    span = delta(hours=1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Hour, self).__init__(startdatetime, enddatetime, data, type=type) 
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex
            
        self.id = self.startdatetime.strftime("%y%m%d%H")

    def __str__(self):
        return 'Hour ' + self.id + ':'

## -- extension nodes --
class Weeks(SeriesNode):
    span = delta(weeks = 1)
    
    def __init__(self, startdatetime, enddatetime, data, type='json', treeIndex={}):
        super(Weeks,self).__init__(startdatetime, enddatetime, data, type=type)
        
        if  treeIndex != {}:
            self.treeIndex = treeIndex 
            
        self.id = self.startdatetime.strftime("%y%V") + "-" + self.enddatetime.strftime("%y%V") 
        
    def __str__(self):
        return 'Weeks from ' + self.startdatetime.strftime("%Y%m%d%H%M") + ' to ' + self.enddatetime.strftime("%Y%m%d%H%M") + ":" 
    
    def buildtree(self):
        self.aggregate(Week, self.up2down, self.left2right)
        
        return self
    
    # vertical grouping
    @staticmethod
    def up2down(self, child):
        self.add_child(child)
        ## up2down
        child.statistic()
        child.buildtree()
    
    # horizontal groupign
    @staticmethod
    def left2right(self, child):
        self.treeIndex['weekly'].append(child)     
   
## event trigger function 
        
def onTest(start_date, end_date, series, *args, **keywords):
    print('series-tree test: begin')
    seriesnode = SeriesNode(start_date, end_date, series)
    # test set up
    seriesnode.setup()
    # test statistic
    print(
          str(
              seriesnode.statistic()
              )
          )
    # test build tree for month
    print('\t build hirarchical tree, begin ... ...')
    Month(start_date, end_date, series).setup().buildtree()#.get_children()
    print('\t buld hirarchical tree, end!')

    # test leaf confi
    Day(start_date, end_date, series).setup().buildtree().get_children()
    
    print('series-tree test: End')
~~~

The above programme is actaully a hierarchical. It was initially intentionly designed as a longterm object residence in redis server to provide services of hierarchical query. As illustrated in the above pictures, we found that, data nodes in the bottom of three is of high randomness \(our group collected them from meters purchased from Japan\). After negotiating with the headers from Japan, we realize that the data is not instantaneous data but a data computed using mathematics from sampled data in a delta time.

We also noticed that, at some level, the randomness tend to be eliminated at some tree depth. That means we are always doing Var prediction not Exact Value prediction. Some people challenged the idea by using a black box model for leaf nodes, while use a more explainable model in shallow depth of the data tree. 
 
 
## Mapping Direction -- What if bidirectional mapping?
This is a very important work I am currently working on based on my work in 2014 when I was doing an internship in I2R supervised by Senior Scientist Huang Dongyan. Simply put, typically researchers working on a mapping F from samping space X to target space Y, and use error to supvise learning. We are comparing data in the similar target sampling space.

Should we design a model m1 mapping X to Sapce U, and model m2 mapping Y to space V? We don't requre U, V are from the same samping space. We just require they being of similar demisions and supvise the learning using Correlation. And if m2 is invertible, we can built mapping from X to Y using **m1(m2)<sup>-1</sup>**. Shall we see.

## Bibliography

1. Vapnic, V.N & Chervonenkis, A. Y. (1971), "On the uniform convergence of relative ferequncies of events to their probabilities," Theory of Probability and Its Application XVI(2), 264-280
