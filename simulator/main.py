from simulator.agent import *
from simulator.intersection import *
from simulator.state import *

i1 = Intersection((2, 5))
i2 = Intersection((1, 4))
i3 = Intersection((6, 2))
i4 = Intersection((1, 2))
i5 = Intersection((7, 6))

d1 = Intersection((1, 1), depot=True)

r1 = Road((i1, i2), 800)
r2 = Road((i2, i3), 1200)
r3 = Road((i1, i5), 300)
r4 = Road((i1, i3), 400)
r5 = Road((i4, i2), 700)
r6 = Road((i5, i1), 1000)
r7 = Road((d1, i3), 600)

p1 = Pickup("Pickup 1", (r1, 0), 1, 1)
p2 = Pickup("Pickup 2", (r2, 200), 1, 1)

a1 = Agent("Agent 1", 'g', (r3, 250), 10000, 10000, 10, 0, 400, [i1, p1, i2, p2, i3, d1], None)

problem_state = ProblemState([i1, i2, i3, i4, i5, d1], [r1, r2, r3, r4, r5, r6, r7], [a1], [p1, p2])

arena = Arena(problem_state)
# arena.build()
# arena.draw()

state = State(problem_state, 1, 1, 0)

for i in range(30):
    problem_state = state.next_state()
    arena.problem_state = problem_state

    if i % 1 == 0:

        arena.build()

        # arena.draw(True, "figures/fig" + str(i).zfill(3))
        arena.draw()
