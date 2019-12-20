# Scikit Learn
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
        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        tfidf = TfidfVectorizer().fit_transform(documents)
        # no need to normalize, since Vectorizer will return normalized tf-idf
        pairwise_similarity = tfidf * tfidf.T
        return pairwise_similarity.toarray()[0][1]

    def getCosineBERT(self, documents, model):
        """
        Returns a similarity score between Sentence Transformers BERT sentence embeddings of two documents.
        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        sentence_embeddings = model.encode(documents)
        return (1 - scipy.spatial.distance.cosine(sentence_embeddings[0], sentence_embeddings[1]))
        

    def hardCosine(documents):
        """
        Returns a similarity score between word2vec representations of two documents.
        @param documents: A size 2 array of strings. Example: ['This is a short sentence.', 'One. Two sentences here.']
        """
        # Create the Document Term Matrix
        count_vectorizer = CountVectorizer(stop_words='english')
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(documents)

        # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=['doc_1', 'doc_2', 'doc_3', 'doc_4', 'doc_5', 'doc_6'])

        # Compute Cosine Similarity
        return cosine_similarity(df, df)

    def softCosine(self, model, documents):
        
        # Prepare a dictionary and a corpus.
        dictionary = corpora.Dictionary([simple_preprocess(doc) for doc in documents])

        # Prepare the similarity matrix
        similarity_matrix = model.similarity_matrix(dictionary, tfidf=None, threshold=0.0, exponent=2.0, nonzero_limit=100)
        
        # Convert the sentences into bag-of-words vectors.
        sentenceVector = []
        for doc in documents:
            sentenceVector.append(dictionary.doc2bow(simple_preprocess(doc)))

        return softcossim(sentenceVector[0], sentenceVector[1], similarity_matrix)