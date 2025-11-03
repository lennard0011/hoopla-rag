#!/usr/bin/env python3

import argparse
import json
import math
from inverted_index import InvertedIndex
from preprocessing import preprocess_string

STOPWORDS = open("data/stopwords.txt").read().splitlines()

def get_movies(movies, query: str):
    query_tokens = preprocess_string(query)
    found_movies = []
    for movie in movies:
       movie_tokens = preprocess_string(movie['title'])
       match = any(token in movie_token for token in query_tokens for movie_token in movie_tokens)    
       
       if match:
            found_movies.append(movie)
    found_movies = sorted(found_movies, key=lambda x: x['id'])         
    return found_movies[:5]

def print_found_movies(found_movies):
   for index, movie in enumerate(found_movies):
       print(f"{index + 1}. {movie['title']}") 

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the inverted index")

    tf_parser = subparsers.add_parser("tf", help="Get term frequency for a term in a document")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to get frequency for")

    idf_parser = subparsers.add_parser("idf", help="Get inverse document frequency for a term")
    idf_parser.add_argument("term", type=str, help="Term to get IDF for")

    args = parser.parse_args()
    movies = json.load(open("data/movies.json"))["movies"]

    match args.command:
        case "search":
            print("Searching for: QUERY") 
            inverted_index = InvertedIndex()
            inverted_index.load()
            tokens = preprocess_string(args.query)
           
            found_movies = []
            for token in tokens:
                found_movies_by_token = inverted_index.get_documents(token)
                print(f"Found {len(found_movies_by_token)} documents for token '{token}':")
                for doc in found_movies_by_token:
                    found_movies.append(doc)
                    if len(found_movies) >= 5:
                        break
                        
                print_found_movies(found_movies)
                    
        case "build":
            inverted_index = InvertedIndex()
            inverted_index.build(movies)
            inverted_index.save()

        case "tf":
            inverted_index = InvertedIndex()
            inverted_index.load()
            doc_id = args.doc_id
            term = args.term
            tf = inverted_index.get_tf(doc_id, term)
            print(f"Term Frequency of '{term}' in document ID {doc_id}: {tf}")
        
        case "idf":
            term = args.term
            inverted_index = InvertedIndex()
            inverted_index.load()
            
            number_of_documents = inverted_index.get_number_of_documents()
            term_doc_count = inverted_index.get_number_of_documents_with_term(term)
            idf = math.log((number_of_documents + 1) / (term_doc_count + 1))
            
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}") 
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()