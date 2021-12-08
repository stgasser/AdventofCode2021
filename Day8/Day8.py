def parse_input(filename):
    with open(filename) as f:
        for l in f.readlines():
            pats, vals = l.split(' | ')
            pats = pats.split()
            vals = vals.split()
            yield [set(p) for p in pats], [set(v) for v in vals]


def part1(inp):
    return sum(sum(map(lambda val: len(val) in {2, 3, 4, 7}, vals)) for _, vals in inp)


# 0 ... len 6; len 0u5 4;
# 1 ... len 2;
# 2 ... len 5; len 2u4 2;
# 3 ... len 5; len 3u1 2;
# 4 ... len 4;
# 5 ... len 5; len 5u4 3;
# 6 ... len 6; len 6u1 1;
# 7 ... len 3;
# 8 ... len 7;
# 9 ... len 6; len 9u4 4;
def part2(inp):
    ret = 0
    for pats, vals in inp:
        digits = dict()
        for pat in pats:
            if len(pat) == 2:
                digits[1] = pat
            if len(pat) == 4:
                digits[4] = pat
            if len(pat) == 3:
                digits[7] = pat
            if len(pat) == 7:
                digits[8] = pat
        for pat in pats:
            u4 = pat.intersection(digits[4])
            u1 = pat.intersection(digits[1])
            if len(pat) == 6:
                if len(u4) == 4:
                    digits[9] = pat
                elif len(u1) == 1:
                    digits[6] = pat
                else:
                    digits[0] = pat
            elif len(pat) == 5:
                if len(u1) == 2:
                    digits[3] = pat
                elif len(u4) == 3:
                    digits[5] = pat
                else:
                    digits[2] = pat

        num = 0
        for val in vals:
            for d, pat in digits.items():
                if pat == val:
                    num = num * 10 + d
                    break
        ret += num
    return ret


if __name__ == '__main__':
    data = list(parse_input('Day8.in'))
    print(part1(data))
    print(part2(data))
