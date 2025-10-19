import os
from preprocessing import preprocess_string
import pickle
from collections import Counter

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, object] = {}
        self.term_frequencies: dict[int, Counter] = {} 

    def __add_document(self, document: dict):
        print(f"Indexing document ID: {document['id']}")
        doc_id = document['id']
        self.docmap[doc_id] = document

        text = f"{document['title']} {document['description']}" 

        tokens = preprocess_string(text)
        for token in tokens:
            self.__add_to_index(token, doc_id)
        self.term_frequencies[doc_id] = Counter(tokens)

    def __add_to_index(self, token : str, doc_id: int):
        if token not in self.index:
            self.index[token] = set()
        self.index.setdefault(token, set()).add(doc_id)

    def get_documents(self, token: str) -> list[object]:
        doc_ids = sorted(self.index.get(token, set()), key=lambda x: int(x))
        return [self.docmap[doc_id] for doc_id in doc_ids]
    
    def get_tf(self, doc_id: int, term: str) -> int:
        tokens = preprocess_string(term)
        if len(tokens) != 1:
            raise ValueError("Term must be a single token")
        term_token = tokens[0]
        return self.term_frequencies.get(doc_id, Counter()).get(term_token, 0)

    def build(self, documents: list[dict]):
        for document in documents:
            self.__add_document(document)

    def save(self):
        if not os.path.exists('cache'):
            os.makedirs('cache')
        with open('cache/index.pkl', 'wb') as file:
            pickle.dump(self.index, file)
        
        with open('cache/dockmap.pkl', 'wb') as file:
            pickle.dump(self.docmap, file)
        
        with open('cache/term_frequencies.pkl', 'wb') as file:
            pickle.dump(self.term_frequencies, file)
    
    def load(self):
        with open('cache/index.pkl', 'rb') as file:
            self.index = pickle.load(file)
        
        with open('cache/dockmap.pkl', 'rb') as file:
            self.docmap = pickle.load(file)
        
        with open('cache/term_frequencies.pkl', 'rb') as file:
            self.term_frequencies = pickle.load(file)
        