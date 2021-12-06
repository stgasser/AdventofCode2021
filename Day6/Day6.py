import numpy as np
from collections import Counter


def parse_input(filename):
    return Counter(np.fromfile(filename, sep=',', dtype=int))


def part1(fishes, days=80):
    queue = [0, 0]
    for day in range(days):
        new_fishes = Counter({6: queue.pop(0)})
        for countdown in fishes:
            if countdown == 0:
                new_fishes[6] += fishes[countdown]
                queue.append(fishes[countdown])
            else:
                new_fishes[countdown - 1] += fishes[countdown]
        if len(queue) < 2:
            queue.append(0)
        fishes = new_fishes
    return sum([v for k, v in fishes.items()]) + sum(queue)


if __name__ == '__main__':
    data = parse_input('Day6.in')
    print(part1(data))
    print(part1(data, days=256))
