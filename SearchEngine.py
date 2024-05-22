import json
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import time

class SearchEngine:

    def __init__(self, index_path='index.json', doc_info_path='doc_info.json'):
        self.index = self.load_json(index_path)
        self.doc_info = self.load_json(doc_info_path)
        self.total_docs = len(self.doc_info)
        self.stemmer = PorterStemmer()

    def load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    # function to tokenize search query to match terms stored in index
    def tokenize_query(self, query):
        tokenizer = RegexpTokenizer(r'\b[a-zA-Z0-9]+\b')
        tokens = tokenizer.tokenize(query.lower())
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    def search(self, query):
        # start time of query
        start_time = time.time()
        # logic that will search index for query
        all_docs = set()
        # sort tokens by least amount of postings
        sorted_tokens = sorted(query, key=lambda token: self.index.get(token, {'postings': [], 'df': 0})['df'])
        # loops through all tokens and gets postings from index
        for token in sorted_tokens:
            postings = self.index.get(token, {}).get('postings', [])
            doc_ids = set(posting['docID'] for posting in postings)
            # adds the list of docIDs if it is empty
            if not all_docs:
                all_docs = doc_ids
            elif all_docs:
                all_docs = all_docs.intersection(doc_ids)
            # break loop if no docs match
            if not all_docs:
                break

        if all_docs:
            all_docs = list(all_docs)

        # adding timing functionality to measure runtime of queries
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Query runtime: {runtime:.4f} seconds")

        return all_docs

    def match_docIDs(self, docIDs):
        urls = []
        for docID in docIDs:
            if str(docID) in self.doc_info:
                urls.append(self.doc_info[str(docID)]['url'])
        return urls

    def run(self):
        while True:
            # asks for user query and prints out result from query
            query = input("Enter your query: ")
            stemmed_tokens = self.tokenize_query(query)
            results = self.search(stemmed_tokens)
            urls = self.match_docIDs(results)
            for url in urls:
                print(url)