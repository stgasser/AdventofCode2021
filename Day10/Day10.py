def parse_input(filename):
    with open(filename) as f:
        return (''.join(f.readlines())).split()


def evaluate_line(line: str):
    opening = {'(': '1', '[': '2', '{': '3', '<': '4'}
    closing = {')': 3, ']': 57, '}': 1197, '>': 25137}
    chunks = []
    for c in line:
        if c in opening:
            chunks.append(c)
        elif c in closing:
            last = chunks.pop()
            if abs(ord(last) - ord(c)) > 2:
                return closing[c], None
    # translate missing characters to a base 5 number
    return 0, int(''.join(chunks[::-1]).translate({ord(k): v for k, v in opening.items()}), 5)


def part1(lines):
    return sum(evaluate_line(line)[0] for line in lines)


def part2(lines):
    auto_scores = []
    for line in lines:
        error_score, autocomplete_score = evaluate_line(line)
        if error_score == 0:
            auto_scores.append(autocomplete_score)
    auto_scores.sort()
    return auto_scores[len(auto_scores)//2]


if __name__ == '__main__':
    data = parse_input('Day10.in')
    print(part1(data))
    print(part2(data))
