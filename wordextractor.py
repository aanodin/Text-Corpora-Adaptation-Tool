import re

class WordExtractor:

    concatenations = {
        "you're" : "you are",
        "we're" : "we are",
        "he's" : "he is",
        "she's" : "she is"
    }

    def get_words(str):
        #returns a list of all words found in the sentence

        str = str.lower()
        words = re.findall(r"([^\W\d_]+(?:'[^\W\d_]+)?)", str, re.UNICODE)
        end = len(words)
        i = 0
        while i < end:
            deapostrophized = WordExtractor.__deapostrophize(words[i])
            if deapostrophized != "":
                parts = deapostrophized.split(" ")
                words[i] = parts[0]
                words.insert(i+1, parts[1])
                end += 1
            i += 1
        return words

    def __deapostrophize(str):
        if str in WordExtractor.concatenations:
            return WordExtractor.concatenations[str]
        else:
            return ""