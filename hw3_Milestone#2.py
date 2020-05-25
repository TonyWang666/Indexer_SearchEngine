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

#3 things to do:
#1. Load the dictionary
#2. Tokenize all the words and stem all the words
#3. Find the words in and get a list of documentID one by one with the sum of ranked value
#4. Return top 5 ranked url
# termWeightInQueryMap: {key: term, Value: weight of this term in query}
class MiniSearchEngine:
    urlMap = {}
    invertedTable = {}
    def __init__(self, urlMapAddress, invertedTableAddress):
        with open(invertedTableAddress, 'rb') as f:
            self.invertedTable = pickle.load(f)
        with open(urlMapAddress, 'rb') as f:
            self.urlMap = pickle.load(f)

    # 
    def search(self, text):
        ps = PorterStemmer()
        scores = {} #signature: key: docId, value: score(Int)

        cleanInputArray = []
        termWeightInQueryMap = {}
        for token in tokenize(text):
            token = ps.stem(token)
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
                w_td = (1 + math.log(tf_td)) * df_t
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
        for k, v in sorted(scores.items(), key=lambda item:item[1], reverse=True):
            if index >= 6: 
                break
            result.append(self.urlMap[k])
            index += 1
        return result


                        
if __name__ == '__main__':
    print("Welcome to Goodu!")
    urlMapAddress = './maps/docIdUrlMap'
    invertedTableAddress = './map_result/combinedTable'
    searchEngine = MiniSearchEngine(urlMapAddress, invertedTableAddress)
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

            
    
