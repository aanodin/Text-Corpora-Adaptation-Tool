from domainextractor import DomainExtractor
from runconfiguration import *
from ngramperplexity import NGramPerplexity
import sys

general_corpora_dir = "corpora/big"
specific_corpora_dir = "corpora/small"
output_dir = "corpora/output/bilingual"

NGramPerplexity.ngram_size = 2
RUN_CONFIGURATION.mode = MODE.STATISTICS
RUN_CONFIGURATION.accept_criteria = ACCEPT_CRITERIA.BILINGUAL_BOTH
if len(sys.argv) > 1:
    RUN_CONFIGURATION.workers = int(sys.argv[1]) # Number of workers
    RUN_CONFIGURATION.worker_id = int(sys.argv[2]) # Current worker id, should be >= 1 and <= number of workers

threshold_en_tfidf = 0.963 # range [0.0,1.0]: lower value = more similar data extracted
threshold_en_perplexity_ngram = 458 # range [0.0,infinite]: lower value = more similar data extracted
threshold_en_edit_distance = 0.86  # range [0.0,1.0]: lower value = more similar data extracted
threshold_pl_tfidf = 0.994 # range [0.0,1.0]: lower value = more similar data extracted
threshold_pl_perplexity_ngram = 465.404 # range [0.0,infinite]: lower value = more similar data extracted
threshold_pl_edit_distance = 0.90  # range [0.0,1.0]: lower value = more similar data extracted

domain_extractor = DomainExtractor(general_corpora_dir, specific_corpora_dir, output_dir)
domain_extractor.run_bilingual(threshold_en_tfidf, threshold_en_perplexity_ngram, threshold_en_edit_distance,
                     threshold_pl_tfidf, threshold_pl_perplexity_ngram, threshold_pl_edit_distance)