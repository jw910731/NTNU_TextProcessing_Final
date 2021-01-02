# -*-coding:UTF-8 -*- 
import sys, sqlite3, emoji, re, json
sys.path.append("../Bot/")
import postgresql as sql

def readJson(jsonPath):
	with open (jsonPath, 'r', encoding="utf-8") as f:
		data = json.loads(f.read())
	return data

def rmplusone(comments):
	l = len(comments)
	for i in range(l):
		if comments[i] in ["+1", "＋１", "+１", "＋1"]:
			comments[i] = None
	comments = list(filter(None, comments))
	return comments

def rmemoji(comments, emojiJson):
	l = len(comments)
	for i in range(l):
		text = emoji.demojize(comments[i])
		reList = re.findall(':\S+?:', text)
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
	emojiJson = readJson('./emoji.json')
	comments = rmemoji(comments, emojiJson)
	comments = rmplusone(comments)
	return comments

if __name__=='__main__':
	textList = preProcess()
	for i in textList:
		print(i)
