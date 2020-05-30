import os
from lxml import etree
from bs4 import BeautifulSoup
from io import StringIO
import re,string
import json
import pickle
from nltk.stem import PorterStemmer
import re,string
import timeit
import math

def tokenize(content):
    token = re.findall(r"[A-Za-z0-9]+", content.lower())
    return token

# Input: 1. content: a list of words; n: number of ngrams
# Ex: {'abcnew': 1, 'newyork': 2, 'yorknew': 1, 'newapple': 1, 'applegood': 1, 'gooduci': 1, 'ucinew': 1}
def ngrams(content, n):
    output = {}
    for i in range(len(content)-n+1):
        #print(i)
        ngramTemp = ''.join(content[i:i+n])
        #print(ngramTemp)
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

#3 things to do:
#1. Load the dictionary
#2. Tokenize all the words and stem all the words
#3. Find the words in and get a list of documentID one by one with the sum of ranked value
#4. Return top 5 ranked url
# termWeightInQueryMap: {key: term, Value: weight of this term in query}
class MiniSearchEngine:
    urlMap = {}
    invertedTable = {}
    word2gramMap = {} #{key: "New York": {key: docId, value: frequency}, ......}
    def __init__(self, urlMapAddress, invertedTableAddress, word2gramMapAddress):
        with open(invertedTableAddress, 'rb') as f:
            self.invertedTable = pickle.load(f)
        with open(urlMapAddress, 'rb') as f:
            self.urlMap = pickle.load(f)
        with open(word2gramMapAddress, 'rb') as f:
            self.word2gramMap = pickle.load(f)

    # 
    def search(self, text):
        ps = PorterStemmer()
        scores = {} #signature: key: docId, value: score(Int)

        cleanInputArray = []
        termWeightInQueryMap = {}
        tokenList = tokenize(text)

        # clear token with stemmer
        for index, token in enumerate(tokenList):
            tokenList[index] = ps.stem(token)

        # get all 2-grams words combination from query
        query2gramList = ngrams(tokenList, 2)

        for token in query2gramList:
            if token in self.word2gramMap:
                for docId in self.word2gramMap[token]:
                    score = scores.setdefault(docId, 0)
                    scores[docId] = score + max(10, self.word2gramMap[token][docId])
                    # print('scores of 2gram is:', scores[docId])
                    

        for token in tokenList:
            if token not in termWeightInQueryMap:
                termWeightInQueryMap[token] = 1
            else:
                termWeightInQueryMap[token] += 1
            cleanInputArray.append(token)

        for key in termWeightInQueryMap:
            termWeightInQueryMap[key] = termWeightInQueryMap[key] / len(termWeightInQueryMap)

        for token in cleanInputArray:
            if token not in self.invertedTable:
                print('token is not in invertedTable')
                continue
            # Using scores[docId] = W(t,d) * W(t,q) to get scores for all related documents
            for docId in self.invertedTable[token]['docDict']:
                w_tq = termWeightInQueryMap[token]
                tf_td =  len(self.invertedTable[token]['docDict'][docId]['positions']) #tf_td: num of occurance of term t in document d
                # tf = max(1, self.invertedTable[token]['docDict'][docId]['rank'])
                df_t = math.log(len(self.urlMap) / len(self.invertedTable[token]['docDict'])) # df_t: number of document contains t
                w_td = (1 + math.log(tf_td)) * df_t # calculating weight of tf-idf by tf-idf = (1 + log(tft, d)) * log(N/dft)
                score = w_tq * w_td
                if docId in scores:
                    scores[docId] += score
                else:
                    scores[docId] = score
        for key in scores:
            scores[key] /= len(scores) # normalization
        
        # Now the resDocumentDict has all ranked docId
        # Return top 5 url with most rank value
        index = 1
        result = []
        tempRes = {}
        with open('./maps/pageRankDict', 'rb') as f:
            pageRankDict = pickle.load(f)
        # get top 20 from tf-idf algortihm and increment with page rank: k is url, v is score
        for k, v in sorted(scores.items(), key=lambda item:item[1], reverse=True):
            if index >= 20: 
                break
            index += 1
            tempRes[k] = v + pageRankDict.setdefault(k, 0)
        # get top 5 from top 20 with algorithm of tf-idf + pagerank
        # index = 1
        # for k, v in sorted(tempRes.items(), key=lambda item:item[1], reverse=True):
        #     if index > 5:
        #         break
        #     index += 1
        #     result.append(self.urlMap[k])
        # return result


                        
if __name__ == '__main__':
    print("Welcome to Goodu!")
    urlMapAddress = './maps/docIdUrlMap'
    invertedTableAddress = './map_result/combinedTable'
    word2gramMapAddress = './maps/word2gramMap'
    searchEngine = MiniSearchEngine(urlMapAddress, invertedTableAddress, word2gramMapAddress)
    while(True):
        text = input("Please enter the word you want to search and end with 'enter', or enter 'exist' to exist: ")
        if text == 'exist':
            break
        start = timeit.default_timer()
        listUrl = searchEngine.search(text)
        stop = timeit.default_timer()
        print('Time: ', stop - start)   
        print('The returned url is:')
        index = 0
        for url in listUrl:
            index += 1
            print(index, '. ', url)
    print('Thank you for your time and looking forward to next service. Good bye!')