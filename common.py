class ProblemState:

    def __init__(self, intersections, roads, agents, pickups):
        self.intersections = intersections
        self.roads = roads
        self.agents = agents
        self.pickups = pickups


class StateError(Exception):
    """Exception for when the simulator finds the problem in an inconsistent state"""


# Takes in a road and an integer progress showing distance travelled along that road and
#   returns a tuple giving a location coordinate
def position_to_location(road, progress):

    end1 = road.ends[0].location
    end2 = road.ends[1].location

    distance_percent = progress / road.length

    location_x = (1 - distance_percent) * end1[0] + distance_percent * end2[0]
    location_y = (1 - distance_percent) * end1[1] + distance_percent * end2[1]

    return location_x, location_y
