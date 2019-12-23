'''
The Semantics Legal Information Systems project.
Running this file will retrieve federal agency descriptions from the Federal Register and Dbpedia, then will create
 .csv and .txt files with BERT, word2vec and tfidf similarity scores between such descriptions.

Created on Sep 25, 2019
Submitted: Dec 22, 2019

@author: David Fu
'''

from uriMatching import uriMatching
from dbpediaRequest import DbpediaRequest
from docSimilarity import docSimilarity
import pprint
import gensim
from sentence_transformers import SentenceTransformer
import csv

uriMatching = uriMatching()
frNameUrlMap, nameToUriMap, uriToFedRegAbstracts = uriMatching.matchWdFrByName()

uriMatches = []
uriToFedRegUrl = {}
for key in frNameUrlMap.keys():
    try:
        if nameToUriMap[key] == None:
            match = frNameUrlMap[key] + " : None"
        else:  
            for uri in nameToUriMap[key]:
                match = frNameUrlMap[key] + " : " + uri
                uriMatches.append(uri)
                uriToFedRegUrl[uri] = frNameUrlMap[key]
        print(match)
    except:
        continue

dbReq = DbpediaRequest()

data = dbReq.getJsonAbstractsFromWikidataURIs('https://dbpedia.org/sparql', uriMatches)
wdAbstracts = dbReq.getAbstractsFromDict(data)

docSim = docSimilarity()
print("LOADING WORD EMBEDDINGS")
# Download the FastText model
model = gensim.models.KeyedVectors.load_word2vec_format('~/Desktop/GoogleNews-vectors-negative300.bin', binary=True, limit = 500000).wv
print("LOADED")
transformerModel = SentenceTransformer('bert-base-nli-mean-tokens')


toPrintTfidf = []
toPrintWordVec = []
toPrintBERT = []
count = 0
for uri in uriMatches:
    pair = [wdAbstracts[uri], uriToFedRegAbstracts[uri]]
    similarity = docSim.getTFIDF(pair)
    word2vecSim = docSim.softCosine(model, pair)
    bertSimilarity = docSim.getCosineBERT(pair,transformerModel)
    count += 1
    print("Computing similarities: ", count, "/", len(uriMatches))

    toPrintTfidf.append([similarity, uri, uriToFedRegUrl[uri]])
    toPrintWordVec.append([word2vecSim, uri, uriToFedRegUrl[uri]])
    toPrintBERT.append([bertSimilarity, uri, uriToFedRegUrl[uri]])

toPrintTfidf.sort(key = lambda x:x[0])
toPrintWordVec.sort(key = lambda x:x[0])
toPrintBERT.sort(key = lambda x:x[0])

f = open("td-idf.txt", "w+")
for i in toPrintTfidf:
    f.write(str(i[0]) + " : " + str(i[1]) + " " + str(i[2]) + "\n")
f.close()

f = open("word2vec.txt", "w+")
for i in toPrintWordVec:
    f.write(str(i[0]) + " : " + str(i[1]) + " " + str(i[2]) + "\n")
f.close()

f = open("bert.txt", "w+")
for i in toPrintBERT:
    f.write(str(i[0]) + " : " + str(i[1]) + " " + str(i[2]) + "\n")
    print(i)
f.close()

f = open("csvPrintFailures.txt", "w+")
f.write("Failed to print in csv: \n")
with open('tfidfScores.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Score', 'Fedreg Abstract', 'Dbpedia Abstract', 'Wikidata URI', 'Fedreg URL'])
    for i in toPrintTfidf:
        try:
            writer.writerow([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
        except:
            print("Could not write tf-idf csv row", [i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
            f.write("tf-idf: " + str([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]]) + "\n")

with open('wordVecScores.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Score', 'Fedreg Abstract', 'Dbpedia Abstract', 'Wikidata URI', 'Fedreg URL'])
    for i in toPrintWordVec:
        try:
            writer.writerow([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
        except:
            print("Could not write wordVec csv row", [i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
            f.write("wordVec: " + str([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]]) + "\n")
        
with open('BERTscores.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Score', 'Fedreg Abstract', 'Dbpedia Abstract', 'Wikidata URI', 'Fedreg URL'])
    for i in toPrintBERT:
        try:
            writer.writerow([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
        except:
            print("Could not write BERT csv row", [i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]])
            f.write("BERT: " + str([i[0], uriToFedRegAbstracts[i[1]], wdAbstracts[i[1]], i[1], i[2]]) + "\n")
f.close()
print("Complete: Wrote to CSV and .txt files.")