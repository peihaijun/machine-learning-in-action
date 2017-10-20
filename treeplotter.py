# coding: utf-8
import matplotlib.pyplot as plt
import time

def jishiqi(func):
    def jishi(*args,**kwargs):
        time0=time.time()
        back=func(*args,**kwargs)
        return back,time.time()-time0
    return jishi

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[
                    key]).__name__ == 'dict':  #
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

#计算树的层数
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[
                    key]).__name__ == 'dict':  #判断是不是字典
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def shendu(mytree):
    jian=mytree.keys()[0]
    i=0
    if  type(mytree[jian]).__name__=='dict':
        i+=1
        xintree=mytree[jian]
        # xinjianlength=len(xintree.keys())
        for n in xintree.keys():
            if type(xintree[n]).__name__=='dict':
                i=i+shendu(xintree[n])

    return i
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

#绘制树图形，myTree树的字典，parentPt父节点，nodeTxt节点的文字标注
def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)  #树叶节点数
    depth = getTreeDepth(myTree)#树的层数
    firstStr = myTree.keys()[0]  #节点标签
    #计算当前节点的位置
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)#在父节点间填充文本信息
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[
                    key]).__name__ == 'dict':  #判断是不是字典
            plotTree(secondDict[key], cntrPt, str(key))  #递归绘制树形图
        else:  # 如果是叶节点
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


# 创建绘图区
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


# def createPlot():
#    fig = plt.figure(1, facecolor='white')
#    fig.clf()
#    createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
#    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
#    plt.show()

def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                   ]
    return listOfTrees[i]

# createPlot(thisTree)
# # coding: utf-8
# import  matplotlib.pyplot as plt
# decisionNode=dict(boxstyle="sawtooth",fc="0.8")#定义判断节点形态
# leafNode=dict(boxstyle="round4",fc="0.8")#定义叶节点形态
# arrow_args=dict(arrowstyle="<-")#定义箭头
# #绘制带箭头的注解
# #nodeTxt：节点的文字标注，centerPt：节点中心位置
# #parentPt：箭头起点位置（上一节点的位置），nodeType：节点属性
# def plotNode(nodeTxt,centerPt,parentPt,nodeType):
#     createPlot.ax1.annotate(nodeTxt,xy=parentPt,
#                             xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',
#                             va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)
# def createPlot(inTree):
#     fig=plt.figure(1,facecolor='white')
#     fig.clf()
#     axprops=dict(xtixks=[],yticks=[])
#     createPlot.ax1 = plt.subplot(111)#, frameon=False, **axprops
#     # createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
#     plotTree.totalW=float(getNumLeafs(inTree))
#     plotTree.totalD=float(getTreeDepth(inTree))
#     plotTree.xOff=-0.5/plotTree.totalW;plotTree.yOff=1.0;
#     # plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
#     # plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
#     plotTree(inTree,(0.5,1.0),'')
#     plt.show()
# #计算叶节点数
# def getNumLeafs(mytree):
#     numLeafs=0
#     firstStr=mytree.keys()[0]
#     secondDict=mytree[firstStr]
#     for key in secondDict.keys():
#         if type(secondDict[key]).__name__=='dict':#是否是字典
#             numLeafs+=getNumLeafs(secondDict[key])#递归调用getNumLeafs
#         else: numLeafs+=1#如果是叶节点，则节点加1
#     return numLeafs
# # createPlot()
# #计算树的层数
# def getTreeDepth(mytree):
#     maxDepth=0
#     firstStr=mytree.keys()[0]
#     secondDict=mytree[firstStr]
#     for key in secondDict.keys():
#         if type(secondDict[key]).__name__=='dict':#是否是字典
#             thisDepth=1+getTreeDepth(secondDict[key])#如果是字典，则层数加1再递归调用getTreeDepth
#         else: thisDepth=1
#         #得到最大层数
#         if thisDepth>maxDepth:maxDepth=thisDepth
#     return maxDepth
# def retrieveTree(i):
#     listOfTrees=[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
#                  {'no surfacing': {0: 'no', 1: {'flippers': {0:{'head':{ 0: 'no', 1: 'yes'}},1:'no'}}}}
#                  ]
#     return  listOfTrees[i]
#
#
# def plotMidText(cntrPt,parentPt,txtString):
#     xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
#     yMid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
#     createPlot().ax1.text(xMid,yMid,txtString)
#
#
# def plotTree(mytree,parentPt,nodeTxt):
#     numLeafs=getNumLeafs(mytree)
#     depth=getTreeDepth(mytree)
#     firstStr=mytree.keys()[0]
#     cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
#     # cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalw,plotTree.yOff)
#     plotMidText(cntrPt,parentPt,nodeTxt)
#     plotNode(firstStr,cntrPt,parentPt,decisionNode)
#     secondDict=mytree[firstStr]
#     plotTree().yOff=plotTree().yOff-1.0/plotTree.totalD
#     for key in secondDict.keys():
#         if type(secondDict[key]).__name__=='dict':
#             plotTree(secondDict[key],cntrPt,str(key))
#         else:
#             plotTree().xOff=plotTree().xOff+1.0/plotTree.totalw
#             plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
#             plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
#         plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD
#
mytree=retrieveTree(1)
# # print result
# mytree=retrieveTree(1)
# print getTreeDepth(mytree)
shendu=jishiqi(shendu)
print shendu(mytree)
#问题：函数添加装饰器后，函数的返回会变成一个元组，这样的话，就无法进行原来的计算了？？？？？

# print getNumLeafs(mytree)
# createPlot(mytree)
