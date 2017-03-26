class Intersection:

    # location is a tuple of two coordinates
    def __init__(self, location, depot=False):

        self.location = location
        self.depot = depot

    def __str__(self):
        return str(self.location)

    def __repr__(self):
        return str(self.location)