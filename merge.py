import pickle
def mergeTwoFile(baseFileName, fileName2, storeFileName):
    # load two inverted Table
    with open(baseFileName, 'rb') as f:
        baseTable = pickle.load(f)
    with open(fileName2, 'rb') as f:
        table2 = pickle.load(f)

    # merge two into combined
    # key: token; value: {totalFreq: INT, docDict: { Key: docId:INT; value: {rank: INT, positions:[INT]} } }
    # For each token in table2, we insert or update corresponding baseTable[token]
    for token in table2:
        # if token exist in baseTable, update value of baseTable[token]
        if token in baseTable.keys():
            # increment totalFreq
            baseTable[token]['totalFreq'] += table2[token]['totalFreq'] 
            # insert or update docDict of table2[token] exist in docDict of baseTable[token](logic is to update the information of html page)
            for docId in table2[token]['docDict'].keys():
                baseTable[token]['docDict'][docId] = table2[token]['docDict'][docId]
        else:
            baseTable[token] = table2[token]
    # load base table back to base file 
    with open(storeFileName, 'wb') as f:
        pickle.dump(baseTable, f)         
    
if __name__ == '__main__':
    print("hello world")
    fileName1 = './map_result/loading1'
    fileName2 = './map_result/loading2'
    fileName3 = './map_result/loading3'
    storeFileName = './map_result/combinedTable'
    # mergeTwoFile(fileName1, fileName2, storeFileName) # First run
    mergeTwoFile(storeFileName, fileName2, storeFileName) # Second run

    