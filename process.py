# -*- coding: UTF-8 -*-
#import plot
import pre
import csvwriter as csv
from pypinyin import pinyin, Style
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from queue import Queue
from pprint import pprint
import sys,re,threading,time,concurrent.futures,json
import pandas as pd
sys.path.append("../")
from ArticutAPI import ArticutAPI

articut = ArticutAPI.Articut()

def readJson(jsonPath):
    with open(jsonPath, 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

def createJson(jsonPath, inputDict):
    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(inputDict, f, indent=4, ensure_ascii=False)

def nameJob(inputStr, af):
    nameList = []
    try:
        cutResult = None
        userDefinedName = './name.json'
        while cutResult is None or not cutResult['status']:
            if cutResult is not None:
                if "現代白話中文" in cutResult['msg']:
                    print("Articut拒絕處理字串: {}  Skipping...".format(inputStr), file=sys.stderr)
                    af.write(inputStr+'\n')
                    #print(inputStr, file=af)
                    return None
                time.sleep(3)
            cutResult = articut.parse(inputStr, level="lv2", userDefinedDictFILE=userDefinedName)
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
    with open("./entertainment.txt", "a+", encoding="utf-8") as af:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Start the load operations and mark each future with its URL
            tasks = []
            for v in textList:
                tasks.append(executor.submit(nameJob, v, af))
            for future in concurrent.futures.as_completed(tasks):
                partial = future.result()
                if partial is not None:
                    for v in partial:
                        if v in nameDict:
                            nameDict[v] = nameDict[v] + 1
                        else:
                            nameDict[v] = 1
    return nameDict

def Attribute(textList):
    attJson = readJson('./attribute.json')
    attDict = {}
    resultDict = {}
    sia = SIA()
    for i in textList:
        for j in attJson:
            for k in attJson[j]:
                if k in i:
                    if j in resultDict:
                        tmp = sia.polarity_scores(i)
                        for l in tmp.keys():
                            resultDict[j][l] = resultDict[j][l] + tmp[l]
                        resultDict[j]['Total']=resultDict[j]['Total']+1
                    else:
                        resultDict[j] = sia.polarity_scores(i)
                        resultDict[j]['Total']=1
                    if j in attDict:
                        attDict[j] = attDict[j] + 1
                    else:
                        attDict[j] = 1
                    break
    for i in list(resultDict.keys()):
        for j in list(resultDict[i].keys())[0:3]:
            resultDict[i][j]=resultDict[i][j]/resultDict[i]['Total']
    return attDict, resultDict

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
    # print(textList)
    # print(len(textList))
    # sumDonate = donate(textList)
    # pprint(sumDonate)
    # nameDict = name(textList)
    # pprint(nameDict)
    # createJson('./nameResult.json', nameDict)
    attDict, sentimentDict = Attribute(textList)
    # pprint(attDict)
    # pprint(sentimentDict)
    # plot.makeSentimentplot(sentimentDict)
    # plot.makeplot(attDict)
    # csv.csvwrite(sentimentDict)
