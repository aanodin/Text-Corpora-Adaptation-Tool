from domainsimilarity import DomainSimilarity
import os
from formatter import Formatter
from runconfiguration import *
from wordextractor import WordExtractor
import time

class DomainExtractor:

    def __init__(self, general_corpora_dir, specific_corpora_dir, output_dir):
        self.output_dir = output_dir
        self.general_corpora_dir = general_corpora_dir
        self.specific_corpora_dir = specific_corpora_dir
        self.extracted_lines = 0
        self.scanned_lines = 0
        self.assigned_lines = 0
        self.unusable_lines = 0

    def check_settings_monolingual(self):
        # Make sure input paths exists
        if not os.path.exists(os.path.dirname(self.specific_corpora_dir + "/mono/")):
            raise Exception("General corpora dir: " + self.general_corpora_dir + "/mono does not exist")
        if not os.path.exists(os.path.dirname(self.general_corpora_dir + "/mono/")):
            raise Exception("Specific corpora dir: " + self.specific_corpora_dir + "/mono does not exist")
        # Create output path if necessary
        if RUN_CONFIGURATION.workers > 1:
            self.output_file_mono = self.output_dir + "/mono-"+str(RUN_CONFIGURATION.worker_id)+".txt"
        else:
            self.output_file_mono = self.output_dir + "/mono.txt"
        if not os.path.exists(os.path.dirname(self.output_file_mono)):
            os.makedirs(os.path.dirname(self.output_file_mono))

    def check_settings_bilingual(self):
        # Make sure input paths exists
        if not os.path.exists(os.path.dirname(self.general_corpora_dir + "/en/")):
            raise Exception("General corpora dir: " + self.general_corpora_dir + "/en does not exist")
        if not os.path.exists(os.path.dirname(self.general_corpora_dir + "/pl/")):
            raise Exception("General corpora dir: " + self.general_corpora_dir + "/pl does not exist")
        if not os.path.exists(os.path.dirname(self.specific_corpora_dir + "/en/")):
            raise Exception("Specific corpora dir: " + self.specific_corpora_dir + "/en does not exist")
        if not os.path.exists(os.path.dirname(self.specific_corpora_dir + "/pl/")):
            raise Exception("Specific corpora dir: " + self.specific_corpora_dir + "/pl does not exist")
        # Create output paths if necessary
        if RUN_CONFIGURATION.workers > 1:
            self.output_file_en = self.output_dir + "/en/en-"+str(RUN_CONFIGURATION.worker_id)+".txt"
            self.output_file_pl = self.output_dir + "/pl/pl-"+str(RUN_CONFIGURATION.worker_id)+".txt"
        else:
            self.output_file_en = self.output_dir + "/en/en.txt"
            self.output_file_pl = self.output_dir + "/pl/pl.txt"
        if not os.path.exists(os.path.dirname(self.output_file_en)):
            os.makedirs(os.path.dirname(self.output_file_en))
        if not os.path.exists(os.path.dirname(self.output_file_pl)):
            os.makedirs(os.path.dirname(self.output_file_pl))

    def print_progress_summary(self):
        useful_lines = self.assigned_lines - self.unusable_lines
        print("(General corpora): Total lines scanned : " + str(self.scanned_lines))
        print("(General corpora): Lines assigned to worker: " + str(self.assigned_lines))
        print("(General corpora): Lines containing words: " + str(useful_lines))
        print("(General corpora): Extracted lines: " + str(self.extracted_lines))
        print("(General corpora): Sentence accept rate: " + Formatter.percent(self.extracted_lines / useful_lines))

    def print_progress_bilingual(self, current_file_en, current_file_pl, en_domain_similarity, pl_domain_similarity):
        self.print_progress_summary()
        print("Current extracting from files: " + current_file_en + " & " + current_file_pl)
        print("")
        if RUN_CONFIGURATION.mode == MODE.TURBO:
            return
        print("EN extractor stats:")
        en_domain_similarity.print_progress()
        print("")
        print("PL extractor stats:")
        pl_domain_similarity.print_progress()
        print("")

    def print_progress_monolingual(self, current_file, domain_similarity):
        self.print_progress_summary()
        print("Current extracting from file: " + current_file)
        print("")
        if RUN_CONFIGURATION.mode == MODE.TURBO:
            return
        print("MONO extractor stats:")
        domain_similarity.print_progress()
        print("")

    def analyze_and_output_bilingual(self, general_en, general_pl, output_en, output_pl):
        words_general_en = WordExtractor.get_words(general_en)

        # skip if not assigned to worker
        if self.scanned_lines % RUN_CONFIGURATION.workers != RUN_CONFIGURATION.worker_id - 1:
            return
        self.assigned_lines += 1

        if len(words_general_en) == 0:
            self.unusable_lines += 1
            return
        words_general_pl = WordExtractor.get_words(general_pl)
        if len(words_general_pl) == 0:
            self.unusable_lines += 1
            return

        # FOR BILINGUAL
        if RUN_CONFIGURATION.mode == MODE.STATISTICS:
            # Always run both languages in HELP mode to gather useful statistics
            en_accepts = self.domain_similarity_en.accepts_sentence(words_general_en)
            pl_accepts = self.domain_similarity_pl.accepts_sentence(words_general_pl)
            if RUN_CONFIGURATION.accept_criteria == ACCEPT_CRITERIA.BILINGUAL_EITHER:
                if not en_accepts and not pl_accepts:
                    return
            elif RUN_CONFIGURATION.accept_criteria == ACCEPT_CRITERIA.BILINGUAL_BOTH:
                if not en_accepts or not pl_accepts:
                    return
        else:
            #In TURBO mode, only run PL analysis if necessary
            en_accepts = self.domain_similarity_en.accepts_sentence(words_general_en)
            if RUN_CONFIGURATION.accept_criteria == ACCEPT_CRITERIA.BILINGUAL_EITHER:
                if not en_accepts:
                    pl_accepts = self.domain_similarity_pl.accepts_sentence(words_general_pl)
                    if not pl_accepts:
                        return
            elif RUN_CONFIGURATION.accept_criteria == ACCEPT_CRITERIA.BILINGUAL_BOTH:
                if not en_accepts:
                    return
                pl_accepts = self.domain_similarity_pl.accepts_sentence(words_general_pl)
                if not pl_accepts:
                    return

        # Write to output since all conditions are satisfied
        self.extracted_lines += 1
        output_en.write(general_en)
        output_pl.write(general_pl)

    def analyze_and_output_mono(self, general_line, output):
        # skip if not assigned to this worker
        if self.scanned_lines % RUN_CONFIGURATION.workers != RUN_CONFIGURATION.worker_id - 1:
            return
        self.assigned_lines += 1

        words_general = WordExtractor.get_words(general_line)
        if len(words_general) == 0:
            self.unusable_lines += 1
            return

        if self.domain_similarity.accepts_sentence(words_general):
            self.extracted_lines += 1
            output.write(general_line)

    def run_mono(self, threshold_tfidf, threshold_perplexity_ngram, threshold_edit_distance):
        # Train domain similarity classes for each language in the specific domain
        self.domain_similarity = DomainSimilarity(self.specific_corpora_dir + "/mono", threshold_tfidf,
                                                   threshold_perplexity_ngram, threshold_edit_distance)

        self.check_settings_monolingual()
        start = time.time()
        # Run through all lines in big general domain, and save the good lines to output
        for file_general_mono in os.listdir(self.general_corpora_dir + "/mono"):
            file_general_mono = self.general_corpora_dir + "/mono/" + file_general_mono
            with open(self.output_file_mono, "w+", encoding="utf8") as output_mono:
                with open(file_general_mono, encoding="utf8") as general_mono:
                    for mono_line in general_mono:
                        self.scanned_lines += 1
                        self.analyze_and_output_mono(mono_line, output_mono)
                        if self.scanned_lines % 100 == 0 and self.scanned_lines > 0:
                            self.print_progress_monolingual(file_general_mono, self.domain_similarity)
        print("Time elapsed: " + str(time.time() - start))
        print("*** Finished, extracting a total of " + str(self.extracted_lines) + " lines ***")

    def run_bilingual(self, threshold_en_tfidf, threshold_en_perplexity_ngram, threshold_en_edit_distance,
            threshold_pl_tfidf, threshold_pl_perplexity_ngram, threshold_pl_edit_distance):

        self.check_settings_bilingual()
        # Train domain similarity classes for each language in the specific domain
        self.domain_similarity_en = DomainSimilarity(self.specific_corpora_dir + "/en", threshold_en_tfidf,
                                                     threshold_en_perplexity_ngram, threshold_en_edit_distance)
        self.domain_similarity_pl = DomainSimilarity(self.specific_corpora_dir + "/pl", threshold_pl_tfidf,
                                                     threshold_pl_perplexity_ngram, threshold_pl_edit_distance)
        start = time.time()
        # Run through all lines in big general domain, and save the good lines to output
        # First, run through all EN files in general domain
        for file_general_en in os.listdir(self.general_corpora_dir + "/en"):
            file_general_pl = self.general_corpora_dir + "/pl/" + file_general_en[:len(file_general_en)-2] + "pl"
            file_general_en = self.general_corpora_dir + "/en/" + file_general_en
            if not os.path.isfile(file_general_pl):
                print("Skipping general file: " + file_general_en + " because no PL equivalent exists")
                continue
            with open(self.output_file_en, "w+", encoding="utf8") as output_en:
                with open(self.output_file_pl, "w+", encoding="utf8") as output_pl:
                    with open(file_general_en, encoding="utf8") as general_en:
                        with open(file_general_pl, encoding="utf8") as general_pl:
                            for en_line in general_en:
                                self.scanned_lines += 1
                                pl_line = general_pl.readline()
                                self.analyze_and_output_bilingual(en_line, pl_line, output_en, output_pl)
                                if self.scanned_lines % 100 == 0 and self.scanned_lines > 0:
                                    self.print_progress_bilingual(file_general_en, file_general_pl,
                                                                  self.domain_similarity_en, self.domain_similarity_pl)
        print("Time elapsed: " + str(time.time() - start))
        print("*** Finished, extracting a total of " + str(self.extracted_lines) + " lines ***")