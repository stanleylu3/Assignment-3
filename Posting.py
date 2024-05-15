class Posting:

    def __init__(self, docID, freq, tf):
        self.docID = docID
        self.freq = freq
        self.tf = tf

    def to_dict(self):
        return {"docID": self.docID, "freq": self.freq, 'tf': self.tf}