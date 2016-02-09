from wordextractor import WordExtractor
import math

class NGramPerplexity:
# Calculates the perplexity of a given query string, according to the ngrams learned by the model.
# See section 3.2 at http://www.hindawi.com/journals/tswj/2014/745485/

    ngram_size = 2

    def __init__(self):
        self.ngrams = dict()
        self.size = 0

    def reset(self):
        self.ngrams.clear()
        self.size = 0

    def train_from_text(self, words):
        # Learn an n-gram model from a string
        for i in range(0, len(words) - self.ngram_size + 1):
            self.size += 1
            ngram = ",".join(words[i:i+self.ngram_size])
            if ngram in self.ngrams:
                self.ngrams[ngram] += 1
            else:
                self.ngrams[ngram] = 1

    def calc_perplexity(self, words):
        # Calculates the perplexity of a given query string, according to the ngrams learned by the model.
        # First, make an ngram model of query string
        query_ngrams = dict()
        query_size = 0
        alpha = 1 # bias count

        for i in range(0, len(words) - self.ngram_size + 1):
            ngram = ",".join(words[i:i+self.ngram_size])
            if ngram in self.ngrams:
                query_size += 1
            if ngram in query_ngrams:
                query_ngrams[ngram] += 1
            else:
                query_ngrams[ngram] = 1

        # we add a bias of every ngram seen 0.1 times
        query_size += alpha * len(self.ngrams)

        #calc perplexity by comparing ngram model of query string with learned ngram model
        entropy = 0

        for ngram,count in self.ngrams.items():
            # entropy -= p(w) * log q(w)
            pw = count / self.size
            seen = alpha
            if ngram in query_ngrams:
                seen += query_ngrams[ngram]
            entropy -= pw * math.log(seen / query_size)
        return math.pow(2, entropy)
