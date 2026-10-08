import matplotlib.pyplot as plt
import random
import math

NUM_AGENTS = 200
BOX_SIZE = 800
INFECT_DIST = 10
DT = 0.125

class Agent:
    def __init__(self, infected=False):
        self.x = random.uniform(0, BOX_SIZE)
        self.y = random.uniform(0, BOX_SIZE)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.infected = infected

    def move(self):
        self.x += self.vx * DT
        self.y += self.vy * DT
        if self.x < 0 or self.x > BOX_SIZE: self.vx *= -1
        if self.y < 0 or self.y > BOX_SIZE: self.vy *= -1

agents = [Agent(False) for _ in range(NUM_AGENTS - 1)] + [Agent(True)]

plt.ion()
fig, ax = plt.subplots(figsize=(6,6))

for step in range(3000):
    ax.clear()
    ax.set_xlim(0, BOX_SIZE); ax.set_ylim(0, BOX_SIZE)
    ax.set_title(f"Эпидемия. Шаг {step}")
    
    for a in agents: a.move()
    
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            a1, a2 = agents[i], agents[j]
            if a1.infected != a2.infected:
                dist = math.hypot(a1.x - a2.x, a1.y - a2.y)
                if dist < INFECT_DIST:
                    a1.infected = a2.infected = True

    x_h = [a.x for a in agents if not a.infected]
    y_h = [a.y for a in agents if not a.infected]
    x_i = [a.x for a in agents if a.infected]
    y_i = [a.y for a in agents if a.infected]
    
    ax.scatter(x_h, y_h, c='blue'); ax.scatter(x_i, y_i, c='red')
    plt.pause(0.02)

plt.ioff()
plt.show()