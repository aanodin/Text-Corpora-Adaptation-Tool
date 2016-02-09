# If set to Turbo, optimizations are made to process data as quick as possible
# If set to Help, different statistics are gathered for each extraction method. In that way, even if one
# extraction method has already accepted a string, the other methods are run to carry statistics.
class MODE:
    TURBO = 1,
    STATISTICS = 2

class ACCEPT_CRITERIA: # Only used for bilingual extraction
    BILINGUAL_BOTH = 1
    BILINGUAL_EITHER = 2

class RUN_CONFIGURATION:
    mode = MODE.STATISTICS
    accept_criteria = ACCEPT_CRITERIA.BILINGUAL_BOTH
    workers = 1 # total number of processes you plan to run
    worker_id = 1 # must be >= 1, <= value of workers





