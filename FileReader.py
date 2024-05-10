import os.path
from collections import Counter

from nltk.tokenize import RegexpTokenizer
import Posting as p
import json
import zipfile

class FileReader:

    def __init__(self):
        self.total_docs = 0

    def build_index(self, path):
        # index to be returned at the end of parsing files
        index = {}
        # beginning of serialization of documents
        n = 0
        with zipfile.ZipFile(path, 'r') as files:
            # loop through all documents and tokenize content
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read().decode('utf-8')
                    try:
                        json_data = json.loads(contents)
                        text = json_data.get('content','')
                    except json.decoder.JSONDecodeError:
                        print(f"Empty file or invalid JSON content in {file}. Continuing to next.")
                        continue
                    n += 1
                    tokenizer = RegexpTokenizer(r'\w+')
                    tokens = tokenizer.tokenize(text.lower())
                    token_freq = Counter(tokens)
                    for token, freq in token_freq.items():
                        if token not in index:
                            #create token in index and create posting object
                            posting = p.Posting(n, freq)
                            index[token] = posting.to_dict()

        self.total_docs = n
        return index

    def calculate_size(self, index, path):
        # serialize the index to temp JSON file
        temp_json = "temp.json"
        with open(temp_json, 'w') as json_file:
            json.dump(index, json_file)
        # calculate size in KB
        index_size = os.path.getsize(temp_json) / 1024
        # delete the temp file
        os.remove(temp_json)

        return index_size