from domainextractor import DomainExtractor
from enums import SIMILARITY_ACCEPT_CRITERIA
from ngramperplexity import NGramPerplexity

general_corpora_dir = "corpora/big"
specific_corpora_dir = "corpora/small"
output_file_en = "corpora/output/output.en"
output_file_pl = "corpora/output/output.pl"

NGramPerplexity.ngram_size = 2
sim_accept_criteria = SIMILARITY_ACCEPT_CRITERIA.BOTH_LANGUAGES

threshold_en_tfidf = 0.963 # range [0.0,1.0]: lower value = more similar data extracted
threshold_en_perplexity_ngram = 458 # range [0.0,infinite]: lower value = more similar data extracted
threshold_en_edit_distance = 0.86  # range [0.0,1.0]: lower value = more similar data extracted
threshold_pl_tfidf = 0.994 # range [0.0,1.0]: lower value = more similar data extracted
threshold_pl_perplexity_ngram = 465.404 # range [0.0,infinite]: lower value = more similar data extracted
threshold_pl_edit_distance = 0.90  # range [0.0,1.0]: lower value = more similar data extracted




domain_extractor = DomainExtractor(general_corpora_dir, specific_corpora_dir, output_file_en, output_file_pl)
domain_extractor.run(threshold_en_tfidf, threshold_en_perplexity_ngram, threshold_en_edit_distance,
                     threshold_pl_tfidf, threshold_pl_perplexity_ngram, threshold_pl_edit_distance,
                     sim_accept_criteria)