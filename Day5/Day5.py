import numpy as np
from collections import Counter


def parse_input(filename):
    with open(filename) as f:
        ret = []
        for line in f.readlines():
            p1, p2 = line.strip().split(' -> ')
            ret.append((np.fromstring(p1, sep=',', dtype=int), np.fromstring(p2, sep=',', dtype=int)))
        return ret


def part1(lines):
    cnt = Counter()
    for start, end in lines:
        if (start == end).sum() != 1:
            continue
        pts = [tuple(start)]
        cur = start.copy()
        vel = (end - start)
        vel[vel != 0] = vel[vel != 0] / abs(vel[vel != 0])
        while np.any(cur != end):
            cur += vel
            pts.append(tuple(cur))
        cnt.update(pts)
    return sum(cnt[p] >= 2 for p in cnt)


def part2(lines):
    cnt = Counter()
    for start, end in lines:
        pts = [tuple(start)]
        cur = start.copy()
        vel = (end - start)
        vel[vel != 0] = vel[vel != 0] / abs(vel[vel != 0])
        while np.any(cur != end):
            cur += vel
            pts.append(tuple(cur))
        cnt.update(pts)
    return sum(cnt[p] >= 2 for p in cnt)


if __name__ == '__main__':
    data = parse_input('Day5.in')
    print(part1(data))
    print(part2(data))
