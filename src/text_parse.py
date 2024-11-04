import nltk
import numpy as np
import pandas as pd
import networkx as nx
import gensim
import gensim.downloader as api
import math
from math import e
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, brown
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

class Texts:

    stop_words_en = set(stopwords.words('english'))
    model = KeyedVectors.load(r'models\word2vec-google-news-300.model')

    def __init__(self, new_text):
        self.text = new_text
        self.original = new_text

    def __tokenize_to_words(self, input=None):
        if input is None:
            text = word_tokenize(self.text)
            self.token_words = text
        else:
            return word_tokenize(input)         
    
    def __tokenize_to_sentences(self, input=None):
        if input is None:
            text = sent_tokenize(self.text)
            self.token_sentences = text
        else:
            return sent_tokenize(input)
    
    def __drop_stopwords(self, choice):
        text = None

        match choice.lower():
            case "w":
                text = [word for word in self.token_words if word.lower() not in self.stop_words_en]
                self.filtered_words = text
            case "s":
                self.filtered_sentences = []                
                for sentence in self.token_sentences:
                    words = self.__tokenize_to_words(sentence)
                    text = [word for word in words if word.lower() not in self.stop_words_en]
                    self.filtered_sentences.append(" ".join(text))
            case _:
                print("Use 'w' for words or 's' for sentences.")

    def __lemmatize(self):
        return None
    
    def __create_sentence_similarity_matrix(self):
        sentence_vectors = []

        for sentence in self.filtered_sentences:
            word_vectors = []

            if len(sentence) != 0:
                for word in sentence:
                    if word in self.model:
                        word_vectors.append(self.model[word])
                    else:
                        word_vectors.append(np.zeros(300))

                sentence_vectors.append(np.mean(word_vectors, axis=0))
            else:
                sentence_vectors.append(np.zeros(300))

        sim_matrix = np.zeros([len(self.token_sentences), len(self.token_sentences)])

        for i in range(len(self.token_sentences)):
            for j in range(len(self.token_sentences)):
                if i != j:
                    sim_matrix[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,300), 
                                                         sentence_vectors[j].reshape(1,300))[0,0]

        self.sim_matrix = sim_matrix

    def graph_similarity_matrix(self):
        self.nx_graph = nx.from_numpy_array(self.sim_matrix)
        return nx.pagerank(self.nx_graph)
    
    def run_extractive_summarization(self, summary_length = 0):
        self.__tokenize_to_sentences()
        self.__drop_stopwords('s')
        self.__create_sentence_similarity_matrix()

        scores = self.graph_similarity_matrix()

        ranked = sorted(((scores[i],s) for i,s in enumerate(self.token_sentences)), reverse=True)

        result = ""
        if summary_length < 1:
            # ln(x)^2, rounded up to highest integer
            summary_length = math.ceil(math.log(len(self.token_sentences))**2)        

        for i in range(summary_length):
            result += ranked[i][1] + " "

        return result

    def get_original(self):     

        return self.original