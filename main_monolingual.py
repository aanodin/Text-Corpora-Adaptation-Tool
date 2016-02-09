from domainextractor import DomainExtractor
from runconfiguration import *
from ngramperplexity import NGramPerplexity
import sys

general_corpora_dir = "corpora/big"
specific_corpora_dir = "corpora/small"
output_dir = "corpora/output/monolingual"

NGramPerplexity.ngram_size = 2
RUN_CONFIGURATION.mode = MODE.STATISTICS
if len(sys.argv) > 1:
    RUN_CONFIGURATION.workers = int(sys.argv[1]) # Number of workers
    RUN_CONFIGURATION.worker_id = int(sys.argv[2]) # Current worker id, should be >= 1 and <= number of workers

threshold_tfidf = 0.963 # range [0.0,1.0]: lower value = more similar data extracted
threshold_perplexity_ngram = 458 # range [0.0,infinite]: lower value = more similar data extracted
threshold_edit_distance = 0.80  # range [0.0,1.0]: lower value = more similar data extracted

domain_extractor = DomainExtractor(general_corpora_dir, specific_corpora_dir, output_dir)
domain_extractor.run_mono(threshold_tfidf, threshold_perplexity_ngram, threshold_edit_distance)