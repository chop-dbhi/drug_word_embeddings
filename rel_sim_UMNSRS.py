import csv
from gensim.models import word2vec
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load saved model
model = word2vec.Word2Vec.load_word2vec_format('./model/model_dimension_248.bin', binary=True)  # C text format
vocab = model.vocab

# load drugs in DrugBank data
data = pd.read_csv("./data/DrugBank_drug.csv")
drugs = data['name'].values

# get two terms and sim/rel scores from UMNSRS dataset
data = pd.read_csv("./dataset/UMNSRS_relatedness.csv")
term1 = data['term1'].values
term2 = data['term2'].values
mean = data['mean'].values

meanArray = []
simArray = []
for i in range(0, len(term1)):
    if term1[i] in vocab and term2[i] in vocab:
        if term1[i] in drugs and term2[i] in drugs:
        # if term1[i] in drugs or term2[i] in drugs:
        # if term1[i] not in drugs and term2[i] not in drugs:
            sim = model.similarity(term1[i], term2[i])
            meanArray.append(mean[i])
            simArray.append(sim)

# calculate correlation coefficient
pearson = pearsonr(meanArray, simArray)
spearman = spearmanr(meanArray, simArray)
print "Pearsonr: ", pearson[0]
print "Spearmanr: ", spearman[0]
print len(simArray)


