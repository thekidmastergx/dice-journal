from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

#Helper Functions
def paramChecker(funcName,types,params):
    paramTypes = [type(i) for i in params]
    testResults = [(expected == actual) for expected,actual in zip(types,paramTypes)]
    tuples = zip(types,paramTypes,testResults)
    argIdx = 0;
    for typeName, paramType, correctType in tuples:
        if not correctType:
            raise TypeError("{0}.args({1}): {2} != {3}".format(funcName,argIdx,typeName,paramType))
        argIdx += 1

def prod(l1,l2):
    paramChecker("prod",[list,list],[l1,l2])
    paramChecker("prod2",[list,list],[l1[0],l2[0]])
    l3 = []
    for i in l1:
        for j in l2:
            l3.append(i+j)
    return l3

#Dice Rolling Function
def d(num,faces,mod=0,drop=0,__prop__ = False):
    paramChecker("d",[int,int,int,int,bool],[num,faces,mod,drop,__prop__])
    if num < 1 or faces < 1 or drop < 0 or num <= drop : return
    if num > 1:
        s = prod(d(num-1,faces,__prop__=True),[[i+1] for i in range(faces)])
    else:
        s = [[i+1] for i in range(faces)]
    if __prop__:
        return s
    for _ in range(drop):
        for i in s:
            i.remove(min(i))
    ds = []
    for i in s:
        ds.append(sum(i) + mod)
    return ds

#Graphing Functions
def xaxis_assist(freqTable):
    xlow = min(np.amin(freqTable[:,0]),1)-1
    xhigh = max(np.amax(freqTable[:,0]),-1)+1
    plt.xlim(xlow,xhigh)
    if xhigh-xlow > 25:
        plt.xticks(np.arange(xlow,xhigh+1,(xhigh-xlow+1)/10))
    else:
        plt.xticks(np.arange(xlow,xhigh+1))

def histogram(title,ds):
    paramChecker("histogram",[list],[ds])
    s = stats.itemfreq(ds)

    plt.subplot(211)
    plt.gca().get_yaxis().set_visible(False)
    xaxis_assist(s)
    plt.boxplot(ds, 0, 'rs', 0)

    Q = []
    for i in range(0,101,25):
        Q.append(np.percentile(ds,i))
    IQR = Q[3]-Q[1]
    Wmin = float(math.ceil(Q[1] - 1.5 * IQR))
    Wmax = float(math.floor(Q[3] + 1.5 * IQR))
    Q[0] = Q[0] if Q[0] > Wmin else Wmin
    Q[4] = Q[4] if Q[4] < Wmax else Wmax
    for value in Q:
        plt.text(value,1.1,value,ha='center', va='bottom')
    plt.title(title)

def barPlot(ds):
    paramChecker("barPlot",[list],[ds])
    s =  stats.itemfreq(ds)

    plt.subplot(212)
    plt.gca().yaxis.grid(True)
    xaxis_assist(s)
    plt.bar(s[:,0], s[:,1] / np.sum(s[:,1]),align="center")


def freqPlot(title,ds):
    paramChecker("freqPlot",[list],[ds])
    histogram(title,ds)
    barPlot(ds)
    plt.show()

def plotD(num,faces,mod=0,drop=0):
    title = "{0}d{1}".format(num,faces)
    if mod > 0:
        title += "+%d" % mod
    if drop == 1:
        title += ", drop low"
    elif num-drop == 1:
        title += ", take high"
    elif drop > 1:
        title += ", drop %d low" % drop
    freqPlot(title,d(num,faces,mod=mod,drop=drop))

def demo():
    numberCount = widgets.IntSlider(description='Number of Dice',min=1,max=12,step=1,value=4,continuous_update=False)
    faceCount = widgets.IntSlider(description='Dice Type',min=2,max=20,step=1,value=4,continuous_update=False)
    modifier = widgets.IntSlider(description='Modifier',min=-5,max=10,step=1,value=2,continuous_update=False)
    dropCount = widgets.IntSlider(description='Number of Removed Low Rolls',min=0,max=3,step=1,value=1,continuous_update=False)

    def update_max_drop(*args):
        dropCount.max = numberCount.value - 1
    numberCount.on_trait_change(update_max_drop,name="value")

    interact(plotD,num=numberCount,faces=faceCount,mod=modifier,drop=dropCount)
