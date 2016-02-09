from ngramperplexity import NGramPerplexity
from wordextractor import WordExtractor

NGramPerplexity.ngram_size = 3
ngp = NGramPerplexity()
ngp.train_from_text(WordExtractor.get_words("There are so many people at the beach"))
ngp.train_from_text(WordExtractor.get_words("The beach is so crowded with all these people, I wish they would just go to another beach"))
ngp.train_from_text(WordExtractor.get_words("It is summer and a great day to go to the beach."))
ngp.train_from_text(WordExtractor.get_words("Let's go to the beach and enjoy the great weather we've got today."))
ngp.train_from_text(WordExtractor.get_words("I think the first thing I will do at the beach is to buy an ice cream."))
ngp.train_from_text(WordExtractor.get_words("There's many people at the beach today, I think they are enjoying their holidays."))
ngp.train_from_text(WordExtractor.get_words("I think something is going on at the beach right now, there are literally people everywhere."))

#sentences with great similarity
very_similar_sentences = [WordExtractor.get_words("The weather is great at the beach!"),
                          WordExtractor.get_words("something is probably going on at the beach right now."),
                          WordExtractor.get_words("I think they would like an ice cream to enjoy at the beach.")]

slightly_similar_sentences = [WordExtractor.get_words("Great day today, I want to run a long distance"),
                            WordExtractor.get_words("It is expensive to buy too many things"),
                            WordExtractor.get_words("These people are new to me, I have never seen them before.")]

different_sentences = [[],
                       WordExtractor.get_words("I play guitar in a band, but I better like to play piano"),
                       WordExtractor.get_words("The Jaguar is a very dangerous animal, that can run very fast"),
                       WordExtractor.get_words("Dinosaurs are extinct and we will probably never see them alive.")]


#A very similar sentence must be more similar than a slightly similar sentence
for very_similar_sentence in very_similar_sentences:
    for slightly_similar_sentence in slightly_similar_sentences:
        pp1 = ngp.calc_perplexity(very_similar_sentence)
        pp2 = ngp.calc_perplexity(slightly_similar_sentence)
        print(str(pp1) + " < " + str(pp2))
        assert(pp1 < pp2)


#A slightly similar sentence must be more similar than a different sentence
for slightly_similar_sentence in slightly_similar_sentences:
    for different_sentence in different_sentences:
        pp1 = ngp.calc_perplexity(very_similar_sentence)
        pp2 = ngp.calc_perplexity(different_sentence)
        print(str(pp1) + " < " + str(pp2))
        assert(pp1 < pp2)


#A very similar sentence must be more similar than a different sentence
for very_similar_sentence in very_similar_sentences:
    for different_sentence in different_sentences:
        pp1 = ngp.calc_perplexity(very_similar_sentence)
        pp2 = ngp.calc_perplexity(different_sentence)
        print(str(pp1) + " < " + str(pp2))
        assert(pp1 < pp2)

print("Success")


