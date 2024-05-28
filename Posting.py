class Posting:

    def __init__(self, docID, tf):
        self.docID = docID
        self.tf = tf

    def to_dict(self):
        return {"docID": self.docID, 'tf': self.tf}