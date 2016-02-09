import array


class Levenshtein:
    # This class is an implementation of the Edit distance method described in section 3.3 of
    # http://www.hindawi.com/journals/tswj/2014/745485/


    @staticmethod
    def normalized_distance(s1, s2):
        # Returns a value in range [0,1]
        # 0 for equal strings
        # 1 for most possible different string
        if (len(s1) == 0 and len(s2) == 0):
            return 0
        else:
            return Levenshtein.distance(s1, s2) / max(len(s1), len(s2))

    @staticmethod
    def distance(s1, s2):
        # degenerate cases
        if s1 == s2:
            return 0
        if len(s2) == 0:
            return len(s1)
        if len(s1) == 0:
            return len(s2)

        # create two work vectors of integer distances
        v0 = array.array('i',(0,)*(len(s2) + 1))
        v1 = array.array('i',(0,)*(len(s2) + 1))

        # initialize v0 (the previous row of distances)
        # this row is A[0][i]: edit distance for an empty s
        # the distance is just the number of characters to delete from t
        for i in range(0, len(v0)):
            v0[i] = i

        for i in range(0, len(s1)):
            # calculate v1 (current row distances) from the previous row v0

            # first element of v1 is A[i+1][0]
            #   edit distance is delete (i+1) chars from s to match empty t
            v1[0] = i + 1

            # use formula to fill in the rest of the row
            for j in range(0, len(s2)):
                cost = 0 if s1[i] == s2[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

            # copy v1 (current row) to v0 (previous row) for next iteration
            for j in range(0, len(v0)):
                v0[j] = v1[j]

        return v1[len(s2)]