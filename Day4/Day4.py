import numpy as np
from collections import defaultdict


def parse_input(filename):
    with open(filename) as f:
        draws = np.array(f.readline().strip().split(','), dtype=int);
        board_str = '\n'.join(''.join(f.readlines()).strip().split('\n\n'))
        return np.fromstring(board_str, dtype=int, sep=' ').reshape((-1, 5, 5)), draws
    pass


def calculate_score(board, marks, num):
    return (board * (1 - marks)).sum() * num


def part1(boards, draws):
    number_indices = defaultdict(list)
    for idx, n in np.ndenumerate(boards):
        number_indices[n].append(idx)
    marks = np.zeros(boards.shape, dtype=int)
    for i, num in enumerate(draws):
        for idx in number_indices.get(num, []):
            marks[idx] = 1
        if marks.sum(axis=1).max() == 5:
            b_id = np.argwhere(marks.sum(axis=1) == 5)[0][0]
            return calculate_score(boards[b_id, :, :], marks[b_id], num)
        if marks.sum(axis=2).max() == 5:
            b_id = np.argwhere(marks.sum(axis=2) == 5)[0][0]
            return calculate_score(boards[b_id, :, :], marks[b_id], num)


def part2(boards, draws):
    number_indices = defaultdict(list)
    for idx, n in np.ndenumerate(boards):
        number_indices[n].append(idx)
    marks = np.zeros(boards.shape, dtype=int)
    playing_boards = {i for i in range(boards.shape[0])}
    won_boards = set()
    last_board = -1
    for i, num in enumerate(draws):
        for idx in number_indices.get(num, []):
            marks[idx] = 1
        won_boards = won_boards.union(set(np.argwhere(marks.sum(axis=1) == 5)[:, 0])).union(set(np.argwhere(marks.sum(axis=2) == 5)[:, 0]))
        if len(playing_boards - won_boards) == 1:
            b_id = (playing_boards - won_boards).pop()
            last_board = b_id
        if len(playing_boards - won_boards) == 0:
            return calculate_score(boards[last_board], marks[last_board], num)


if __name__ == '__main__':
    data = parse_input('Day4.in')
    print(part1(*data))
    print(part2(*data))
