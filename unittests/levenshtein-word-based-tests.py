from levenshtein import Levenshtein
# A more through general test is found in levenshteintests.py
# This test is only to show that word based distance works the same way as character based distance

assert(Levenshtein.distance(["hi", "there"], ["hi"]) == 1)
assert(Levenshtein.distance(["hi", "there"], ["there", "hi"]) == 2)
assert(Levenshtein.distance(["hi", "there"], []) == 2)
assert(Levenshtein.distance(["aaa", "bbbb", "cccc"], ["aaa", "fff", "cccc"]) == 1)
assert(Levenshtein.distance([], []) == 0)

print("Success")