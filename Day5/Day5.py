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
        # the rounding is necessary as there is strange float behaviour going on 183 -> 183.9999999999994 -> 185
        cnt.update(tuple(np.round(pt).astype(int)) for pt in np.linspace(start, end, num=abs(end - start).max() + 1))
    return sum(cnt[p] >= 2 for p in cnt)


def part2(lines):
    cnt = Counter()
    for start, end in lines:
        cnt.update(tuple(np.round(pt).astype(int)) for pt in np.linspace(start, end, num=abs(end - start).max() + 1))
    return sum(cnt[p] >= 2 for p in cnt)


if __name__ == '__main__':
    data = parse_input('Day5.in')
    print(part1(data))
    print(part2(data))
