from itertools import product
from copy import copy


def parse_input(filename: str):
    with open(filename) as f:
        cmds = []
        for line in f.read().splitlines():
            cmdtype, numbers = line.split()
            region = []
            for coords in numbers.split(','):
                a, b = coords[2:].split('..')
                a, b = int(a), int(b)
                if a <= b:
                    region.append((a, b))
                else:
                    region.append((b, a))

            cmds.append((cmdtype, region))
        return cmds


def get_in_range(lower, upper, limits=(-50, 50)):
    assert lower <= upper
    if lower > limits[1] or upper < limits[0]:
        return []
    return range(max(lower, limits[0]), min(upper, limits[1]) + 1)


def get_region(xr, yr, zr, limits=(-50, 50)):
    return product(get_in_range(*xr, limits=limits), get_in_range(*yr, limits=limits), get_in_range(*zr, limits=limits))


def part1(commands, limits=(-50, 50)):
    on_cuboids = set()
    for cmd, ranges in commands:
        if cmd == 'on':
            on_cuboids |= set(get_region(*ranges, limits=limits))
        else:
            on_cuboids -= set(get_region(*ranges, limits=limits))
    return len(on_cuboids)


class Region:
    def __init__(self, p1, p2):
        self.lower, self.upper = list(p1), list(p2)
        assert all(c1 <= c2 for c1, c2 in zip(p1, p2))

    def __le__(self, other):  # checks if self is a sub-region off other
        return all(a <= b for a, b in zip(other.lower, self.lower)) and all(a >= b for a, b in zip(other.upper, self.upper))

    def get_cube_count(self):
        ret = 1
        for u, l in zip(self.upper, self.lower):
            ret *= (u - l + 1)
        return ret

    def get_corners(self):
        return [c for c in product(*zip(self.lower, self.upper))]

    def get_intersection(self, other):
        upper = list(min(a, b) for a, b in zip(self.upper, other.upper))
        lower = list(max(a, b) for a, b in zip(self.lower, other.lower))
        if all(a <= b for a, b in zip(lower, upper)):
            return Region(lower, upper)
        return None

    def does_intersect(self, other):
        upper = (min(a, b) for a, b in zip(self.upper, other.upper))
        lower = (max(a, b) for a, b in zip(self.lower, other.lower))
        return all(a <= b for a, b in zip(lower, upper))

    def is_contained(self, point):
        return all(l <= p <= u for l, p, u in zip(self.lower, point, self.upper))

    def clone(self):
        return Region(copy(self.lower), copy(self.upper))

    def split(self, point):
        if not self.is_contained(point):
            return [self]
        ret = [self]
        for axis, coord in enumerate(point):
            ret = sum([r._split_along_axis(axis, coord) for r in ret], [])
        return ret

    def _split_along_axis(self, axis, coord):
        l, u = self.lower[axis], self.upper[axis]
        if coord < l or u < coord:
            return [self]
        ret = [self.clone()]
        ret[0].upper[axis] = coord
        ret[0].lower[axis] = coord
        if l < coord:
            new_region = self.clone()
            new_region.upper[axis] = coord - 1
            ret.append(new_region)
        if u > coord:
            new_region = self.clone()
            new_region.lower[axis] = coord + 1
            ret.append(new_region)
        return ret

    def __sub__(self, other):
        if not self.does_intersect(other):
            return [self]
        intersection = self.get_intersection(other)
        if intersection is None:
            return [self]
        regions = [self]
        for corner in intersection.get_corners():
            new_regions = []
            for r in regions:
                if r.is_contained(corner):
                    for new_region in r.split(corner):
                        if not new_region <= intersection:
                            new_regions.append(new_region)
                else:
                    new_regions.append(r)
            regions = new_regions
        return regions


def part2(commands):
    on_regions = []
    cnt = 0
    for cmd, ranges in commands:
        print(cnt / len(commands), len(on_regions))
        cnt += 1
        new_region = Region(*zip(*ranges))
        if cmd == 'on':
            on_regions = [new_region] + sum([region - new_region for region in on_regions], [])
        else:
            on_regions = sum([region - new_region for region in on_regions], [])
    return sum(r.get_cube_count() for r in on_regions)


if __name__ == '__main__':
    data = parse_input('Day22.in')
    print(part1(data))
    print(part2(data))
