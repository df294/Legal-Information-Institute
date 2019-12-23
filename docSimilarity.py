"""
The docSimilarity class contains all methods necessary to compare two documents using tf-idf, word2vec, and BERT.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import gensim
# upgrade gensim if you can't import softcossim
from gensim.matutils import softcossim 
from gensim import corpora
import gensim.downloader as api
from gensim.utils import simple_preprocess

from sentence_transformers import SentenceTransformer
import scipy.spatial.distance

class docSimilarity():

    def getTFIDF(self, documents):
        """
        Returns a TF-IDF similarity score between two documents.
        Credit and additional information: https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents

        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        tfidf = TfidfVectorizer().fit_transform(documents)
        # no need to normalize, since Vectorizer will return normalized tf-idf
        pairwise_similarity = tfidf * tfidf.T
        return pairwise_similarity.toarray()[0][1]

    def getCosineBERT(self, documents, model):
        """
        Returns a similarity score between Sentence Transformers BERT sentence embeddings of two documents.
        Credit and additional information: https://github.com/UKPLab/sentence-transformers

        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        sentence_embeddings = model.encode(documents)
        return (1 - scipy.spatial.distance.cosine(sentence_embeddings[0], sentence_embeddings[1]))
        

    def softCosine(self, model, documents):
        """
        Returns a similarity score using cosine similarity between combined word vectors of two documents.
        Credit and additional information: https://www.machinelearningplus.com/nlp/cosine-similarity/

        @param model: A set of pretrained word embeddings, such as GoogleNews-vectors-negative300.bin.
        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        # Prepare a dictionary and a corpus.
        dictionary = corpora.Dictionary([simple_preprocess(doc) for doc in documents])

        # Prepare the similarity matrix
        similarity_matrix = model.similarity_matrix(dictionary, tfidf=None, threshold=0.0, exponent=2.0, nonzero_limit=100)
        
        # Convert the sentences into bag-of-words vectors.
        sentenceVector = []
        for doc in documents:
            sentenceVector.append(dictionary.doc2bow(simple_preprocess(doc)))

        return softcossim(sentenceVector[0], sentenceVector[1], similarity_matrix)