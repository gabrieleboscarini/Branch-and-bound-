# Author: Gabriele Boscarini 2063145

import timeit
from tabulate import tabulate


class item():

    def __init__(self, profit, weight, index):
        self.profit = profit
        self.weight = weight
        self.relative_profit = self.profit / self.weight
        self.index = index


class Node():

    def __init__(self, level, constraints, w, items_list):
        self.level = level
        self.x_opt, self.upper_bound, self.relaxation_index = relaxation_solver(items_list, w, constraints)


def dot_product(items_list, l):
    k = [x.profit for x in items_list]

    if len(k) != len(l):
        return 0

    return sum(i[0] * i[1] for i in zip(k, l))


def relaxer(direction, relaxation_index, x_opt):
    new_constraints = x_opt.copy()

    if not isinstance(x_opt[relaxation_index], int):
        if direction == 0:
            new_constraints[relaxation_index] = 0
        else:
            new_constraints[relaxation_index] = 1

    return new_constraints


def relaxation_solver(items_list, w: int, x_opt):
    items_list_sorted = [i for i in items_list if x_opt[i.index] == 1]

    items_list_sorted.sort(key=lambda x: x.relative_profit, reverse=True)

    current_w = items_list_sorted[0].weight

    relaxation_index = 0

    for s in range(len(items_list_sorted)):

        if current_w < w:
            x_opt[items_list_sorted[s].index] = 1
            if s + 1 < len(items_list_sorted):
                current_w += items_list_sorted[s + 1].weight
        else:
            critical_element = (w - sum(i.weight for i in items_list_sorted[:s])) / items_list_sorted[s].weight
            if critical_element == 1:
                critical_element = int(critical_element)
            x_opt[items_list_sorted[s].index] = critical_element
            relaxation_index = items_list_sorted[s].index
            break

    upper_bound = dot_product(items_list, x_opt)

    return x_opt, upper_bound, relaxation_index


# implementation of branch and bound algorithm


def branch_and_bound(items_list, w):

    start = timeit.default_timer()

    number_of_nodes = 1

    # initialize root
    solved = True
    gap = 0
    level = 0
    z_opt = 0
    x_opt = [1 for i in range(len(items_list))]
    root = Node(level, x_opt, w, items_list)
    queue = []

    if root.upper_bound > z_opt and isinstance(root.upper_bound, int):
        x_opt = root.x_opt
        z_opt = root.upper_bound

    if root.upper_bound > z_opt:
        queue.append(root)

    while queue:

        t = queue.pop()

        for i in range(2):
            level += 1

            if i == 0:

                child = Node(level, relaxer(0, t.relaxation_index, t.x_opt), w, items_list)

            else:

                child = Node(level, relaxer(1, t.relaxation_index, t.x_opt), w, items_list)

            number_of_nodes += 1

            if isinstance(child.upper_bound, int) and child.upper_bound > z_opt:

                x_opt = child.x_opt
                z_opt = child.upper_bound

                for j in range(len(queue)):
                    if queue[j].upper_bound <= z_opt:
                        queue.remove(j)

            if child.upper_bound > z_opt:
                if child.x_opt != t.x_opt:
                    queue.append(child)

        stop = timeit.default_timer()
        if(stop-start) == 300:
            gap = z_opt
            solved = False

    if solved:
        optimality_gap = 0
    else:
        optimality_gap = z_opt - gap

    stop1 = timeit.default_timer()

    return x_opt, z_opt, number_of_nodes, stop1 - start, optimality_gap, solved


if __name__ == "__main__":

    # importing data from the input file

    with open("input.txt", "r") as f:
        file = [row.split() for row in f]

    # writing solutions in the output file

    data = []

    with open("output.txt", "w") as f:

        instance = 0

        for i in range(len(file)):

            if not file[i]:

                if i == len(file) - 1:
                    break

                if instance == 5:
                    instance = 0

                instance += 1

                capacity = int(file[i + 1][1])
                n_items = int(file[i + 1][0])
                items_list = [item(int(file[n + i + 2][0]), int(file[n + i + 2][1]), n) for n in range(n_items)]
                solutions, profit, nodes, time, optimality_gap, solved = branch_and_bound(items_list, capacity)

                data.append([str(instance), str(n_items), str(nodes), str(time), str(optimality_gap), str(solved)])

                f.write(str(profit) + "\n")
                f.write('\n'.join(f'{x}' for x in solutions))
                f.write("\n" + "" + "\n")

    print(tabulate(data, headers=["instance", "n_items", "nodes", "Time", "optimality_gap", "Solved"]))
