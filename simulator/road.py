from common import *


class Road:

    ends_index = dict()

    def __init__(self, ends, length, contains_pickup=False):

        self.ends = ends
        self.length = length
        self.contains_pickup = contains_pickup

        Road.ends_index[ends] = self

    @classmethod
    def find_by_ends(cls, ends):
        try:
            if ends in Road.ends_index:
                return Road.ends_index[ends]
            else:
                return Road.ends_index[(ends[1], ends[0])]
        except KeyError:
            raise StateError("Road in target route does not exist")
