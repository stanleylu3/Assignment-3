import json
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

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
        # logic that will search index for query
        pass

    def compute_tf_idf(self, term, docID):
        # logic that will compute if_idf score
        pass

    def run(self):
        while True:
            # asks for user query and prints out result from query
            query = input("Enter your query: ")
            results = self.search(query)
            for result in results:
                print(result)