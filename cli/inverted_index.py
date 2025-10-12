import os
from preprocessing import preprocess_string
import pickle

class InvertedIndex:
    def __init__(self):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, str] = {}

    def __add_document(self, doc_id: int, text: str):
        self.docmap[doc_id] = text

        tokens = preprocess_string(text)
        for token in tokens:
            self.__add_to_index(token, doc_id)

    def __add_to_index(self, token : str, doc_id: int):
        if token not in self.index:
            self.index[token] = set()
        self.index[token].add(doc_id)

    def get_documents(self, token: str) -> list[str]:
        doc_ids = sorted(self.index.get(token, set()), key=lambda x: int(x))
        return [self.docmap[doc_id] for doc_id in doc_ids]

    def build(self, documents: dict[int, str]):
        inverted_index = InvertedIndex()
        for doc_id, text in documents.items():
            print(f"Indexing document {doc_id}")
            inverted_index.__add_document(doc_id, text)
        print(f"First document for token 'merida' = {inverted_index.get_documents('merida')[0]}")

    def save(self):
        if not os.path.exists('cache'):
            os.makedirs('cache')
        with open('cache/index.pkl', 'wb') as file:
            pickle.dump(self.index, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        with open('cache/dockmap.pkl', 'wb') as file:
            pickle.dump(self.docmap, file, protocol=pickle.HIGHEST_PROTOCOL)