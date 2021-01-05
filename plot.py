# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def makeplot(DICT):
    plt.rcParams['axes.unicode_minus']=False
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei','Arial']
    plt.figure(figsize=(16,16))
    plt.bar(list(DICT.keys()), DICT.values(), color='g',width=0.8) 
    plt.xlim([-1,11.5])
    plt.savefig("result.png")

def makeSentimentplot(DICT):
    fig , ax = plt.subplots(5, 3, sharex=True, sharey=True,figsize=(16,16))
    j=0
    plt.setp(ax,xticks=[0,1,2,3], xticklabels=['neg','neu','pos','compound'])
    for i in list(DICT.keys()):
        tmpDICT=DICT[i]
        ax[j//3,j%3].bar(range(len(tmpDICT)-1),list(tmpDICT.values())[:-1])
        j=j+1
    plt.savefig("result2.png")
