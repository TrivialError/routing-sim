class Pickup:

    number = 0

    # position is a tuple of a road and an integer showing distance travelled along that road
    def __init__(self, name, position, priority, size):
        self.name = name
        self.position = position
        self.priority = priority
        self.size = size

        Pickup.number += 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
