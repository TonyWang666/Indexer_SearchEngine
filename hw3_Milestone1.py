import os
from lxml import etree
from bs4 import BeautifulSoup
from io import StringIO
import re,string
import json
import pickle
from nltk.stem import PorterStemmer
from lxml import html
# from similarity_detection import isSimilarToOtherPage
import similarity_detection

global urlFingersList   # list to save calculated fingerprint of url,locked by FingerLock

urlFingersList = list()

def tokenize(content):
    token = re.findall(r"[A-Za-z0-9]+", content.lower())
    return token

# O(n)
# take a list and return the word counts
def computeWordFrequencies(tokens: [str]) -> {str: int}:
    token_map = {}
    for token in tokens:
        if token in token_map:
            token_map[token] += 1
        else:
            token_map[token] = 1
    return token_map

# Input: 1. content: a list of words; n: number of ngrams
# Output: Ex: {'abcnew': 1, 'newyork': 2, 'yorknew': 1, 'newapple': 1, 'applegood': 1, 'gooduci': 1, 'ucinew': 1}
def ngrams(content, n):
    output = {}
    for i in range(len(content)-n+1):
        ngramTemp = ''.join(content[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

# Preprocess inGraphMap and outGraphMap to inser url for the later used at Page Rank
def processGraphMap(inGraphMap, outGraphMap, content, uniqueDocId, urlDocIdMap, docIdUrlMap):
    if len(content) <= 5:
        return
    try:
        element_tree = html.fromstring(content) 
        for link in element_tree.xpath('//a/@href'):
            if link[0] == '#' or len(link) < 5:
                continue
            if link not in urlDocIdMap.keys():
                newDocId = len(urlDocIdMap)
                urlDocIdMap[link] = newDocId
                docIdUrlMap[newDocId] = link
            else:
                newDocId = urlDocIdMap[link]
            # Implement inGraphMap and outGraphMap Logic: inGraphMap[newDocId] = uniqueDocId; outGraphMap[uniqueDocId] = newDocId
            inList = inGraphMap.setdefault(newDocId, [])
            inList.append(uniqueDocId)
            outList = outGraphMap.setdefault(uniqueDocId, [])
            outList.append(newDocId)
    except:
        print('do nothing')

# Take 3 parameters: fileLocation, urlDocIdMap, invertedIndex
# fileLocation is the file location to extract data. We assume the file is in json
# urlDocIdMap is a global map to save the mapping data of url. (Key: url, Value: uniqueDocumentId(generated by us))
# docIdUrlMap is also a global map used to get correct url during searching. (Key: uniqueDocumentId(generated by us), Value: url)
# invertedIndex is the global inverted index to save the data of each document, the format is:
    # key: token; value: {totalFreq: INT, 'docMap': { key: docId:INT; value: {rank: INT, positions:[INT]} } }
# Main Task: load the json data in "fileLocation" into invertedIndex, urlDocIdMap, and docIdUrlMap

# Preprocess Operation for word2gramMap:
    # implement word2gramMap with token and docId. Ex: {key: "New York": {key: docId, value: frequency}, ......}
def indexingFile(fileLocation, urlDocIdMap, docIdUrlMap, invertedIndex, word2gramMap, inGraphMap, outGraphMap):
    try:
        print('file location is: ', fileLocation)
        fileObj = open(fileLocation)
        wholeFile = json.loads(fileObj.read())
        url, content = wholeFile['url'], wholeFile['content'] # get url and content from the file
        fileObj.close()

        # Implement the urlDocIdMap and create docId
        if url not in urlDocIdMap.keys():
            uniqueDocId = len(urlDocIdMap)
            urlDocIdMap[url] = uniqueDocId
            docIdUrlMap[uniqueDocId] = url
        else:
            uniqueDocId = urlDocIdMap[url]

        # Implement inGraphMap and outGraphMap for page Rank
        processGraphMap(inGraphMap, outGraphMap, content, uniqueDocId, urlDocIdMap, docIdUrlMap)

        # Initialize rankDictionary with algorithm: totalRank of one token in one document = numTitle * 3 + numHead * 2 + b/strongNum * 1
        tagRankingDict = {'title': 100, 'h1': 20, 'h2': 10, 'h3': 5, 'b': 5, 'strong': 5, 'p': 1, 'span': 1, "li": 1, "a": 1, "cite": 1, "em": 1, "mark": 1, "abbr": 1}

        # Create a word dictionary to save all
        soup = BeautifulSoup(content, 'lxml')
        text = soup.find_all(text=True)
        if(similarity_detection.isSimilarToOtherPage(computeWordFrequencies(text))):
            return
        pos = 0
        ps = PorterStemmer()
        for t in text:
            tokenList = tokenize(t)
            
            if t.parent.name not in tagRankingDict.keys() or len(tokenList) == 0:
                continue

            # clear token with stemmer
            for index, token in enumerate(tokenList):
                tokenList[index] = ps.stem(token) # using porter stemming
            
            # implement word2gramMap with token and docId. Ex: {"New York": {key: uniqueDocId, value: frequency, ......} }
            ngramsMap = ngrams(tokenList, 2)
            for token in ngramsMap:
                if token in word2gramMap: # token is {key: token, value: frequency}
                    word2gramMap[token][uniqueDocId] = word2gramMap[token].setdefault(uniqueDocId, 0) + ngramsMap[token] # increment target token's uniqueDoc's frequency; ex: {token: {docId: freq++} }
                else:
                    word2gramMap[token] = {uniqueDocId: ngramsMap[token]} # token hasn't existed, create a new map for it n word2gramMap

            rank = tagRankingDict[t.parent.name]
            for token in tokenList:
                if(len(token) > 10): #len(token) < 3 or 
                    continue
                # if token not in invertedIndex, create an object
                if token not in invertedIndex.keys():
                    invertedIndex[token] = {'totalFreq': 1, 'docDict': {uniqueDocId: {'rank': rank, 'positions': [pos]} } }
                # if token was in invertedIndex, update it
                else:
                    invertedIndex[token]['totalFreq'] += 1
                    # if document hasn't been stored in the same token, store it
                    if uniqueDocId not in invertedIndex[token]['docDict'].keys():
                        invertedIndex[token]['docDict'][uniqueDocId] = {'rank': rank, 'positions': [pos]}
                    # if document has been stored in the same token, update it
                    else:
                        invertedIndex[token]['docDict'][uniqueDocId]['rank'] += rank
                        invertedIndex[token]['docDict'][uniqueDocId]['positions'].append(pos)
                pos += 1

    except ValueError as e:
        print("Error in File Location:", fileLocation)
        print(e)

# 1 paramter: folderLocation
# Main Task: explore all file in "folderLocation" with method indexingFile
def indexingInvertedTable(folderLocation, urlDocIdMapAddress, docIdUrlMapAddress, word2gramMapAddress, inGraphAddress, outGraphAddress):
    # Processing folder DEV
    invertedIndex = {} # key: token; value: {totalFreq: INT, docMap: { Key: docId:INT; value: {rank: INT, positions:[INT]} } }
    urlDocIdMap = {} #
    word2gramMap = {} # Ex: {"New York": {key: docId, value: frequency} }
    inGraphMap = {}
    outGraphMap = {}
    with open(urlDocIdMapAddress, 'rb') as f:
        urlDocIdMap = pickle.load(f) # get urlDocIdMap; key: url of website, value: unique docId of each url
    with open(docIdUrlMapAddress, 'rb') as f: 
        docIdUrlMap = pickle.load(f) # get docIdUrlMap; key: unique docId of each url, value: url of website
    with open(word2gramMapAddress, 'rb') as f:
        word2gramMap = pickle.load(f)
    with open(inGraphAddress, 'rb') as f:
        inGraphMap = pickle.load(f)
    with open(outGraphAddress, 'rb') as f:
        outGraphMap = pickle.load(f)

    for (root, dirs, files) in os.walk('DEV/' + folderLocation):
        for filename in files:
            fileLocation = os.path.join(root, filename)
            try:
                # print('file_location is:', fileLocation)
                indexingFile(fileLocation, urlDocIdMap, docIdUrlMap, invertedIndex, word2gramMap, inGraphMap, outGraphMap)
            except ValueError as e:
                print("File Location:", fileLocation)
                print(e)

# pr_d: {docId: rank} saving into my local
    # save the Inverted Table into disk            
    with open('./map_result/' + folderLocation , 'wb') as f:
        pickle.dump(invertedIndex, f)
    # save the url Map into disk     
    with open(urlDocIdMapAddress, 'wb') as f:
        pickle.dump(urlDocIdMap, f)
    with open(docIdUrlMapAddress, 'wb') as f:
        pickle.dump(docIdUrlMap, f)
    with open(word2gramMapAddress, 'wb') as f:
        pickle.dump(word2gramMap, f)
    with open(inGraphAddress, 'wb') as f:
        pickle.dump(inGraphMap, f)
    with open(outGraphAddress, 'wb') as f:
        pickle.dump(outGraphMap, f)

if __name__ == '__main__':
    print("hello world")
    folderLocation1 = 'loading1'
    folderLocation2 = 'loading2'
    folderLocation3 = 'loading3'
    urlDocIdMapAddress = './maps/urlDocIdMap'
    docIdUrlMapAddress = './maps/docIdUrlMap'
    docId2gramMapAddress = './maps/docId2gramMap'
    word2gramMapAddress = './maps/word2gramMap'
    inGraphAddress = './maps/inGraph'
    outGraphAddress = './maps/outGraph'
    indexingInvertedTable(folderLocation3, urlDocIdMapAddress, docIdUrlMapAddress, word2gramMapAddress, inGraphAddress, outGraphAddress)
    
