import pickle


class PageRank:
    def __init__(self, dg_in, dg_out):
        self.max_iterations = 100
        self.min_delta = 0.00001
        self.graph_in = dg_in
        self.graph_out = dg_out
        self.dict = {}

    def getPr(self):
        g_in = self.graph_in
        g_out = self.graph_out
        default_page_rank = 1.0
        default_delta_page_rank = 1.0
        deltaPr = {}
        prScore = {}
        loopCount = 0
        with open('./maps/docIdUrlMap', 'rb') as f:
            docIdUrlMap = pickle.load(f)
        for docId in docIdUrlMap:
            deltaPr[docId] = default_delta_page_rank
            prScore[docId] = default_page_rank
        # PR(A) = 0.15 + 0.85 * delta PR
        # PR(A) ==> prScore
        # prScore ==> {key(docid):value(float==> pr)}
        # deltaPr ==> {key(docid):value(float==> delta pr)}
        while loopCount < (self.max_iterations + 1):
            loopCount += 1
            # doc_A to be the DocId we are working on
            # doc_B to be all docids pointed to doc_A

            # this loop for calculating doc A's delta pr
            for doc_A in g_in:
                # g_in ==> {key(docid):value(url => docid)}
                if doc_A not in prScore:
                    prScore[doc_A] = default_page_rank  # set default pr
                    deltaPr[doc_A] = default_delta_page_rank  # set default delta pr

                else:
                    doc_B_List = g_in[doc_A]

                    for doc_B in doc_B_List:
                        doc_B_out_num = float(len(g_out[doc_B]))
                        deltaPr[doc_A] += (prScore[doc_B] / doc_B_out_num)  # doc A get pr from Bs

            # this loop is to set pr score for doc A based on delta pr we get above
            # and calculate with formula PR(A) = 0.15 + 0.85 * delta PR
            ml_iter = False  # set a variable meaningless iteration as ml_iter
            for doc_A in g_in:
                tempPr = prScore[doc_A] # to record the pr of doc A before iteration
                prScore[doc_A] = 0.15 + 0.85 * deltaPr[doc_A]
                if abs(prScore[doc_A] - tempPr) < self.min_delta:
                    ml_iter = True
                if ml_iter and loopCount >= 20:  # to make the delta is bigger than min delta
                    break

                deltaPr[doc_A] = 0.0

        return prScore
# for point A: doc_B_list = ['C'] doc B = c
print('Hello Page Rank...')
with open('./maps/inGraph', 'rb') as f:
    inGraphMap = pickle.load(f)
with open('./maps/outGraph', 'rb') as f:
    outGraphMap = pickle.load(f)
pageRankObj = PageRank(inGraphMap, outGraphMap)
pageRankDict = pageRankObj.getPr()
with open('./maps/pageRankDict', 'wb') as f:
    pickle.dump(pageRankDict, f)
