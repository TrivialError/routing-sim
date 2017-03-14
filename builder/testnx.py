from builder.arena import Arena
from simulator.agent import *
from simulator.intersection import *
from simulator.road import *
from simulator.pickup import *
from common import *

i1 = Intersection((2, 5))
i2 = Intersection((1, 4))
i3 = Intersection((6, 2))
i4 = Intersection((1, 2))
i5 = Intersection((7, 6))

d1 = Intersection((1, 1), depot=True)

r1 = Road((i1, i2), 800)
r2 = Road((i2, i4), 1200)
r3 = Road((i1, i5), 300)
r4 = Road((i1, i3), 400)
r5 = Road((i4, i2), 700)
r6 = Road((i5, i1), 1000)
r7 = Road((d1, i3), 600)

p1 = Pickup((r1, 100), 1, 1)
p2 = Pickup((r2, 200), 1, 1)

a1 = Agent((r3, 250), 2000, 10, 10, (i1, i2, i3, d1), None)

problem_state = ProblemState([i1, i2, i3, i4, i5, d1], [r1, r2, r3, r4, r5, r6, r7], [a1], [p1, p2])

a = Arena(problem_state)
a.build()

a.draw()
