# -*-coding:UTF-8 -*-
import sys
import sqlite3
import emoji
import re
import json
sys.path.append("../Bot/")
import postgresql as sql

def readJson(jsonPath):
    with open(jsonPath, 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
    return data

def strQ2B(comments):
    ss = []
    for i in comments:
        n = ""
        for j in i:
            num = ord(j)
            if num == 0x3000:
                num = 32
            elif 0xFF01 <= num <= 0xFF5E:
                num -= 0xfee0
            n = n + chr(num)
        ss.append(n)
    return ss

def rmplusone(comments):
    l = len(comments)
    for i in range(l):
        if re.match(r"^[\+＋]\d$", comments[i]) != None:
            comments[i] = None
        if comments[i] in ["+", "++", "加1"]:
            comments[i] = None
    comments = list(filter(None, comments))
    return comments

def rmemoji(comments, emojiJson):
    l = len(comments)
    for i in range(l):
        text = emoji.demojize(comments[i])
        reList = re.findall(r':\S+?:', text)
        if reList != []:
            for j in reList:
                if j[1:-1] in emojiJson:
                    text = re.sub(j, emojiJson[j[1:-1]], text)
                else:
                    text = re.sub(j, '', text)
        comments[i] = text
    comments = list(filter(None, comments))
    return comments

def preProcess():
    db = sql.Db('nlp2020', 'nlp2020')
    comments = db.getAll()
    db.cleanup()
    comments = rmemoji(comments, readJson('./emoji.json'))
    comments = strQ2B(comments)
    comments = rmplusone(comments)
    return comments

if __name__ == '__main__':
    textList = preProcess()
    for i in textList:
        print(i)
