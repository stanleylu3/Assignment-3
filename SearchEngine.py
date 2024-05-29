import json
import math
from collections import defaultdict, Counter
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import time

class SearchEngine:

    def __init__(self, index_path='index.txt', doc_info_path='doc_info.json',
                 positions_index ='positions_index.json'):
        self.index = open(index_path, 'r')
        self.doc_info = self.load_json(doc_info_path)
        self.positions_index = self.load_json(positions_index)
        self.total_docs = len(self.doc_info)
        self.stemmer = PorterStemmer()
        self.cache = {}

    def load_json(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    # function to tokenize search query to match terms stored in index
    def tokenize_query(self, query):
        tokenizer = RegexpTokenizer(r'\b[a-zA-Z0-9]+\b')
        tokens = tokenizer.tokenize(query.lower())
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return stemmed_tokens

    def compute_tf_idf_query(self, query_tokens):
        # counts tf of tokens in query
        tf_query = Counter(query_tokens)
        # initializes dictionary to store td-idf scores
        query_vector = {}

        for token, tf in tf_query.items():
            # Calculates tf for query token
            tf_query[token] = tf / len(query_tokens)
            if token in self.index:
                # Calculates idf for token
                idf = math.log(self.total_docs / (1 + self.index[token]['df']))
                # Calculate TF-IDF score for the token in the query
                query_vector[token] = tf_query[token] * idf
            else:
                query_vector[token] = 0
        return query_vector

    def cosine_similarity(self, vec1, vec2):
        dot_product = sum(vec1[token] * vec2.get(token, 0.0) for token in vec1)
        # find magnitudes of vectors
        mag_vec1 = math.sqrt(sum(value ** 2 for value in vec1.values()))
        mag_vec2 = math.sqrt(sum(value ** 2 for value in vec2.values()))
        if mag_vec1 == 0 or mag_vec2 == 0:
            return 0.0
        # formula
        return dot_product / (mag_vec1 * mag_vec2)

    # def calculate_doc_scores(self, query_vector, docs):
    #     doc_scores = {}
    #     for docID in docs:
    #         doc_vector = {}
    #         for token in query_vector:
    #             postings = self.index.get


    def search(self, query):
        # start time of query
        start_time = time.time()
        # logic that will search index for query
        all_docs = set()
        # sort tokens by least amount of postings
        sorted_tokens = sorted(query, key=self.get_token_df)
        # loops through all tokens and gets postings from index
        for token in sorted_tokens:
            if token in self.positions_index:
                position = self.positions_index[token]
                token_data = self.read_token_data(self.index, token, position)
                if token_data is None:
                    print('no token data')
                    continue
                postings = token_data.get('postings', [])
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

    def read_token_data(self, file, token, start_position):
        if token in self.cache:
            return self.cache[token]
        file.seek(start_position)
        line = file.readline().strip()
        if not line.startswith(f"{token}"):
            return None
        try:
            _, data = line.split(': ', 1)
            token_data = eval(data)
            print(type(token_data))
            self.cache[token] = token_data
            return token_data
        except json.JSONDecodeError:
            print("error decoding json")
            return None


    def get_token_df(self, token):
        if token in self.cache:
            return self.cache[token].get('df', float('inf'))
        # get position of token in index
        position = self.positions_index.get(token)
        if position is not None:
            token_data = self.read_token_data(self.index, token, position)
            if token_data is not None:
                return token_data.get('df', float('inf'))
        return float('inf')