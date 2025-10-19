import os
from preprocessing import preprocess_string
import pickle

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, object] = {}

    def __add_document(self, document: dict):
        print(f"Indexing document ID: {document['id']}")
        doc_id = document['id']
        self.docmap[doc_id] = document

        text = f"{document['title']} {document['description']}" 

        tokens = preprocess_string(text)
        for token in tokens:
            self.__add_to_index(token, doc_id)

    def __add_to_index(self, token : str, doc_id: int):
        if token not in self.index:
            self.index[token] = set()
        self.index.setdefault(token, set()).add(doc_id)

    def get_documents(self, token: str) -> list[object]:
        doc_ids = sorted(self.index.get(token, set()), key=lambda x: int(x))
        return [self.docmap[doc_id] for doc_id in doc_ids]

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
    
    def load(self):
        with open('cache/index.pkl', 'rb') as file:
            self.index = pickle.load(file)
        
        with open('cache/dockmap.pkl', 'rb') as file:
            self.docmap = pickle.load(file)
        