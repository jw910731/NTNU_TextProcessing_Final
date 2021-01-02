# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt

def makeplot(DICT):
    plt.rcParams['axes.unicode_minus']=False
    plt.rcParams['font.sans-serif']=['Microsoft JhengHei','Arial']
    plt.figure(figsize=(16,16))
    plt.bar(list(DICT.keys()), DICT.values(), color='g',width=0.8) 
    plt.xlim([-1,11.5])
    plt.savefig("result.png")