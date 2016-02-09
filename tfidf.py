import math
from wordextractor import WordExtractor

class TFIDF:
    # This class is an implementation of the Cosine tf-idf method described in section 3.1 of
    # http://www.hindawi.com/journals/tswj/2014/745485/

    def __init__(self):
        self.doc_frequency = dict()
        self.doc_count = 0

    def calc_cosine_similarity(self, words1, words2):
        term_frequencies1 = self.__get_frequencies(words1)
        term_frequencies2 = self.__get_frequencies(words2)

        if len(words1) == 0 or len(words2) == 0:
            if len(words1) and len(words2) == 0:
                return 1
            else:
                return 0

        #now calculate cosine simmilarity between the two tf-idf vectors:

        #Calculate dot_product
        dot_product = 0
        length1 = 0
        length2 = 0
        for word in term_frequencies1:
            doc_freq = self.doc_frequency[word] if word in self.doc_frequency else 1
            idf = math.log10(self.doc_count / doc_freq)
            w1 = term_frequencies1[word] * idf
            length1 += w1 * w1
            if word in term_frequencies2:
                w2 = term_frequencies2[word] * idf
                length2 += w2 * w2
                dot_product += w1 * w2

        # those words in words2 that are not in words1 have not been accounted for in length of words2 vector
        for word in term_frequencies2:
            if word not in term_frequencies1:
                doc_freq = self.doc_frequency[word] if word in self.doc_frequency else 1
                idf = math.log10(self.doc_count / doc_freq)
                w2 = term_frequencies2[word] * idf
                length2 += w2 * w2

        #Normalize by dividing with lengths of both document vectors
        if length1 * length2 == 0:
            a = 2
        return dot_product / (length1 * length2)

    def __get_frequencies(self, words):
        # converts a list of words to a dictionary of frequencies of each word
        freqs = dict()
        for word in words:
            if word in freqs:
                freqs[word] += 1
            else:
                freqs[word] = 1
        return freqs

    def train_from_text(self, words):
        # Adds 1 to the document frequency of each word that is contained in the document
        self.doc_count += 1
        for word in words:
            if word in self.doc_frequency:
                self.doc_frequency[word] += 1
            else:
                self.doc_frequency[word] = 1



