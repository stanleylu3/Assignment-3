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

    def process_document(self, contents):
        try:
            json_data = json.loads(contents)
            text = json_data.get('content', '')
            url = json_data.get('url', 'No URL')
        except json.decoder.JSONDecodeError:
            print(f"Empty file or invalid JSON content. Skipping document.")
            return None, None
        return text, url

    def build_partial_index(self, docs, start_id):
        # index to be returned at the end of parsing files
        index = {}
        # dictionary to store doc URLs
        doc_info = {}
        # list to store all documents for idf calculation
        token_df = {}
        for doc_id, (contents, file) in enumerate(docs, start=start_id):
            text, url = self.process_document(contents)
            if text is None:
                continue
            self.total_docs += 1
            doc_info[doc_id] = {'url': url}
            # use beautifulsoup to parse relevant html content
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category = UserWarning)
                soup = BeautifulSoup(text, 'html.parser')
            relevant_tags = soup.find_all(['b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span',
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
                posting = Posting(doc_id, tf)
                index[token]['postings'].append(posting.to_dict())
                # counts how many documents have this token
                if token not in token_df:
                    token_df[token] = 1
                else:
                    token_df[token] += 1
            # calculate idf scores
            idf_scores = {token: math.log(self.total_docs / (1 + df)) for token, df in token_df.items()}
            # update the index with tf_idf scores
            for token, postings_info in index.items():
                idf = idf_scores[token]
                for posting in postings_info['postings']:
                    posting['tf_idf'] = idf * posting['tf']

                postings_info['df'] = len(postings_info['postings'])

        return index, doc_info

    def save_index(self, index, doc_info, index_path, doc_info_path):
        with open(index_path, 'w') as f:
            json.dump(index, f)
        with open(doc_info_path, 'w') as f:
            json.dump(doc_info, f)

    def load_index(self, index_path):
        with open(index_path, 'r') as f:
            return json.load(f)

    def merge_indexes(self, partial_indexes):
        final_index = {}
        final_doc_info = {}

        sorted_tokens = []
        # sort all tokens in all the indexes
        for index, doc_info in partial_indexes:
            sorted_tokens.extend(index.keys())
            final_doc_info.update(doc_info)

        sorted_tokens = sorted(set(sorted_tokens))
        # iterates through sorted tokens and creates final index
        for token in sorted_tokens:
            for index, _ in partial_indexes:
                postings_info = index.get(token, {'postings': [], 'df': 0})
                if token not in final_index:
                    final_index[token] = {'postings': [], 'df': 0}
                final_index[token]['postings'].extend(postings_info['postings'])
                final_index[token]['df'] += postings_info['df']
        # sort postings by tf-idf score
        for token, postings_info in final_index.items():
            postings_info['postings'].sort(key=lambda x: x['tf_idf'], reverse=True)

        return final_index, final_doc_info

    def build_final_index(self, path, batch_size = 5000):
        partial_indexes = []
        current_docs = []
        start_id = 1

        with zipfile.ZipFile(path, 'r') as files:
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read().decode('utf-8')
                    current_docs.append((contents, file))
                    # build partial indexes with a specified batch size
                    if len(current_docs) == batch_size:
                        partial_index, doc_info = self.build_partial_index(current_docs, start_id)
                        index_path = f'partial_index_{len(partial_indexes)}.json'
                        doc_info_path = f'partial_doc_info{len(partial_indexes)}.json'
                        self.save_index(partial_index, doc_info, index_path, doc_info_path)
                        partial_indexes.append((index_path, doc_info_path))
                        start_id += len(current_docs)
                        current_docs = []
            # handle the remaining documents
            if current_docs:
                partial_index, doc_info =self.build_partial_index(current_docs, start_id)
                index_path = f'partial_index_{len(partial_indexes)}.json'
                doc_info_path = f'partial_doc_info{len(partial_indexes)}.json'
                self.save_index(partial_index, doc_info, index_path, doc_info_path)
                partial_indexes.append((index_path, doc_info_path))
        # load all the indexes into a list
        loaded_indexes = [(self.load_index(index_path), self.load_index(doc_info_path))
                          for index_path, doc_info_path in partial_indexes]
        # merge the indexes
        final_index, final_doc_info = self.merge_indexes(loaded_indexes)
        # write the final index and doc_info into json files
        with open('index.json', 'w') as f:
            json.dump(final_index, f)
        with open('doc_info.json', 'w') as f:
            json.dump(final_doc_info, f)
        # delete the partial indexes
        for index_path, doc_info_path in partial_indexes:
            os.remove(index_path)
            os.remove(doc_info_path)

    def create_positions_index(self, index_path, positions_index_path):
        token_positions = {}
        newline_char_length = len('\n'.encode('utf-8'))
        # load completed index
        with open(index_path, 'r') as f:
            # initialize beginning position
            byte_position = 0
            # iterate through tokens
            for line in f:
                token, data = line.strip().split(': ', 1)
                token_positions[token] = byte_position
                byte_position += len(line.encode('utf-8')) + newline_char_length

        with open(positions_index_path, 'w') as f:
            json.dump(token_positions, f)

    def convert_index_to_txt(self, index_path):
        with open(index_path, 'r') as f:
            index = json.load(f)

        with open('index.txt', 'w') as f:
            for token, data in index.items():
                f.write(f'{token}: {data}\n')

