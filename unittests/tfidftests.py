from tfidf import TFIDF
from wordextractor import WordExtractor

def calc_most_similar(tfidf, query, docs):
    best_doc = ""
    max_sim = 0
    for doc in docs:
        sim = tfidf.calc_cosine_similarity(WordExtractor.get_words(query), WordExtractor.get_words(doc))
        if sim > max_sim:
            max_sim = sim
            best_doc = doc
    return best_doc

tfidf = TFIDF()
d1 = "It is a great day today"
d2 = "The weather is absolutely great"
d3 = "It is so warm today, almost too hot"
d4 = "We're very happy with the weather today"
d5 = "It is a great day to be at the beach!"
d6 = "We should get out and enjoy the weather right now :)"
d7 = "I've bought a radio I plan to bring to the beach today"
d8 = "The beach is a bit crowded"
d9 = "There's many kids at the beach today"
d10 = "If it starts to rain at the beach, I will go home"

documents = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]
for doc in documents:
    words = WordExtractor.get_words(doc)
    tfidf.train_from_text(words)

q1 = "We have not had rain for a long time!"
q2 = "Where can I buy a radio?"
q3 = "The kids are happy to be at the beach."

assert(calc_most_similar(tfidf, q1, documents) == d10)
assert(calc_most_similar(tfidf, q2, documents) == d7)
assert(calc_most_similar(tfidf, q3, documents) == d5)

print("Success")

