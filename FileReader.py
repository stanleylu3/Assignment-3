import os.path
from collections import Counter
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import Posting as p
import json
import zipfile

class FileReader:

    def __init__(self):
        self.total_docs = 0
        self.stemmer = PorterStemmer()

    # def extract_text(self, html_content):
    #     soup = BeautifulSoup(html_content, 'lxml')
    #     important_text = []
    #     # adding important text from bold, headings, and titles
    #     for tag in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
    #         important_text.extend(tag.stripped_strings)
    #     return ' '.join(important_text)

    def build_index(self, path):
        # index to be returned at the end of parsing files
        index = {}
        # beginning of serialization of documents
        num_of_doc = 0
        with zipfile.ZipFile(path, 'r') as files:
            # loop through all documents and tokenize content
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read().decode('utf-8')
                    try:
                        json_data = json.loads(contents)
                        text = json_data.get('content','')
                        # text = self.extract_text(html_content)
                    except json.decoder.JSONDecodeError:
                        print(f"Empty file or invalid JSON content in {file}. Continuing to next.")
                        continue
                    num_of_doc += 1
                    # use beautifulsoup to parse relevant html content
                    soup = BeautifulSoup(text, 'html.parser')
                    relevant_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span',
                                                   'title', 'li', 'td', 'th', 'cite', ])
                    parsed_content = [tag.get_text() for tag in relevant_tags]
                    final_content = ''.join(parsed_content)
                    tokenizer = RegexpTokenizer(r'\b[a-zA-Z0-9]+\b')
                    tokens = tokenizer.tokenize(final_content.lower())
                    # added stemming for better textual matches
                    stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
                    # counts stemmed tokens now
                    token_freq = Counter(stemmed_tokens)
                    for token, freq in token_freq.items():
                        if token not in index:
                            index[token] = []
                            # create token in index and create posting object
                        posting = p.Posting(num_of_doc, freq)
                        index[token].append(posting.to_dict())

        self.total_docs = num_of_doc
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