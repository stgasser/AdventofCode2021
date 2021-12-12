import networkx as nx
from collections import Counter


def parse_input(filename):
    G = nx.Graph()
    with open(filename) as f:
        for line in f.readlines():
            G.add_edge(*tuple(line.strip().split('-')))
    return G


def part1(G, path=None):
    if not path:
        path = ['start']
    if path[-1] == 'end':
        return 1
    pathcnt = 0
    for n in G.neighbors(path[-1]):
        if n.isupper() or (n not in path):
            pathcnt += part1(G, path=path + [n])
    return pathcnt


def part2(G, path=None, double=False):
    if not path:
        path = ['start']
    if path[-1] == 'end':
        return 1
    pathcnt = 0
    for n in G.neighbors(path[-1]):
        if n == 'start':
            continue
        if n.isupper():
            pathcnt += part2(G, path=path + [n], double=double)
        elif not double:
            pathcnt += part2(G, path=path + [n], double=n in path)
        elif n not in path:
            pathcnt += part2(G, path=path + [n], double=double)
    return pathcnt


if __name__ == '__main__':
    data = parse_input('Day12.in')
    print(part1(data))
    print(part2(data))
