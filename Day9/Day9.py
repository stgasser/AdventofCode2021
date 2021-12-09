import numpy as np


def parse_input(filename):
    chrs = np.fromfile(filename, dtype=np.int8)
    end = np.argwhere(chrs == 10)
    return chrs.reshape((-1, end[0, 0] + 1))[:, :-2] - ord('0')


def part1(heightmap):
    risk_level = 0
    for (x, y), h in np.ndenumerate(heightmap):
        if x > 0 and heightmap[x - 1, y] <= h:
            continue
        if x < heightmap.shape[0] - 1 and heightmap[x + 1, y] <= h:
            continue
        if y > 0 and heightmap[x, y - 1] <= h:
            continue
        if y < heightmap.shape[1] - 1 and heightmap[x, y + 1] <= h:
            continue
        risk_level += h + 1
    return risk_level


def part2(heightmap):
    ridges = (heightmap == 9).astype(int)
    taken = ridges.copy()
    basinsizes = list()
    while np.any(taken == 0):
        start = tuple(np.argwhere(taken == 0)[0])
        fringe = {(start[0], start[1])}
        basin_size = 0
        while fringe:
            x, y = fringe.pop()
            taken[x, y] = 1
            basin_size += 1
            if x > 0 and not ridges[x - 1, y] and not taken[x - 1, y]:
                fringe.add((x - 1, y))
            if x < ridges.shape[0] - 1 and not ridges[x + 1, y] and not taken[x + 1, y]:
                fringe.add((x + 1, y))
            if y > 0 and not ridges[x, y - 1] and not taken[x, y - 1]:
                fringe.add((x, y - 1))
            if y < ridges.shape[1] - 1 and not ridges[x, y + 1] and not taken[x, y + 1]:
                fringe.add((x, y + 1))
        basinsizes.append(basin_size)
    basinsizes.sort()
    return basinsizes[-1] * basinsizes[-2] * basinsizes[-3]


if __name__ == '__main__':
    data = parse_input('Day9.in')
    print(part1(data))
    print(part2(data))
