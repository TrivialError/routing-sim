from builder.arena import *
from simulator.road import *
from simulator.pickup import *
from generator.generator import *
import numpy.random as rand

PICKUP_SIZE_AVG = 2


class State:

    # problem_state is a ProblemState object with the map information
    # sim_interval is the amount of simulated time between each generated state in seconds
    # pickup_rate is the probability that a new pickup will be generated each second.
    # new_pickup indicates whether a new pickup has been generated in the last state update,
    #   and should be set back to False once addressed
    # time is the amount of simulated time that has passed in seconds
    def __init__(self, problem_state, pickup_rate, sim_interval, time):
        self.problem_state = problem_state

        self.pickup_rate = pickup_rate
        self.sim_interval = sim_interval
        self.time = time

        self.new_pickup = False

    # Processes the new state after one sim_interval
    def next_state(self, gen_pickups=True):

        self.move_agents()

        if gen_pickups:
            self.gen_pickups()

        if self.new_pickup:
            self.get_targets()
            self.new_pickup = False

        self.time += self.sim_interval

        return self.problem_state

    def move_agents(self):

        for agent in self.problem_state.agents:

            travel_left = agent.speed * self.sim_interval

            while agent.route and travel_left != 0:
                next_dest = agent.route[0]

                if next_dest != agent.position[0].ends[0] and next_dest != agent.position[0].ends[1]:

                    if isinstance(next_dest, Pickup):
                        if next_dest.position[0] != agent.position[0]:
                            raise StateError("Next destination: pickup " + next_dest.position +
                                             " in agent " + agent.name + "'s route not on current road")
                        else:
                            progress = agent.position[1]

                            if next_dest.position[1] < progress:
                                reverse = True
                            elif next_dest.position[1] > progress:
                                reverse = False
                            else:
                                agent.position[0].contains_pickup = False
                                agent.payload += next_dest.size
                                self.problem_state.pickups.remove(next_dest)
                                agent.route.pop(0)
                                continue

                            road_length = abs(progress - next_dest.position[1])

                    else:
                        raise StateError("Next destination: intersection " + next_dest.location +
                                         " in agent " + agent.name + "'s route not on current road")
                else:
                    progress = agent.position[1]

                    if next_dest == agent.position[0].ends[1]:
                        road_length = Road.find_by_ends(agent.position[0].ends).length - progress
                        reverse = False
                    else:
                        road_length = progress
                        reverse = True

                current_road = agent.position[0]

                travelled = min(road_length, travel_left)
                travel_left -= travelled

                agent.range -= travelled

                if reverse:
                    progress -= travelled
                else:
                    progress += travelled

                if travel_left != 0:

                    if isinstance(next_dest, Pickup):
                        agent.position[0].contains_pickup = False
                        agent.payload += next_dest.size
                        self.problem_state.pickups.remove(next_dest)
                        agent.route.pop(0)
                    else:
                        last_intersection = agent.route.pop(0)
                        if agent.route:
                            next_dest = agent.route[0]
                            if isinstance(next_dest, Pickup):
                                if last_intersection == next_dest.position[0].ends[1]:
                                    next_intersection = next_dest.position[0].ends[0]
                                elif last_intersection == next_dest.position[0].ends[0]:
                                    next_intersection = next_dest.position[0].ends[1]
                                else:
                                    raise StateError("Next destination: pickup " + next_dest.position +
                                                     " in agent " + agent.name + "'s route not on current road")
                            else:
                                next_intersection = next_dest

                            current_road = Road.find_by_ends((last_intersection, next_intersection))

                            if next_intersection == current_road.ends[1]:
                                progress = 0
                            else:
                                progress = current_road.length

                if agent.range < 0:
                    raise StateError("Agent " + agent.name +
                                     " has negative travel range (i.e. travelled farther than capable)")
                if agent.payload > agent.capacity:
                    raise StateError("Agent " + agent.name +
                                     " has too many pickups")

                agent.position = (current_road, progress)

    def gen_pickups(self):

        gen_average = self.pickup_rate * self.sim_interval
        num_pickups = rand.poisson(gen_average)
        for i in range(num_pickups):
            pickup_size = rand.poisson(PICKUP_SIZE_AVG)
            roads = self.problem_state.roads
            length_sum = sum(map(lambda x: x.length, roads))
            road_prob = list(map(lambda x: x.length / length_sum, roads))

            pickup_road = rand.choice(roads, p=road_prob)
            pickup_road.contains_pickup = True

            progress = rand.uniform(0, pickup_road.length)
            pickup_position = (pickup_road, progress)
            pickup_pri = rand.uniform(0, 5)

            new_pickup = Pickup(str(Pickup.number), pickup_position, pickup_pri, pickup_size)

            self.problem_state.pickups.append(new_pickup)
            self.new_pickup = True

    def get_targets(self):
        generator = Generator(self.problem_state)

        generator.generate_problem_instance()
