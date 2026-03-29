import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

"""Handles text preprocessing: tokenization, stemming, and stopword removal."""
class Preprocessor:
    
    """Initialize the preprocessor with stopwords and stemmer."""
    def __init__(self, stopword_file):
        self.stopwords = set()
        self.stemmer = PorterStemmer()
        self.load_stopwords(stopword_file)

    def load_stopwords(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.stopwords.add(word)

    def preprocess(self, text):
        # Convert to lowercase for consistent processing
        text = text.lower()
        # Remove punctuation and special characters - keep only letters, digits,
        #  underscores, and spaces
        text = re.sub(r'[^a-z0-9_\s]', ' ', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Filter and stem: keep only meaningful words and remove stop words
        result = []
        for token in tokens:

            if token not in self.stopwords and len(token) > 2:
                # 
                result.append(self.stemmer.stem(token))

        return result
