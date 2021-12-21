from itertools import product
from collections import Counter, defaultdict
import time


def parse_input(filename: str):
    with open(filename) as f:
        p1, p2 = f.readlines()
        return int(p1[-3:]), int(p2[-3:])


def deterministic_die():
    die = 1
    while True:
        yield die
        die += 1
        if die > 100:
            die -= 100


def part1(p1, p2, die_gen=deterministic_die):
    cur, other = 1, 0
    game = [{'pos': (p1 - 1) % 10, 'sum': 0}, {'pos': (p2 - 1) % 10, 'sum': 0}]
    die_cnt = 0
    die = die_gen()
    while game[cur]['sum'] < 1000:
        cur, other = other, cur
        game[cur]['pos'] = (game[cur]['pos'] + next(die) + next(die) + next(die)) % 10
        game[cur]['sum'] += game[cur]['pos'] + 1
        die_cnt += 3
    return game[other]['sum'] * die_cnt


def dirac_die_dist(max_die=3, throws=3):
    return Counter([sum(x) + throws for x in product(range(max_die), repeat=throws)]).items()


# takes about 23s
def part2(p1, p2, win=21):
    games = defaultdict(int)
    games[(p1, 0, p2, 0, 0)] = 1
    dist = dirac_die_dist()
    p1_wins, p2_wins = 0, 0
    while games:
        (p1_pos, p1_sum, p2_pos, p2_sum, current_player), possibilities = games.popitem()
        for die_sum, die_possibilities in dist:
            current_possibilities = possibilities * die_possibilities
            new_p1_pos, new_p1_sum, new_p2_pos, new_p2_sum = p1_pos, p1_sum, p2_pos, p2_sum
            if current_player == 0:
                new_p1_pos += die_sum
                if new_p1_pos > 10:
                    new_p1_pos -= 10
                new_p1_sum += new_p1_pos
                if new_p1_sum >= win:
                    p1_wins += current_possibilities
                    continue
            else:
                new_p2_pos += die_sum
                if new_p2_pos > 10:
                    new_p2_pos -= 10
                new_p2_sum += new_p2_pos
                if new_p2_sum >= win:
                    p2_wins += current_possibilities
                    continue
            games[(new_p1_pos, new_p1_sum, new_p2_pos, new_p2_sum, 1 - current_player)] += current_possibilities
    return max(p1_wins, p2_wins)


if __name__ == '__main__':
    data = parse_input('Day21.in')
    print(part1(*data))
    print(part2(*data))
