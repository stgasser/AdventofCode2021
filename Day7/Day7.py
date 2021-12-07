import numpy as np


def parse_input(filename):
    return np.fromfile(filename, dtype=int, sep=',')


def get_fuel_costs(d, m):
    return abs(d - m).sum()


def part1(depths: np.ndarray, cost=get_fuel_costs):
    m = int(depths.mean())
    while True:
        c = cost(depths, m)
        if cost(depths, m + 1) < c:
            m += 1
        elif cost(depths, m - 1) < c:
            m -= 1
        else:
            return c


def get_squared_costs(d, m):
    dif = abs(d - m)
    return int((dif * (dif + 1) / 2).sum())


def part2(depths: np.ndarray):
    return part1(depths, cost=get_squared_costs)


if __name__ == '__main__':
    data = parse_input('Day7.in')
    print(part1(data))
    print(part2(data))
