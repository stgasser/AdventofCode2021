def parse_input(filename):
    with open(filename) as f:
        file = f.readline()
        _, _, x, y = file.strip().split(' ')
        x_mi, x_ma = x[2:-1].split('..')
        y_mi, y_ma = y[2:].split('..')
        return (int(x_ma), int(x_mi)), (int(y_ma), int(y_mi))


def part1(xs, ys):
    x_ma, x_mi = xs
    y_ma, y_mi = ys
    highest = 0
    estimated_min_vel = min(x_vel for x_vel in range(x_mi) if x_vel * (x_vel + 1) // 2 >= x_mi)
    # highest shot has to have the highest initial upwards velocity possible
    # up and down cancel each other out max y afterwards needs to lower then the minimal target depth
    y_vel = -y_mi - 1   # -1 due to gravity in the last step
    if estimated_min_vel < y_vel*2 + 1:
        return y_vel*(y_vel + 1)//2     # peak height

    for init_y_vel in reversed(range(-y_mi + 1)):
        if init_y_vel*(init_y_vel + 1)//2 < highest:    # can't go higher
            continue
        for init_x_vel in range(estimated_min_vel - 1, x_ma + 1):
            x_vel, y_vel = init_x_vel, init_y_vel
            x, y = 0, 0
            peak = y
            while y >= y_mi and x <= x_ma:
                x += x_vel
                y += y_vel
                if x_vel > 0:
                    x_vel -= 1
                y_vel -= 1
                if y > peak:
                    peak = y
                if x_mi <= x <= x_ma and y_mi <= y <= y_ma:
                    if peak > highest:
                        highest = peak
                    break
    return highest


def part2(xs, ys):
    x_ma, x_mi = xs
    y_ma, y_mi = ys

    hit_cnt = 0
    estimated_min_vel = min(x_vel for x_vel in range(x_mi) if x_vel * (x_vel + 1) // 2 >= x_mi)
    for init_x_vel in range(estimated_min_vel, x_ma + 1):
        # the minimum amount of steps needed to reach target x value
        steps = min(vel for vel in range(init_x_vel+1) if sum(range(vel)) + vel*(init_x_vel - vel + 1) >= x_mi)
        for init_y_vel in range(y_mi//steps, -y_mi + 1):
            x_vel, y_vel = init_x_vel, init_y_vel
            x, y = 0, 0
            while y >= y_mi and x <= x_ma:
                x += x_vel
                y += y_vel
                if x_vel > 0:
                    x_vel -= 1
                y_vel -= 1
                if x_mi <= x <= x_ma and y_mi <= y <= y_ma:
                    hit_cnt += 1
                    break
    return hit_cnt


if __name__ == '__main__':
    data = parse_input('Day17.in')
    print(part1(*data))
    print(part2(*data))
