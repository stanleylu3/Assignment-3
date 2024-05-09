from collections import Counter

from bs4 import BeautifulSoup
import Posting as p
import zipfile

class FileReader:

    def __init__(self):
        pass

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
                    n += 1
                    soup = BeautifulSoup(contents, 'html.parser')
                    text = soup.get_text() if soup else contents
                    # replace this with tokenizer
                    tokens = text.split()
                    token_freq = Counter(tokens)
                    for token, freq in token_freq.items():
                        if token not in index:
                            #create token in index and create posting object
                            posting = p.Posting(n, freq)
                            index[token] = posting


        return index

