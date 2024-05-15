class Posting:

    def __init__(self, docID, freq, url):
        self.docID = docID
        self.freq = freq
        self.url = url

    def to_dict(self):
        return {"docID": self.docID, "freq": self.freq, "url": self.url}