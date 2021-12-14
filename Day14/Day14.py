from collections import Counter


def parse_input(filename):
    with open(filename) as f:
        file = ''.join(f.readlines())
        template, rules = file.split('\n\n')
        rules_dict = dict()
        for rule in rules.split('\n'):
            pair, ins = rule.split(' -> ')
            rules_dict[pair[0], pair[1]] = ins
        return template, rules_dict


def part1(template, rules, steps=10):
    template = list(template)
    for i in range(steps):
        new_string = [template[0]]
        for c in template[1:]:
            pair = (new_string[-1], c)
            if pair in rules:
                new_string.append(rules[pair])
            new_string.append(c)
        template = new_string
    cnt = Counter(template).most_common()
    return cnt[0][1] - cnt[-1][1]


def part2(template, rules, steps=40):
    pairs = Counter((c1, c2) for c1, c2 in zip(template[:-1], template[1:]))
    for i in range(steps):
        new_pairs = Counter()
        for pair, occ in pairs.items():
            if pair in rules:
                c = rules[pair]
                new_pairs[(pair[0], c)] += occ
                new_pairs[(c, pair[1])] += occ
            else:
                new_pairs[pair] += occ
        pairs = new_pairs
    cnt = Counter()
    for pair, occ in pairs.items():
        cnt[pair[1]] += occ
    cnt[template[0]] += 1
    cnt = cnt.most_common()
    return cnt[0][1] - cnt[-1][1]


if __name__ == '__main__':
    data = parse_input('Day14.in')
    print(part1(*data))
    print(part2(*data))
