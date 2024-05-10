class Posting:

    def __init__(self, docID, freq):
        self.docID = docID
        self.freq = freq

    def to_dict(self):
        return {"docID": self.docID, "freq": self.freq}