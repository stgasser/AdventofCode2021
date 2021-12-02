def parse_input(filename):
    with open(filename) as f:
        return [line.strip().split() for line in f.readlines()]


def part1(commands):
    pos = 0j
    movement = {'forward': 1, 'down': 1j, 'up': -1j}
    for mv, dis in commands:
        pos += int(dis) * movement[mv]
    return int(pos.imag * pos.real)


def part2(commands):
    pos = 0
    depth = 0
    aim = 0
    for mv, dis in commands:
        if mv == 'forward':
            pos += int(dis)
            depth += aim*int(dis)
        else:
            aim += int(dis)*(1 if mv == 'down' else -1)
    return pos*depth


if __name__ == '__main__':
    data = parse_input('Day2.in')
    print(part1(data))
    print(part2(data))
