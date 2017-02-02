import csv
from decimal import *
from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load saved model
model = word2vec.Word2Vec.load_word2vec_format('./model/model_dimension_420.bin', binary=True)  # C binary format
vocab = model.vocab

inputFile = './data/outlier_detection_D-rand.csv'

# #### Calculate compactness Score #### #
with open(inputFile, "rb") as f:
    reader = csv.reader(f)
    termLists = list(reader)

clusterSize = 5         # set the size of neighborhood (drugs + outlier)
scoreLists = []
for row in termLists:
    compact = 0
    scoreList = []
    for k in range(0, clusterSize):
        count = 0
        compact = 0
        for i in range(0, clusterSize):
            if i == k or row[i] not in vocab:
                continue
            for j in range(0, clusterSize):
                if j == i or j == k or row[j] not in vocab:
                    continue
                else:
                    compact += model.similarity(row[i], row[j])
                    count += 1
        if count == 0:
            compact = 0
        else:
            compact = compact/count
        scoreList.append(compact)
    if 0 not in scoreList:
        scoreLists.append(scoreList)

# # save compactness Score into CSV file
# with open('./data/compactScore_5_1.csv', "wb") as f:
#     writer = csv.writer(f)
#     writer.writerows(results)
# print "Done"

# # open the file of compactness Score
# with open("./data/compactScore_5_1.csv", "rb") as f:
#     reader = csv.reader(f)
#     lists = list(reader)

# #### Calculate Accuracy and OPP in outlier detection #### #
count_od = 0
numCluster = len(scoreLists)
opp = 0
for row in scoreLists:
    sorted_row = sorted(range(len(row)), key=lambda k: row[k])  # save the original index after sorting the row
    if sorted_row[clusterSize-1] == clusterSize-1:
        count_od += 1
    else:
    temp = 0
    for i in range(0, clusterSize):
        if sorted_row[i] == clusterSize-1:
            temp = i
    temp = Decimal(temp)/(clusterSize-1)
    opp += temp

accuracy = Decimal(count_od)/numCluster
opp = Decimal(opp)/numCluster
print accuracy
print opp
print "correct outlier num: ", count_od
print "total cluster num: ", numCluster




