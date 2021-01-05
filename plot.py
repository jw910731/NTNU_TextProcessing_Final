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
    plt.rcParams['axes.unicode_minus']=False
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei','Arial']
    for i in list(DICT[list(DICT.keys())[0]].keys()):
        tmpDICT={}
        for j in list(DICT.keys()):
            tmpDICT[j]=DICT[j][i]
        plt.figure(figsize=(12,12))
        plt.bar(list(tmpDICT.keys()),tmpDICT.values(),color='g')
        plt.title(i)
        plt.savefig("result_"+i+'.png')
        print(tmpDICT)
