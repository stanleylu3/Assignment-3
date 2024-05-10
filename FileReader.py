import os.path
from collections import Counter
from bs4 import BeautifulSoup
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
                    # use beautifulsoup to parse relevant html content
                    soup = BeautifulSoup(text, 'html.parser')
                    relevant_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p','span',
                                                   'title', 'li', 'td','th', 'cite',])
                    parsed_content = [tag.get_text() for tag in relevant_tags]
                    final_content = ''.join(parsed_content)
                    n += 1
                    tokenizer = RegexpTokenizer(r'\b[a-zA-Z0-9]+\b')
                    tokens = tokenizer.tokenize(final_content.lower())
                    token_freq = Counter(tokens)
                    for token, freq in token_freq.items():
                        if token not in index:
                            index[token] = []
                            #create token in index and create posting object
                        posting = p.Posting(n, freq)
                        index[token].append(posting.to_dict())

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