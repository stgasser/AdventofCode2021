from itertools import permutations, product
from functools import reduce
from operator import add
import time


def parse_input(filename):
    with open(filename) as f:
        return [[eval(probe) for probe in scanner.split('\n')[1:]] for scanner in ''.join(f.readlines()).split('\n\n')]


def get_deltas(probe, scanner):
    return {(p[0] - probe[0], p[1] - probe[1], p[2] - probe[2]) for p in scanner}


def get_orientations(probe):
    return reduce(add, [[(x * xo, y * yo, z * zo)] for xo, yo, zo in product((1, -1), repeat=3) for x, y, z in permutations(probe)])


def manhattan_dist(A, B):
    return sum(abs(a - b) for a, b in zip(A, B))


def part1(scanners):
    start = time.thread_time()
    beacons = scanners[0].copy()
    matched = {0}
    dont_check = set()
    max_dist = 0
    scanner_coordinates = [(0, 0, 0)]
    while len(matched) < len(scanners):
        # pre-calculate deltas
        deltas = [(i, get_deltas(p, beacons)) for i, p in enumerate(beacons) if i not in dont_check]
        assert len(deltas) > 0
        # find all matches to current beacons
        matches = []
        for j, s2 in enumerate(scanners):
            if j in matched:
                continue  # already integrated
            match = False
            orientations = [get_orientations(p) for p in s2]    # pre-calculate orientations
            # find one matching point
            for pi, delta1 in deltas:
                for orientation in zip(*orientations):
                    for pj, p2 in enumerate(orientation):
                        delta2 = get_deltas(p2, orientation)
                        if len(delta1 & delta2) >= 12:
                            # matching points found in correct orientation and where the shared point is 0, 0, 0
                            matches.append((pi, j, p2, delta2))
                            match = True
                            break
                    if match: break
                if match: break
            else:
                # no match found for this point
                dont_check.add(pi)
        for pi, j, p2, coordinates in matches:

            common = beacons[pi]   # this is the shared point in scanner 1 coordinate offset
            scanner_coordinates.append((common[0] - p2[0], common[1] - p2[1], common[2] - p2[2]))
            # add shared point to new beacons to correct the offset
            new_coordinates = get_deltas((-common[0], -common[1], -common[2]), coordinates)
            # add new beacons to list
            beacon_set = set(beacons)
            beacons += [p for p in new_coordinates if p not in beacon_set]
            matched.add(j)
            print("match found for:", j)
    for A, B in product(scanner_coordinates, repeat=2):
        dist = manhattan_dist(A, B)
        if max_dist < dist:
            max_dist = dist
    print(time.thread_time()-start)
    return len(beacons), max_dist


if __name__ == '__main__':
    data = parse_input('Day19.in')
    print(part1(data))
