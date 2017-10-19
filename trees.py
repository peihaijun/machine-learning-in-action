# coding: utf-8
from math import log
import time

import operator


def jishiqi(func):
    def jishi(*args,**kwargs):
        time0=time.time()
        back=func(*args,**kwargs)
        return back,time.time()-time0
    return jishi

# @jishiqi
def calcShannonEnt(dataSet):
#计算信息熵函数，信息熵越高的话，则混合的数据越多
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1#注意这里不能缩进到if下，否则不会把同类型的标签进行累加
    shannonEnt=0.0
    for key in labelCounts:
        # print key
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)#这里是不是有问题，香农熵计算公式应该是每个信息熵乘以自己的概率来进行计算吧
        # shannonEnt=shannonEnt-prob*log(prob,2)
    return shannonEnt

def creatDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels




def spiltDataSet(dataSet,axis,value):#带划分的数据集，划分数据集的特征，特征的返回值
    #干嘛的？？？
    #按照给定的特征来划分数据
    reDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]#axis始终是零，这一步就是置空操作？
            reducedFeatVec.extend(featVec[axis+1:])
            reDataSet.append(reducedFeatVec)
    return reDataSet



def chooseBestFeatureTopSplit(dataSet):
    #选择最好的数据集进行划分
    numFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)#这是最初时候的香农熵，
    bestInfoGain=0.0;bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]#将数据集的某一列的所有数据送个这个列表
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=spiltDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)#之前在调试的时候，加入了计时器返回成一个列表，所以这里计算时会出现类型错误无法进行计算
        infoGain=baseEntropy-newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature



def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),
                            key=operator.itemgetter(1),reverse=True)
    #True是降序排列，key=operator.itemgetter(1)选用列表的第二位来进行排序
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    #创建决策树代码
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureTopSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    mytree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        mytree[bestFeatLabel][value]=createTree(spiltDataSet(dataSet,bestFeat,value),subLabels)

    return mytree





# # yun xing
mydata,mylabels=creatDataSet()
# print mydata,mylabels
# mydata[0][-1]='maybe'
# result=calcShannonEnt(mydata)
# result=spiltDataSet(mydata,0,1)
result=chooseBestFeatureTopSplit(mydata)
print result



