import json
import pickle
from nltk.stem import PorterStemmer
import re,string
import math

# initial the urlMap, this must be run first before start hw3.py
urlDocIdMap = {}
with open('./maps/urlDocIdMap', 'wb') as f:
        pickle.dump(urlDocIdMap, f)
docIdUrlMap = {}
with open('./maps/docIdUrlMap', 'wb') as f:
    pickle.dump(docIdUrlMap, f)

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