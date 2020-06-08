import json
import pickle
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import re,string
from lxml import etree
import math
from lxml import html

# initial the urlMap, this must be run first before start hw3.py
urlDocIdMap = {}
with open('./maps/urlDocIdMap', 'wb') as f:
        pickle.dump(urlDocIdMap, f)
docIdUrlMap = {}
with open('./maps/docIdUrlMap', 'wb') as f:
    pickle.dump(docIdUrlMap, f)
word2gramMap = {}
with open('./maps/word2gramMap', 'wb') as f:
    pickle.dump(word2gramMap, f)
inGraphMap = {}
with open('./maps/inGraph', 'wb') as f:
    pickle.dump(inGraphMap, f)
outGraphMap = {}
with open('./maps/outGraph', 'wb') as f:
    pickle.dump(outGraphMap, f)


# word2gramMap = {}
# with open('./maps/word2gramMap', 'rb') as f:
#     word2gramMap = pickle.load(f)
#     if 'chen li' in word2gramMap:
#         print(True)

# Input: 1. content: a list of words; n: number of ngrams
# Output: Ex: {'abcnew': 1, 'newyork': 2, 'yorknew': 1, 'newapple': 1, 'applegood': 1, 'gooduci': 1, 'ucinew': 1}

# def ngrams(content, n):
#     output = {}
#     for i in range(len(content)-n+1):
#         #print(i)
#         ngramTemp = ''.join(content[i:i+n])
#         #print(ngramTemp)
#         if ngramTemp not in output:
#             output[ngramTemp] = 0
#         output[ngramTemp] += 1
#     return output

# tokenList = ['tony', 'is', 'doing', 'great']

# uniqueDocId = 1
# ngramsMap = ngrams(tokenList, 2)
# word2gramMap = {}
# for token in ngramsMap:
#     if token in word2gramMap: # token is {key: token, value: frequency}
#         word2gramMap[token][uniqueDocId] = word2gramMap[token].setdefault(uniqueDocId, 0) + ngramsMap[token] # increment target token's uniqueDoc's frequency; ex: {token: {docId: freq++} }
#     else:
#         word2gramMap[token] = {uniqueDocId: ngramsMap[token]} # token hasn't existed, create a new map for it n word2gramMap
                
# print('word2gramMap is:')
# print(word2gramMap)

# # Test n grams
# def tokenize(content):
#     token = re.findall(r"[A-Za-z0-9]+", content.lower())
#     return token
# fileObj = open('./DEV/loading1/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json')
# wholeFile = json.loads(fileObj.read())
# url, content = wholeFile['url'], wholeFile['content']
# element_tree = html.fromstring(content) 
# for link in element_tree.xpath('//a/@href'):
#     print('link is:', link)
# fileObj.close()

        # element_tree = html.fromstring(resp.raw_response.content) 

        # for link in element_tree.xpath('//a/@href'):
        #     res.append(urldefrag(link)[0])

# soup = BeautifulSoup(content, 'lxml')
# text = soup.find_all(text=True)
# print('text is:')
# print(text)
# for t in text:
#     print('token list is:')
#     tokenList = tokenize(t)
#     print(tokenList)
#     print(type(t))
#     string = t
#     string.strip()
#     print('t is:', t)
#     print('first char is:', t[0])
#     print('tag name is:', t.parent.name)
#     print(t.split())

# # Deleting the trap website
# f = open("./maps/urlDocIdMap", "rb")
# urlDocIdMap = pickle.load(f)
# f = open("./maps/docIdUrlMap", "rb")
# docIdUrlMap = pickle.load(f)
# docId = urlDocIdMap["http://mondego.ics.uci.edu/datasets/maven-contents.txt"]
# print('docid is:', docId)
# del docIdUrlMap[docId]


# with open('./map_result/combinedTable', 'rb') as f:
#     invertedTable = pickle.load(f)
#     index = 0
#     for token in invertedTable:
#         print(invertedTable[token])
#         index += 1
#         if index == 1:
#             break

# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
# for k, v in sorted(x.items(), key=lambda item: item[1]):
#     print(x[k])
# {0: 0, 2: 1, 1: 2, 4: 3, 3: 4}

# b1 = a1
# b1['Tony'] = 456
# print(a1['Tony'])



# Output of the data we need:
# documentCount = 0
# UniqueTokenCount = 0
# with open('./map_result/combinedTable', 'rb') as f:
#     loadedFile = pickle.load(f)
#     print('number of unique word is:',  len(loadedFile))
# with open('urlMap', 'rb') as f:
#     loadedFile = pickle.load(f)
#     print('number of unique document is:', len(loadedFile))


# testing on porter stem
# wordList = ["gaming", "nagative", "image", "imagination", "games", "images"]
# ps = PorterStemmer()
# for word in wordList:
#     print(ps.stem(word))
#Output is: "game nag imag imagin game imag". Not very accuracy but work


