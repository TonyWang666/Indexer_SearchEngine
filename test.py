import json
import pickle
from nltk.stem import PorterStemmer

# initial the urlMap, this must be run first before start hw3.py
# fileMap = {}
# with open('urlMap', 'wb') as f:
#         pickle.dump(fileMap, f)


# Output of the data we need:
documentCount = 0
UniqueTokenCount = 0
with open('./map_result/combinedTable', 'rb') as f:
    loadedFile = pickle.load(f)
    print('number of unique word is:',  len(loadedFile))
with open('urlMap', 'rb') as f:
    loadedFile = pickle.load(f)
    print('number of unique document is:', len(loadedFile))


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
