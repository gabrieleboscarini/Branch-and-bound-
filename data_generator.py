#Author: Gabriele Boscarini


import numpy as np
import random
import math

# data generation process

def generate_data():

    weights = [(random.randint(1, 1000)) for i in range(5)]
    profits = [(random.randint(i + 95, i + 105)) for i in weights]

    weights_normalized = [i / 21 for i in weights]
    profits_normalized = [i / 21 for i in profits]

    pairs = list(zip(weights_normalized, profits_normalized))

    with open('input.txt', 'w') as f:

        f.write("\n")

        for n in np.linspace(50, 100, 6):

            for instance in range(5):

                random_idx = [random.randint(0, len(pairs) - 1) for i in range(int(n))]
                items = [(round(pairs[random_idx[i]][0] * random.randint(1, 20)),
                          round(pairs[random_idx[i]][1] * random.randint(1, 20))) for i in range(int(n))]
                capacity = math.ceil(sum([i[1] for i in items]) / 3)
                f.write(str(int(n)) + " " + str(capacity) + "\n")
                f.write('\n'.join(f'{tup[0]} {tup[1]}' for tup in items))
                f.write("\n" + "" + "\n")



