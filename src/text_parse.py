import numpy as np
import networkx as nx
import gensim
import gensim.downloader as api
import math
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

class Texts:
    model = None
    stop_words_en = None

    @classmethod
    def load_model_and_stopwords(cls):
        if cls.model is None or cls.stop_words_en is None:
            cls.model = KeyedVectors.load(r'models\word2vec-google-news-300.model')
            cls.stop_words_en = set(stopwords.words('english'))

    def __init__(self, new_text):
        self.__class__.load_model_and_stopwords()
        self.text = new_text
        self.original = new_text

    def __tokenize_to_words(self, input_text): 
        return word_tokenize(input_text)       
    
    def __tokenize_to_sentences(self):
        return sent_tokenize(self.text)
    
    def __drop_stopwords(self, token_list, choice='w'):
        if choice == 'w':
            return [word for word in token_list if word.lower() not in self.stop_words_en]
        elif choice == 's':
            return [" ".join([word for word in self.__tokenize_to_words(sentence) if word.lower() not in self.stop_words_en]) 
                    for sentence in token_list]
        else:
            raise ValueError("Invalid choice: use 'w' for words or 's' for sentences.")

    def __create_sentence_vectors(self, sentences):
        sentence_vectors = []
        for sentence in sentences:
            word_vectors = [self.model[word] for word in sentence if word in self.model]
            if word_vectors:
                sentence_vectors.append(np.mean(word_vectors, axis=0))
            else:
                sentence_vectors.append(np.zeors(300))

        return sentence_vectors

    def __create_sentence_similarity_matrix(self, sentence_vectors):
        return cosine_similarity(sentence_vectors)

    def graph_similarity_matrix(self):
        self.nx_graph = nx.from_numpy_array(self.sim_matrix)
        return nx.pagerank(self.nx_graph)
    
    def run_extractive_summarization(self, summary_length = 0):
        sentences = self.__tokenize_to_sentences()
        filtered_sentences = self.__drop_stopwords(sentences, choice='s')

        sentence_vectors = self.__create_sentence_vectors(filtered_sentences)

        self.sim_matrix = self.__create_sentence_similarity_matrix(sentence_vectors)

        scores = self.graph_similarity_matrix()

        ranked_sentences = sorted(((score, sentence) for score, sentence in zip(scores.values(), sentences)), reverse=True)

        if summary_length < 1:
            summary_length = math.ceil(math.log(len(sentences))**2)

        summary = " ".join([ranked_sentences[i][1] for i in range(min(summary_length, len(ranked_sentences)))])

        return summary

    def get_original(self):     

        return self.original