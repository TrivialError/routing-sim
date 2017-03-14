class Pickup:

    # position is a tuple of a road and an integer showing distance travelled along that road
    def __init__(self, position, priority, size):
        self.position = position
        self.priority = priority
        self.size = size
