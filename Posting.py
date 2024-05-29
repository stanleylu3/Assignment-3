class Posting:

    def __init__(self, docID, tf, score):
        self.docID = docID
        self.tf = tf
        self.score = score

    def to_dict(self):
        return {"docID": self.docID, 'tf': self.tf, 'score': self.score}