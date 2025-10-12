import string
from nltk.stem import PorterStemmer

STOPWORDS = open("data/stopwords.txt").read().splitlines()

def preprocess_string(s: str) -> list[str]:
    s = s.translate(str.maketrans('', '', string.punctuation))
    tokens = s.lower().split()
    tokens_without_stopwords = [token for token in tokens if token not in STOPWORDS]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens_without_stopwords]
    return stemmed_tokens

