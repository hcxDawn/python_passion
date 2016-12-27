import numpy as np
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # total_steps = 1000
    # position = 0
    # walk = []
    # for i in range(total_steps):
    #     step = random.randint(-1, 1)
    #     position += step
    #     walk.append(position)
    # plt.plot(range(total_steps), walk)
    # plt.show()

    nsteps = 1000
    draws = np.random.randint(0, 2, size=nsteps)
    # print(draws)
    steps = np.where(draws > 0, 1, -1)
    # print(steps)
    walk = steps.cumsum()
    # print(walk)s
    plt.plot(range(1000), walk)
    plt.show()