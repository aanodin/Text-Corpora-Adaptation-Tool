from levenshtein import Levenshtein
from tfidf import TFIDF
from ngramperplexity import NGramPerplexity
from wordextractor import WordExtractor
from formatter import Formatter
from runconfiguration import *
import os

class DomainSimilarity:

    def __init__(self, input_dir, threshold_tfidf, threshold_perplexity_ngram, threshold_edit_distance):
        self.threshold_tfidf = 1-threshold_tfidf
        self.threshold_perplexity_ngram = threshold_perplexity_ngram
        self.threshold_edit_distance = threshold_edit_distance
        self.input_dir = input_dir
        self.sentences = []
        if not os.path.isdir(input_dir):
            raise Exception("The provided dir " + str(input_dir) + " does not exist")
        self.__train_models()

        self.queries_asked = 0
        self.sentences_asked = 0
        self.accepted_by_tfidf = 0
        self.accepted_by_ngp = 0
        self.accepted_by_edit_distance = 0
        self.sum_tfidf = 0
        self.sum_ngp = 0
        self.sum_edit = 0

    def __train_models(self):
        # Now load all sentences from specific domain, and train TFIDF model and NGramPerplexity model.
        self.ngp = NGramPerplexity()
        self.tfidf = TFIDF()
        print("Training models from specific corpora")
        for file in os.listdir(self.input_dir):
            print("Training models from specific corpora: " + file)
            with open(self.input_dir + "/" + file, encoding="utf-8") as input:
                for line in input:
                    words = WordExtractor.get_words(line)
                    if len(words) == 0:
                        continue
                    self.sentences.append(words)
                    self.ngp.train_from_text(words)
                    self.tfidf.train_from_text(words)

    def print_progress(self):
        print("Average tfidf: " + str(1 - self.sum_tfidf / self.queries_asked))
        print("Average ngram-perplexity: " + str(self.sum_ngp / self.sentences_asked))
        print("Average edit-distance: " + str(self.sum_edit / self.queries_asked))
        print("Accept percent by tfidf extractor: " + Formatter.percent(self.accepted_by_tfidf / self.sentences_asked))
        print("Accept percent by ngram-perplexity extractor: " + Formatter.percent(self.accepted_by_ngp / self.sentences_asked))
        print("Accept percent by edit-distance extractor: " + Formatter.percent(self.accepted_by_edit_distance / self.sentences_asked))

    def accepts_sentence(self, words_general):
        # sentence_general: string
        # Returns True if similarity of sentence_general is either:
        # > threshold1 according to tf-idf of one of stored sentences
        # > threshold2 according to ngramperplexity of one of stored sentences
        # > threshold3 according to levenshtein of one of stored sentences
        self.sentences_asked += 1
        accept_ngp = False
        accept_tfidf = False
        accept_edit_distance = False

        perplexity = self.ngp.calc_perplexity(words_general)
        self.sum_ngp += perplexity
        if perplexity <= self.threshold_perplexity_ngram:
            if RUN_CONFIGURATION.mode == MODE.TURBO:
                return True
            self.accepted_by_ngp += 1
            accept_ngp = True

        for words_specific in self.sentences:
            self.queries_asked += 1
            if accept_tfidf and accept_edit_distance:
                return True
            if not accept_tfidf:
                sim = self.tfidf.calc_cosine_similarity(words_general, words_specific)
                self.sum_tfidf += sim
                if sim >= self.threshold_tfidf:
                    if RUN_CONFIGURATION.mode == MODE.TURBO:
                        return True
                    self.accepted_by_tfidf += 1
                    accept_tfidf = True
            if not accept_edit_distance:
                edit_distance = Levenshtein.normalized_distance(words_general, words_specific)
                self.sum_edit += edit_distance
                if edit_distance <= self.threshold_edit_distance:
                    if RUN_CONFIGURATION.mode == MODE.TURBO:
                        return True
                    self.accepted_by_edit_distance += 1
                    accept_edit_distance = True

        if accept_tfidf or accept_ngp or accept_edit_distance:
            return True

        return False
