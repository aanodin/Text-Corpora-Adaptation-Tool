class Formatter:
    @staticmethod
    def percent(val):
        return "{0:.2f}".format(val * 100) + " %"