import csv
from scipy.stats.stats import pearsonr
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

# controlled experiment on parameter and save models into .bin file
# with one parameter changing each time, including vec_dimension, min_count, window,
for dimension in range(240, 520, 8):
    # Set values for various parameters
    dimension = dimension     # dimension of word vector
    window = 5
    min_count = 2
    sg = 1              # sg=1 is the skip-gram algorithm
    hs = 1              # hs=0(default) and negative\=0:negative sampling will be used
    negative = 5

    print("Training model...")
    model = word2vec.Word2Vec(texts, size=dimension, sg=sg, hs=hs, min_count=min_count, window=window, workers=50)

    modelFile = './model/model_dimension_' + str(dimension) + '.bin'
    model.save_word2vec_format(modelFile, binary=True)

    # with open('./result/model_train_history.txt', 'a') as f:
    #     parameters = 'dimension=' + str(dimension) + ',min_count=2' + ',window=' + str(window) + \
    #             ',negative=' + str(negative)
    #     f.write(parameters)
    #     f.write('\n')

	# ###correlation analysis between word occurrence-frequency and vector-length
	# load saved model
	model = word2vec.Word2Vec.load_word2vec_format(modelFile, binary=True)
	vocab = model.vocab

	# rows = []
	freqArray = []
	lenArray = []
	for word in vocab:
   		# row = []
    	# name = word
    	frequency = model.vocab[word].count
    	length = numpy.linalg.norm(model[word])    # calculate the length of a vector
    	# add the items into the array - row
    	# row.append(name)
    	# row.append(frequency)
    	freqArray.append(frequency)
    	# row.append(length)
    	lenArray.append(length)
    	# rows.append(row)
    	# print "name:", name, " length:", length, " frequency:", frequency

	result = pearsonr(freqArray, lenArray)
	print "Model: ", modelFile, " Pearsonr: ", result[0]

