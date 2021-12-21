import numpy as np
from scipy.signal import convolve2d


def parse_input(filename):
    with open(filename) as f:
        content = ''.join(f.readlines())
        alg, img = content.split('\n\n')
        alg = (np.frombuffer(bytes(alg.strip(), 'ascii'), dtype=np.uint8) == ord('#')).astype(int)
        img = np.frombuffer(bytes(img, 'ascii'), dtype=np.uint8)
        idx = np.argwhere(img == ord('\n'))
        return (img.reshape((-1, idx[0][0] + 1))[:, :-1] == ord('#')).astype(int), alg


def part1(img, alg, steps=2):
    mask = (2 ** np.arange(9))[::-1].reshape((3, 3))
    fill = 0
    for _ in range(steps):
        img = alg[convolve2d(img, mask[::-1, ::-1], fillvalue=fill)]
        fill = alg[0] if fill == 0 else alg[-1]         # This took me forever to find. Stupid infinite pictures
    return img.sum()


def part2(img, alg):
    return part1(img, alg, steps=50)


if __name__ == '__main__':
    data = parse_input('Day20.in')
    print(part1(*data))
    print(part2(*data))
