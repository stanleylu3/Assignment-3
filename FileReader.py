from bs4 import BeautifulSoup
import Posting
import zipfile

class FileReader:

    def __init__(self):
        pass

    def build_index(self, path):
        # index to be returned at the end of parsing files
        index = {}
        # beginning of serialization of documents
        n = 0
        # loop through all documents and tokenize content
        with zipfile.ZipFile(path, 'r') as files:
            for file in files.namelist():
                with files.open(file) as doc:
                    contents = doc.read()
                    n += 1


        return index

