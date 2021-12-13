import numpy as np


def parse_input(filename):
    with open(filename) as f:
        points, folds = ''.join(f.readlines()).split('\n\n')
        points = list(map(lambda l: tuple(map(int, l.split(','))), points.split()))
        return points, list(map(lambda l: l[11:].split('='), folds.split('\n')))


def make_paper(points):
    paper = np.zeros(tuple(map(lambda c: max(c) + 1, zip(*points))), dtype=bool)
    for point in points:
        paper[point] = True
    return paper


def fold_paper(paper, axis, line):
    if type(line) == str:
        line = int(line)
    if axis == 'y':
        return paper[:, :line] + paper[:, -1:line:-1]
    elif axis == 'x':
        return paper[:line, :] + paper[-1:line:-1, :]


def part1(points, folds):
    return fold_paper(make_paper(points), *folds[0]).sum()


def part2(points, folds):
    paper = make_paper(points)
    for fold_axis, fold_line in folds:
        paper = fold_paper(paper, fold_axis, fold_line)
    translate = {0: '.', 1: '#'}
    return '\n'.join(map(lambda arr: ' '.join(map(lambda p: translate[p], arr)), paper.astype(int).T))


if __name__ == '__main__':
    data = parse_input('Day13.in')
    print(part1(*data))
    print(part2(*data))
