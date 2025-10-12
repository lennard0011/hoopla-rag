#!/usr/bin/env python3

import argparse
import json
import string

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

def preprocess_string(s: str) -> list[str]:
    s = s.translate(str.maketrans('', '', string.punctuation))
    tokens = s.lower().split()
    return [token for token in tokens if token not in STOPWORDS]

def print_found_movies(found_movies):
   for index, movie in enumerate(found_movies):
       print(f"{index + 1}. {movie['title']}") 

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    movies = json.load(open("data/movies.json"))["movies"]

    match args.command:
        case "search":
           print("Searching for: QUERY") 
           query = args.query
           
           found_movies = get_movies(movies, query)
           print_found_movies(found_movies) 
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()