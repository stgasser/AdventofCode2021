from itertools import permutations

P = 'parent'
L = 'left'
R = 'right'
I = 'int'


def make_tree(l, parent=None):
    if type(l) == int:
        return {I: l, P: parent}
    d = dict()
    d[P] = parent
    d[L] = make_tree(l[0], parent=d)

    d[R] = make_tree(l[1], parent=d)
    return d


def parse_input(filename):
    with open(filename) as f:
        out = []
        for line in f.readlines():
            arr = eval(line)
            out.append(arr)
        return out


def get_neighbor(n, d):
    other = R if d == L else L
    cur = n
    while cur[P] and id(cur[P][d]) == id(cur):
        cur = cur[P]
    if cur[P]:
        cur = cur[P][d]
        while I not in cur:
            cur = cur[other]
        return cur


def get_depth(n):
    d = 0
    while n[P]:
        n = n[P]
        d += 1
    return d


def to_string(n):
    if not n:
        return '[]'
    if I in n:
        return str(n[I])
    return '[' + to_string(n[L]) + ',' + to_string(n[R]) + ']'


def left_iter(n, filter=lambda x: True):
    if filter(n):
        yield n
    if I not in n:
        for left in left_iter(n[L]):
            yield left
        for right in left_iter(n[R]):
            yield right


def reduce(sn):
    while True:
        for n in left_iter(sn):
            if I not in n and get_depth(n) > 3:
                nei_l = get_neighbor(n, L)
                nei_r = get_neighbor(n, R)
                par = n[P]
                if par[L] == n:
                    par[L] = {P: par, I: 0}
                else:
                    par[R] = {P: par, I: 0}
                if nei_l:
                    nei_l[I] += n[L][I]
                if nei_r:
                    nei_r[I] += n[R][I]
                break
            pass
        else:
            for n in left_iter(sn):
                if I in n and n[I] >= 10:
                    n[L] = {I: n[I] // 2, P: n}  # integer division to avoid having to round
                    n[R] = {I: n[I] - n[L][I], P: n}
                    del n[I]
                    break
            else:
                break  # Exit the while Loop


def get_magnitude(n):
    if I in n:
        return n[I]
    else:
        return 3 * get_magnitude(n[L]) + 2 * get_magnitude(n[R])


def part1(snail_numbers):
    s = make_tree(snail_numbers[0])
    for a in snail_numbers[1:]:
        a = make_tree(a)
        d = {P: None, L: s, R: a}
        s[P] = d
        a[P] = d
        reduce(d)
        s = d
    return get_magnitude(s)


def part2(snail_numbers):
    m_max = 0
    for a, b in permutations(snail_numbers, r=2):
        d = {P: None}
        a, b = make_tree(a, d), make_tree(b, d)
        d[L] = a
        d[R] = b
        reduce(d)
        m = get_magnitude(d)
        if m > m_max:
            m_max = m
    return m_max


if __name__ == '__main__':
    print(part1(parse_input('Day18.in')))
    print(part2(parse_input('Day18.in')))
