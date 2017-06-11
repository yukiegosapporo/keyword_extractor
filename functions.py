import math
import os
from textblob import TextBlob as tb
from gensim.models import doc2vec
from collections import namedtuple
from sklearn.cluster import AffinityPropagation
from collections import defaultdict
from operator import itemgetter
import numpy as np
import csv
from config import logger

def get_module_path(file_name):
    return os.path.dirname(os.path.realpath(file_name))

class KeyphraseExtractor(object):
    def __init__(self, project_path,use_cluster,top_n):
        self.project_path = project_path
        self.data_path = os.path.join(project_path, "data")
        self.use_cluster = use_cluster
        self.top_n = top_n
        self.paths = [
        os.path.join(self.data_path, file) for file in os.listdir(self.data_path) if ".txt"in file]
        self.phrase_list = None
        self.clustered_phrase_list = None
        self.phrase_scores = None
        self.key_phrases = None
        logger.info("Keyword extractor created with the following parameters")
        logger.info("project_path: {}".format(self.project_path))
        logger.info("use_cluster: {}".format(self.use_cluster))
        logger.info("top_n: {}".format(self.top_n))
        logger.info("paths: {}".format(self.paths))
    
    def get_phrase_list(self, threshold=30):
        def script2tb(threshold):
            res = list()
            lines = list()
            for path in self.paths:
                f = open(path, "rb")
                lines = lines + f.read().decode('UTF-8').splitlines()
                f.close()
            combined = ""
            for idx, line in enumerate(lines):
                if len(line) != 0:
                    combined = combined + line
                else:
                    if len(combined) >= threshold:
                        res.append(combined)
                    combined = ""
            return res

        def get_nouns(blob):
            return [word for word, tag in blob.tags if tag == "NN"]

        logger.info("Getting phrase list")
        tbs = script2tb(threshold)
        bloblist = list(map(lambda x: tb(str(x)).lower(), tbs))
        phrase_list = [get_nouns(blob) + list(blob.noun_phrases.lemmatize()) for blob in bloblist]
        self.phrase_list = phrase_list
        logger.info("Phrase list made: {} docs".format(len(phrase_list)))

    def tfidf(self, phrase, phrases, data):
        def tf(phrase, phrases):
            return phrases.count(phrase) / len(phrases)

        def n_containing(phrase, data):
            return sum(1 for phrases in data if phrase in phrases)

        def idf(phrase, data):
            return math.log(len(data) / (1 + n_containing(phrase, data)))
        return tf(phrase, phrases) * idf(phrase, data)

    def cluster_docs(self):
        docs = []
        analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
        for i, words in enumerate(self.phrase_list):
            tags = [i]
            docs.append(analyzedDocument(words, tags))
        d2v = doc2vec.Doc2Vec(docs, size = 1000, window = 300, min_count = 1, workers = 4)
        clusters = AffinityPropagation().fit_predict(np.vstack(
           d2v.docvecs))
        return list(zip(self.phrase_list, clusters))

    def get_clustered_phrase_list(self):
        logger.info("Clustering docs")
        clustered_phrases = self.cluster_docs()
        res = defaultdict(list)
        for clustered_phrase in clustered_phrases:
            res[clustered_phrase[1]] += clustered_phrase[0]
        self.clustered_phrase_list = list(res.values())
        logger.info("Clustered phrase list into {}".format(len(clustered_phrases)))

    def get_phrase_scores(self):
        logger.info("Getting phrases and their scores")
        if int(self.use_cluster)==1:
            self.get_clustered_phrase_list()
            data = self.clustered_phrase_list
            logger.info("Using clustered phrase list as an input")
        else:
            data = self.phrase_list
            logger.info("Using raw phrase list as an input")
        res = defaultdict(list)
        for i, phrases in enumerate(data):
            logger.debug("Phrases in document {}".format(i + 1))
            scores = {phrase: self.tfidf(phrase, phrases, data) for phrase in phrases}
            sorted_phrases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            tmp = list()
            for phrase, score in sorted_phrases:
                logger.debug("Phrase: {}, TF-IDF: {}".format(phrase, round(score, 4)))
                tmp.append([phrase, round(score, 4)])
            logger.debug("\n")
            res[i] = tmp
        self.phrase_scores = res

    def get_key_phrases(self):
        logger.info("Getting key phrases")
        res = defaultdict(float)
        for _, v in self.phrase_scores.items():
            for phrase_score in v:
                res[phrase_score[0]] += phrase_score[1]
        self.key_phrases = sorted(res.items(), key=itemgetter(1), reverse=True)[:int(self.top_n)]
        logger.info("Saving top {} key phrases to {}".format(
            self.top_n,
            os.path.join(self.project_path,"keyphrases.csv")))
        with open(os.path.join(self.project_path,"keyphrases.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.key_phrases)

