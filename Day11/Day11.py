import numpy as np
from scipy.signal import convolve2d


def parse_input(filename):
    file = np.fromfile(filename, dtype=np.int8)
    return file.reshape((-1, np.argwhere(file == 10)[0, 0] + 1))[:, :-2] - ord('0')


def perform_step(octopi, mask=np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])):
    octopi += 1
    flashed = np.zeros_like(octopi).astype(bool)
    while np.any((octopi > 9) & ~flashed):
        flashes = (octopi > 9) & ~flashed
        octopi += convolve2d(flashes, mask, mode='same')
        flashed |= flashes
    octopi *= ~flashed
    return flashed, octopi


def part1(octopi, steps=100):
    flash_cnt = 0
    for _ in range(steps):
        flashed, octopi = perform_step(octopi)
        flash_cnt += flashed.sum()
    return flash_cnt


def part2(octopi):
    step_cnt = 0
    while True:
        flashed, octopi = perform_step(octopi)
        step_cnt += 1
        if np.all(flashed):
            return step_cnt


if __name__ == '__main__':
    data = parse_input('Day11.in')
    print(part1(data.copy()))
    print(part2(data.copy()))
