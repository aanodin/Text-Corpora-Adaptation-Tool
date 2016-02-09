About
=====

Tool allows to conduct text domain adaptation on parallel and monolingual corpora.

In-domain data is filtered from a general corpus, by considering how similar each sentence is to a target domain. The filtration can be run as either mono­ or bilingual, by running main_monolingual.py or main_bilingual.py, respectively. In the following, when describing bilingual translation, we will consider a translation from English (EN) to Polish (PL), even though any language can be used.

Input / Output

general_corpora_dir ​should point to a directory containing the general corpora. For bilingual extraction, the directory should contain folders with the name ​en​and ​pl​, containing parallel files with equivalent names. The files in the ​en ​folder must have ​.en​extension, and files in the ​pl ​folder must have ​.pl​extension. Parallel files means that the same line in two files are translations of each other. For monolingual translation, the directory should contain a folder with the name ​mono​where corpora files are contained inside.
specific_corpora_dir ​should be organized the same way as for the general corpora, except that it contains the specific / target corpora.
output_dir​should point to where you want the output. No organization of folders is needed, it will be created automatically.

Filtration methods
=====

Each sentence (or sentence pair if bilingual extraction) from general corpora are examined, and will be extracted (kept), if one of the following 3 techniques deem it useful:

Edit distance (Levenshtein distance)
Perplexity measure (based on n­grams)
Tf-­idf (cosine similarity)

All of these 3 measures are well described in numerous articles, and Wikipedia provide a good description of all of them. The n­gram size used by the perplexity measure can be changed by the parameter ​NGramPerplexity.ngram_size​. If having a small target corpora, a value of 2 works good, but with a very large target corpora, and if the target domain is closer to the general domain, a value of up to 5 can be used. The tf­idf is converted to a distance measure by subtracting the similarity from 1. In that way, all 3 measures are distance measures. Whether a method accepts a sentence from the general domain is then based on whether the distance towards the target domain is below a given threshold.
For monolingual extraction, the thresholds are set in main_monolingual.py like this:
threshold_tfidf​​# range [0.0,1.0] threshold_perplexity_ngram​​# range [0.0,infinite] threshold_edit_distance​​# range [0.0,1.0]
Since all are distance measures, a lower value will result in more data being extracted. For bilingual extraction, there a threshold can be set for each method and each language side.
The parameters to change in main_bilingual.py are: threshold_en_tfidf,​threshold_en_perplexity_ngram, threshold_en_edit_distance, threshold_pl_tfidf, threshold_pl_perplexity_ngram, threshold_pl_edit_distance
The reason for having thresholds for both language sides, is that the extraction can be set up to accept a sentence pair from the general domain if either ​both​languages in the target domain accepts the sentence, or if just ​either​of the languages in the target domain accepts the sentence. This is determined by the ​RUN_CONFIGURATION.accept_criteria parameter, that can be set to either ​ACCEPT_CRITERIA.BILINGUAL_BOTH​or ACCEPT_CRITERIA.BILINGUAL_EITHER​.

Statistics or Turbo mode
=====

Choosing the right thresholds are not trivial. If thresholds are too low, all data is extracted, and if thresholds are too high, nothing will be extracted. A statistics mode can be used by setting the parameter ​RUN_CONFIGURATION.mode=MODE.STATISTICS​. This will cause a bit slower run time, because all 3 distance measure are evaluated on every sentence, to gather statistics. The statistics will be output for every 100 sentences scanned from the general domain. The statistics include the average distance of sentences according to each measure. The average distance is a good starting point for setting the thresholds, which is almost guaranteed to extract some, but not all sentences. Then, the thresholds can be lowered gradually. An article on the subject found an extraction close to 1 % of all sentences to give the best BLEU­score (when extracted sentences were used to train a translator).
When good thresholds have been selected, run speed can be increased by using setting the parameter ​RUN_CONFIGURATION.mode=MODE.TURBO.
In that mode, no statistics will be output. The extraction will run faster, because once a single of the 3 distance measures accepts a sentence, the remaining distance measures will not be run, since the sentence will be extracted regardless of their acceptance.

Multiple processes
=====

If running on a multicore system, or running on multiple computers, the main_monolingual.py or main_bilingual.py can be run with the parameters ​#workers #worker­id​.
For instance, if having 4 CPUs, 4 processes can be set up to distribute the work, by running the following commands one at a time:

python main_bilingual.py 4 1
python main_bilingual.py 4 2
python main_bilingual.py 4 3
python main_bilingual.py 4 4

Process 1 will then process the lines 1, 5, 9, … from the general corpora, process 2 will process the lines 2, 6, 10, … and so on. Each process will produce its own output, that can be combined after all processes have finished. There is no guarantee that each process will produce the same amount of output. For instance, if all odd lines in the general corpora only contains a number, process 1 and 3 will produce no outputs at all, since they will only be working on odd lines. If there is a such pattern in the general corpora, it might be better to use an odd number of processes, so the work is more evenly distributed.

Final info
====

Feel free to use this tool if you cite:
Wołk K., Marasek K., “PJAIT Systems for the IWSLT 2015 Evaluation Campaign Enhanced by Comparable Corpora.”, Proceedings of the 12th International Workshop on Spoken Language Translation, Da Nang, Vietnam, December 3-4, 2015, p.101-104

For more information, see: http://arxiv.org/pdf/1512.01639

For any questions:
| Krzysztof Wolk
| krzysztof@wolk.pl
