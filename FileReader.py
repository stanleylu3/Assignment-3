from bs4 import BeautifulSoup
from Posting import Posting
import zipfile
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict
import re
import os
import json


class FileReader:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        # Initialize inverted index
        self.index = defaultdict(list)

        # initialize containers to get analytics

        # beginning of serialization of documents
        self.num_indexed_doc = 0
        self.total_index_size = 0

    def preprocessing(self, text):
        # Apply stemming
        stemmer = PorterStemmer()
        tokens = word_tokenize(text)
        stemmed_tokens = [stemmer.stem(token) for token in tokens if token.isalnum()]
        return stemmed_tokens

    def build_index(self, path):

        # loop through all documents and tokenize content
        with zipfile.ZipFile(path, 'r') as files:
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read()
                    soup = BeautifulSoup(contents, 'html.parser')
                    text = soup.get_text().lower()

                    # preprocess text
                    preprocessing_tokens = self.preprocessing(text)

                    # updating inverted index with tokens and postings
                    for position, token in enumerate(preprocessing_tokens):
                        if token not in self.index:
                            self.index[token] = []
                        if not any(posting.docID == file for posting in self.index[token]):
                            self.index[token].append(Posting(file))
                        else:
                            posting = next(posting for posting in self.index[token] if posting.docID == file)
                            posting.increment_term_freq()

                    self.num_indexed_doc += 1

        # Calculate total index size
        self.total_index_size = self.calculate_index_size()

        # Save index to files
        self.save_index_to_files()

    def calculate_index_size(self):
        # Serialize the index to JSON and calculate its size
        serialized_index = json.dumps(self.index)
        size_in_bytes = len(serialized_index.encode('utf-8'))
        return size_in_bytes

    def save_index_to_files(self):
        # Serialize the index to JSON and save it to a file
        index_file_path = os.path.join(self.index_dir, 'index.json')
        with open(index_file_path, 'w') as index_file:
            json.dump(self.index, index_file)
