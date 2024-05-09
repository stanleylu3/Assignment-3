class Posting:
    def __init__(self, docID):
        self.docID = docID
        # initialize count for freq
        self.freq = 0
    def increment_term_freq(self):
        self.freq += 1

