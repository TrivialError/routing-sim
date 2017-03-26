class Agent:

    # position is a tuple of a road and an integer showing distance travelled along that road
    # speed is speed in m/s
    # route is a list of intersections defining a target route
    def __init__(self, name, color, position, travel_range, total_range, capacity, payload, speed, route, agent_type):
        self.name = name
        self.color = color
        self.position = position
        self.range = travel_range
        self.total_range = total_range
        self.capacity = capacity
        self.payload = payload
        self.speed = speed
        self.route = route
        self.agent_type = agent_type

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