# testing the final output
# with open('./map_result/combinedTable', 'rb') as f:
#     loadedFile = pickle.load(f)
#     print('number of unique word is:', len(loadedFile)) # "number of unique word is: 403743"
#     index = 0
#     for token in loadedFile:
#         if index >= 1:
#             break
#         index += 1
#         print(token, ": ", loadedFile[token])


# open and load the dictionary with pickle
# invertedIndex['token'] = {'totalFreq': 1, 'docDict': {docId: {'rank': 100, 'positions': [1, 2, 3]} } }
# with open('mypickle.pickle', 'wb') as f:
#     pickle.dump(invertedIndex, f)
# with open('mypickle.pickle','rb') as f:
#     loaded_obj = pickle.load(f)
# print('rank is:', loaded_obj['token']['docDict'][docId]['rank'])
# print('docId exist is: ', docId in loaded_obj['token']['docDict'].keys())
# print('loaded_obj is', loaded_obj)
# using picke because json map key into string


# write and load dictionary with json
# invertedTable = {'test': 100}
# with open('./map_result/' + folderLocation, 'w') as f:
#     json.dump(invertedTable, f)
# with open('./map_result/' + folderLocation) as f:
#     a = json.load(f)
#     for each in a:
#         print(each, ' ', a[each])

# Original HW_3 Milestone2
# get all rank of counted document, only keep documents have all terms in the query
# for token in tokenize(text):
#     token = ps.stem(token)
#     if token not in self.invertedTable:
#         print('token is not in invertedTable')
#         continue
#     if len(resDocumentDict) == 0:
#         for docId in self.invertedTable[token]['docDict']:
#             resDocumentDict[docId] = self.invertedTable[token]['docDict'][docId]['rank']
#     else:
#         res = {} #signature: key: docId, value: rank(Int)
#         newDocDict = self.invertedTable[token]['docDict']
#         if(len(resDocumentDict) < len(newDocDict)):
#             for docId in resDocumentDict:
#                 if docId in newDocDict:
#                     res[docId] = resDocumentDict[docId] + newDocDict[docId]['rank'] # add both rank together
#             resDocumentDict = res
#         else:
#             for docId in newDocDict:
#                 if docId in resDocumentDict:
#                     res[docId] = resDocumentDict[docId] + newDocDict[docId]['rank'] # add both rank together
#             resDocumentDict = res
# # Now the resDocumentDict has all ranked docId
# # Return top 5 url with most rank value
# index = 1
# result = []
# for k, v in sorted(resDocumentDict.items(), key=lambda item:item[1], reverse=True):
#     if index >= 6: 
#         break
#     result.append(self.urlMap[k])
#     index += 1
# return result




# # For extra credit ngrams and anchor
# content = ['abc', 'new', 'york', 'new', 'apple', 'good', 'uci', 'new','york']
# content1 = ['abc', 'new']

# # Signature:
# # content: word list
# # n: number of grams
# def ngrams(content, n):
#     output = {}
#     for i in range(len(content)-n+1):
#         #print(i)
#         ngramTemp = ''.join(content[i:i+n])
#         #print(ngramTemp)
#         if ngramTemp not in output:
#             output[ngramTemp] = 0
#         output[ngramTemp] += 1
#     output = sorted(output.items(), key=lambda k: k[1], reverse= True)
#     return output

# res = ngrams(content, 2)
# for word in res:
#     print(word)

# # output are:
# ('newyork', 2)
# ('abcnew', 1)
# ('yorknew', 1)
# ('newapple', 1)
# ('applegood', 1)
# ('gooduci', 1)
# ('ucinew', 1)

# Create during Milestone1 ==> very large map
# {docId1: {"New York": 10, "I love": 1}, docId2: {...} }

# Loop again to create and store at Milestone1
# map: {"New York": {key: docId, value: frequency} }

# ex: {1000: 10, 53: 98, 103: 2}

# Preprocess Operation:
# 1. Map all 2-gram word into map called docId2gramMap. Ex: {docId1: {"New York": 10, "I love": 1}, docId2: {...} }
# 2. After All process, loop docId2gramMap again to generate word2gramMap. Ex: {"New York": {key: docId, value: frequency} }

# Run-time Operation: # before normalization
# 1. Get list of all 2-grams from query
# 2. delete  the 2-grams from query
# 3. Calculate and Increment score at Milestone2 if query contains word combination
#     score[docId] += offset * frequency # offset = 1




# Anchor Text: 
# 1. If text in tag <a>:
#     anchorMap[text] = docId
    
# uci good student:
# ......
# Zhao Siheng
# .......
# goto_zhaosiheng_personal_website

# zhao si heng personal website

# map: {"zhao si heng": url}

# zhao si heng

# score[url] += 1000
