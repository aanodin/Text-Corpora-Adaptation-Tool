from levenshtein import Levenshtein

assert(Levenshtein.distance("", "abc") == 3)
assert(Levenshtein.distance("abc", "") == 3)
assert(Levenshtein.distance("", "") == 0)
assert(Levenshtein.distance("abc", "abc") == 0)
assert(Levenshtein.distance("abcdef", "xxxxxx") == 6)
assert(Levenshtein.distance("xxxxxx", "abcdef") == 6)
assert(Levenshtein.distance("abcdef", "abefcd") == 4)
assert(Levenshtein.distance("abefcd", "abcdef") == 4)
assert(Levenshtein.distance("acdefg", "abcdef") == 2)
assert(Levenshtein.distance("abcdef", "acdefg") == 2)

assert(Levenshtein.normalized_distance("abcdef", "abc") == 0.5)
assert(Levenshtein.normalized_distance("abcdef", "") == 1)
assert(Levenshtein.normalized_distance("a", "b") == 1)
assert(Levenshtein.normalized_distance("a", "") == 1)
assert(Levenshtein.normalized_distance("a", "a") == 0)
assert(Levenshtein.normalized_distance("abcd", "c") == 0.75)
assert(Levenshtein.normalized_distance("abcd", "bd") == 0.5)
assert(Levenshtein.normalized_distance("abcd", "db") == 0.75)

print("Success")