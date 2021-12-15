import numpy as np
import networkx as nx
from itertools import product


def parse_input(filename):
    file = np.fromfile(filename, dtype=np.int8)
    return file.reshape((-1, np.argwhere(file == 10)[0, 0] + 1))[:, :-2] - ord('0')


def get_neighbors(pos, ma, mi=(0, 0)):
    neighbors = []
    x, y = pos
    if x > mi[0]:
        neighbors.append((x - 1, y))
    if x + 1 < ma[0]:
        neighbors.append((x + 1, y))
    if y > mi[1]:
        neighbors.append((x, y - 1))
    if y + 1 < ma[1]:
        neighbors.append((x, y + 1))
    return neighbors


def manhattan_distance(pos, target):
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1])


def get_cost(path, grid):
    return grid[tuple(zip(*path[1:]))].sum()


def part1(grid: np.ndarray):
    D = nx.DiGraph()
    for pos, c in np.ndenumerate(grid):
        for n in get_neighbors(pos, grid.shape):
            D.add_edge(n, pos, weight=c)
    path = nx.astar_path(D, (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1), heuristic=manhattan_distance, weight='weight')
    return get_cost(path, grid)


def part2(grid: np.ndarray):
    x, y = grid.shape
    new_grid = np.zeros((x * 5, y * 5), dtype=int)
    for i, j in product(range(5), repeat=2):
        new_grid[x * i:x * i + x, y * j:y * j + y] = (grid - 1 + i + j) % 9 + 1
    return part1(new_grid)


if __name__ == '__main__':
    data = parse_input('Day15.in')
    print(part1(data))
    print(part2(data))
