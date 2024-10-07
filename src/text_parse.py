import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, brown

class Texts:

    stop_words_en = set(stopwords.words('english'))

    def __init__(self, newtxt):
        self.txt = newtxt

    def tokenize_to_words(self):
        text = word_tokenize(self.txt)
        self.words = text
    
    def tokenize_to_sentences(self):
        text = sent_tokenize(self.txt)
        self.sentences = text
    
    def drop_stopwords(self):
        text = [word for word in self.words
                    if word.lower() not in self.stop_words_en]
        self.filtered = text
    
    def lemmatize(self):
        return None
   
    def get_original(self):        
        return self.txt
    
    def get_filtered(self):
        result = None

        if hasattr(self, 'filtered'):
            result = self.filtered
        else:
            result = AttributeError('Filtered Text Does Not Exist')

        return result
    
    def get_word_tokens(self):
        result = None

        if hasattr(self, 'words'):
            result = self.words
        else:
            result = AttributeError('Word Tokens Do Not Exist')

        return result
    
    def get_sentence_tokens(self):
        result = None
        
        if hasattr(self, 'sentences'):
            result = self.sentences
        else:
            result = AttributeError('Sentence Tokens Do Not Exist')

        return result
    
#txt = Texts("This is a bit of informat1on in a plaintext format 2 be read by the application. Checking to  see if it reads all the informat1on ... correctly")
# txt.tokenize_to_words()
# txt.drop_stopwords()
#txt.tokenize_to_words()
#print(txt.get_word_tokens())

#print(txt.__dict__)