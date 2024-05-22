import os.path
import zipfile
import json
import warnings
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from Posting import Posting
import math

class FileReader:

    def __init__(self):
        self.total_docs = 0
        self.stemmer = PorterStemmer()

    def build_index(self, path):
        # suppress warnings from bs4
        warnings.filterwarnings("ignore", category=UserWarning)

        # index to be returned at the end of parsing files
        index = {}
        # beginning of serialization of documents
        num_of_doc = 0
        # dictionary to store doc URLs
        doc_info = {}
        # list to store all documents for idf calculation
        token_df = {}
        with zipfile.ZipFile(path, 'r') as files:
            # loop through all documents and tokenize content
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read().decode('utf-8')
                    text, url = self.process_document(contents)
                    if text is None:
                        continue
                    num_of_doc += 1
                    # indexes url into dictionary
                    doc_info[num_of_doc] = {'url': url}

                    # use beautifulsoup to parse relevant html content
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=UserWarning)
                        soup = BeautifulSoup(text, 'html.parser')
                    relevant_tags = soup.find_all(['b','h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span',
                                                   'title', 'li', 'td', 'th', 'cite', 'href'])
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
                            index[token] = {'postings': [], 'df': 0}
                        # calculate tf
                        tf = freq / len(stemmed_tokens)
                        # create token in index and create posting object
                        posting = Posting(num_of_doc, freq, tf)
                        index[token]['postings'].append(posting.to_dict())
                        # counts how many documents have this token
                        # token_df[token] = token_df.get(token, 0) + 1
                        if token not in token_df:
                            token_df[token] = 1
                        else:
                            token_df[token] += 1

        print('Calculating IDF scores...')
        #calulate IDF score
        idf_scores = {}
        for token, df in token_df.items():
            idf_scores[token] = math.log(num_of_doc / (1 + df))
        print('Updating postings with tf-idf score...')
        # update postings with tfidf score
        for token, postings_info in index.items():
            df = token_df[token]
            idf = idf_scores[token]
            postings = postings_info['postings']
            for posting in postings:
                posting['tf_idf'] = idf * posting['tf']
                # removes tf and freq to save space in index
                del posting['tf']
                del posting ['freq']
            # sorts token postings based on td-idf score
            sorted_postings = sorted(postings, key = lambda x: x['tf_idf'], reverse = True)
            # creates df for each token
            index[token]['df'] = df
            print("doc freq:", index[token]['df'])
            index[token]['postings'] = sorted_postings


        self.total_docs = num_of_doc
        # saves index and doc info to json files
        with open('index.json', 'w') as f:
            json.dump(index, f)
        with open('doc_info.json', 'w') as f:
            json.dump(doc_info, f)

        return index, doc_info

    def calculate_size(self, index, path):
        # suppress warnings from bs4
        warnings.filterwarnings("ignore", category=UserWarning)

        # serialize the index to temp JSON file
        temp_json = "temp.json"
        with open(temp_json, 'w') as json_file:
            json.dump(index, json_file)
        # calculate size in KB
        index_size = os.path.getsize(temp_json) / 1024
        # delete the temp file
        os.remove(temp_json)

        return index_size

    def process_document(self, contents):
        try:
            json_data = json.loads(contents)
            text = json_data.get('content', '')
            url = json_data.get('url', 'No URL')
        except json.decoder.JSONDecodeError:
            print(f"Empty file or invalid JSON content. Skipping document.")
            return None, None
        return text, url