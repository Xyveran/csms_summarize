import nltk
import numpy as np
import pandas as pd
import random
import networkx as nx
import re
import spacy
import pytextrank
import gensim
import gensim.downloader as api
import mmap
import os
import math
from math import e
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, brown
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

class Texts:

    stop_words_en = set(stopwords.words('english'))

    # need to move this as to never intialize more than once per app start
    model = KeyedVectors.load(r'models\word2vec-google-news-300.model')

    text = None

    original = None
    token_words = None
    token_sentences = None
    filtered_words = None
    filtered_sentences = None
    sim_matrix = None
    nx_graph = None

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
    
    def create_sentence_vectors(self):
        # this is done by word2vec-google-news-300
        return
    
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

        if summary_length < 1:
            # ln(x)^2, rounded up to highest integer
            summary_length = math.ceil(math.log(len(self.token_sentences))**2)        

        for i in range(summary_length):
            print(ranked[i][1])

    # # TextRank Algorithm
    # # Gather text.
    # # Split text into sentences.
    # # Find each sentences’ vector representation – word embeddings.
    # # Calculate similarities between sentence vectors and store in a matrix.
    # # Convert matrix into a graph with sentences as vertices and similarity scores as edges.
    # # x number of top-ranked sentences form the final summary.

    def get_original(self):     

        return self.original

    
txt = Texts(" Text to be summarized. Here it is to utilize. A rabbi ate the president this morning. Covid was an inside job.")
txt.run_extractive_summarization()