from gensim.models import word2vec
from functions import findDrugInVocabulary, cleanStr, mostSim3
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# load saved model
model = word2vec.Word2Vec.load_word2vec_format('./model/model_dimension_444.bin', binary=True)  # C binary format

# call function findDrugInVocabulary(model,outputFile)
drugVocabFile = './data/drug_vocab.csv'
# findDrugInVocabulary(model, drugVocabFile)

# call function mostSim to get evaluation result
neighbor_size = 10
outputFile = './data/coherence_size_' + str(neighbor_size) + '.dataset.csv'
mostSim(model, drugVocabFile, outputFile, neighbor_size)

def mostSim(model, inputFile, outputFile, neighbor_size):
    data = pd.read_csv(inputFile)
    drug_vocab = data['name'].values
    # print type(drug_vocab[0])

    data = pd.read_csv("./data/DrugBank_drug.csv")
    drugs = data['name'].values
    # print type(drugs[0])

    rows = []
    countIsDrug = 0
    for drug in drug_vocab:
        sim_lists = model.most_similar(positive=[drug], topn=neighbor_size)
        row = []
        row.append(drug)
        for i in range(0, neighbor_size):
            sim_item = cleanStr(sim_lists[i][0])
            # print type(name)
            row.append(sim_item)

        for i in range(0, neighbor_size):
            sim = str(sim_lists[i][1])
            row.append(sim)

        for i in range(0, neighbor_size):
            if cleanStr(sim_lists[i][0]) in drugs:
                isDrug = 1
                countIsDrug += 1
                row.append(str(isDrug))
            else:
                isDrug = 0
                row.append(str(isDrug))
        rows.append(row)

    with open(outputFile, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print "Done: Coherence assessment: neighborhood_size = ", neighbor_size
	print float(countIsDrug)/(len(rows)*(neighbor_size-1))