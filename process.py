# -*- coding: UTF-8 -*-
import sys, re, threading, time, concurrent.futures, json
sys.path.append("../")
from ArticutAPI import ArticutAPI
from pprint import pprint
from queue import Queue
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pypinyin import pinyin,Style
import pre,plot

articut = ArticutAPI.Articut()

def readJson(jsonPath):
	with open (jsonPath, 'r', encoding="utf-8") as f:
		data = json.loads(f.read())
	return data

def ctp(LIST):
    resultLIST=[]
    for i in LIST:
        tmpSTR=""
        for j in i:
            tmpSTR=tmpSTR+pinyin(j,style=Style.NORMAL)[0][0]+" "
        print(tmpSTR)
        resultLIST.append(tmpSTR)
    return resultLIST

def nltkSentiment(view):
    sid = SentimentIntensityAnalyzer()
    for sen in view:
        senti = sid.polarity_scores(sen)
        for k in senti:
            print('{0}:{1},'.format(k, senti[k]), end='\n')

def nameJob(inputStr):
    nameList = []
    try:
        cutResult = None
        userDefinedName = './name.json'
        while cutResult is None or not cutResult['status']:
            if cutResult is not None:
                time.sleep(3)
            cutResult = articut.parse(inputStr, level = "lv2", userDefinedDictFILE = userDefinedName)
        personList = articut.getPersonLIST(cutResult, includePronounBOOL=False)
        for i in cutResult["result_obj"]:
            for j in i:
                if j["pos"] == "UserDefined":
                    nameList.append(j["text"])
    except Exception as e:
        print(e, file=sys.stderr)
    ret = []
    if personList != None:
        for i in personList:
            if i != []:
                for j in i:
                    print(j[2])
                    ret.append(j[2])
    nameJson = readJson('./name.json')
    for i in nameList:
        for j in nameJson:
            if i in nameJson[j]:
                print(i, '->', j)
                ret.append(j)
    return ret

def name(textList):
    nameDict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        tasks = []
        for v in textList:
            tasks.append(executor.submit(nameJob, v))
        for future in concurrent.futures.as_completed(tasks):
            partial = future.result()
            for v in partial:
                if v in nameDict:
                    nameDict[v] = nameDict[v] + 1
                else:
                    nameDict[v] = 1
    return nameDict

def Attribute(textList):
    attJson = readJson('./attribute.json')
    attDict = {}
    for i in textList:
        for j in attJson:
            for k in attJson[j]:
                if k in i:
                    if j in attDict:
                        attDict[j] = attDict[j] + 1
                    else:
                        attDict[j] = 1
                    break
    return attDict

def donate(textList):
    cnt = {}
    for i in textList:
        # text = re.match('NT\$\d+.*\d from ', i)
        text = re.search('\d+.*\d from ', i)
        if text != None:
            pos = text.start()
            moneytype = i[:pos]
            text = text.group(0).strip()
            text = re.search('\d+.*\d', text)
            text = text.group(0).replace(',', '')
            if moneytype in cnt:
                cnt[moneytype] = cnt[moneytype] + float(text)
            else:
                cnt[moneytype] = float(text)
    return cnt

if __name__ == '__main__':
    textList = pre.preProcess()
    # ctp(textList)
    # print(ctp(textList))
    # print(textList)
    # print(len(textList))
    # sumDonate = donate(textList)
    # pprint(sumDonate)
    nameDict = name(textList)
    pprint(nameDict)
    # nltkSentiment(textList)
    # attDict = Attribute(textList)
    # pprint(attDict)
    # plot.makeplot(attDict)
