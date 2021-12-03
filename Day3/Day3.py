import numpy as np

BIT_WIDTH = 12


def parse_input(filename):
    return (np.fromfile(filename, dtype=np.int8, sep='').reshape((-1, BIT_WIDTH + 2))[:, :-2] == ord('1')).astype(int)


def bin2num(arr: np.ndarray):
    return (arr * 2 ** np.arange(arr.shape[0])[::-1]).sum()


def part1(binary: np.ndarray):
    most_common = binary.sum(axis=0) > binary.shape[0] // 2
    return bin2num(most_common) * bin2num(~most_common)


def filter_numbers(binary: np.ndarray, selector):
    valid_idx = np.arange(binary.shape[0])
    bit = 0
    while len(valid_idx) > 1:
        correct_bits = selector(binary[valid_idx].sum(axis=0), valid_idx.shape[0])
        valid_idx = valid_idx[binary[valid_idx, bit] == correct_bits[bit]]
        bit += 1
    return binary[valid_idx][0]


def part2(binary: np.ndarray):
    return bin2num(filter_numbers(binary, lambda occ, l: occ >= (l / 2))) * bin2num(filter_numbers(binary, lambda occ, l: occ < l / 2))


if __name__ == '__main__':
    data = parse_input('Day3.in')
    print(part1(data))
    print(part2(data))
