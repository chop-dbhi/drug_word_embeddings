The pretrained word embeddings are available at:

[https://s3.amazonaws.com/chop-dbhi/user/masinoa/drug_embedding_model.tar.gz](https://s3.amazonaws.com/chop-dbhi/user/masinoa/drug_embedding_model.tar.gz)

# To generate and evaluate new embeddings:

1.abstractExtraction.py: given the query, extract PubMed abstracts and save results into .csv files

2.model_training.py: train and save word2vec models on given corpus (we use PubMed+DrugBank to create our corpus)

3.model_grid_search.py: train models by varying vec_dimension, min_count, and window_size; evaluate quality of the trained model by calculating correlation coefficient between word vector size and its frequency

4.rel_sim_UMNSRS: evaluate relatedness and similarity of word embeddings on UMNSRS-rel and UMNSRS-sim datasets

5.coherence.py: assess coherence in drugs' neighborhood

6.outlier_detect.py: calculate accuracy and OPP in outlier detection task

