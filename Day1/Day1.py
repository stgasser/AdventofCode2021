import numpy as np


def parse_input(filename: str):
    return np.loadtxt(filename, delimiter='\n', dtype=int)


def part1(depths):
    return (depths[:-1] < depths[1:]).sum()


def part2(depths):
    return part1(np.convolve(depths, np.ones(3, dtype=int), mode='valid'))


if __name__ == '__main__':
    data = parse_input('Day1.in')
    print(part1(data))
    print(part2(data))
