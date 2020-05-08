Statistics:
The number of documents in total is: 55393
The number of unique tokens in total is: 397430
The size of invertedIndex(dictionary) is: 134.2 MB on disk
The size of urlMap(dictionary) is: 5.2 MB on disk

Describtion:
1. We split the Folder "DEV" into 3 folders("loading1", "loading2", "loading3"), each time "hw3.py" will only process one loading folder and save the result into 
folder "map_result".
2. After all 3 folders are processed, we merge 3 processed dictionaries in the folder "map_result" into "combinedTable" with method in "merge.py"
3. Finally, we use file "test.py" to generate the output information we want.

Data Structure:
InvertedIndex: key: token; value: {totalFreq: INT, 'docMap': { key: docId:INT; value: {rank: INT, positions:[INT]} } }
Example: {"token1": {'totalFreq': 1001, 'docMap': {1: {'rank': 7, positions:[1, 23, 78]}}}}

Meeting of Requirements:
1. Token: all alphanumeric sequences in the dataset.
2. Stop Word: No stop word used during Indexing
3. Stemming: Porter Stemming in line 48 of "hw3.py"
4. Important word: all words in tag "title", "h1", "h2", "h3", "b", "strong" are given different portion of ranking scores and saved in invertedIndex 
    Formula of ranking scores for tag: TotalRank of one token in one document = numTitle * 3 + numHead * 2 + b/strongNum * 1
5. Saving the position of each word in the documents for later use