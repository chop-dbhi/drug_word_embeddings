from gensim.models import word2vec
import gensim, logging
import numpy
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

inputFile = './data/corpus_pubmed_drugbank.txt'
with open(inputFile) as f:
    sentences = f.read().splitlines()

# split sentence into words
texts = [[word for word in sentence.split()] for sentence in sentences]
print("Done: split sentence into separate words")

# Set values for various parameters
vec_dimension = 420  # Word vector dimensionality
min_count = 2
window = 5
sg = 1
hs = 1

print("Training model...")
model = word2vec.Word2Vec(texts, size=vec_dimension, window=window, sg=sg, hs=hs, min_count=min_count, workers=55)
print("The vocabulary size is: " + str(len(model.vocab)))

# Save Model
model.init_sims(replace=False)
fname = './model_test/model1121_bin.bin'
model.save_word2vec_format(fname, binary=True)



