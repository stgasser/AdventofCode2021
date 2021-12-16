import numpy as np
from collections import Counter


def parse_input(filename):
    with open(filename) as f:
        transmission = f.readline()
        return np.unpackbits(np.frombuffer(bytes.fromhex(transmission), dtype=np.uint8))


def bin2int(arr):
    return int(((2 ** np.arange(len(arr))[::-1]) * arr).sum())


def prod(*args):
    p = 1
    for n in args:
        p *= n
    return p


def gt(a, b):
    return int(a > b)


def lt(a, b):
    return int(a < b)


def eq(a, b):
    return int(a == b)


def su(*args):
    s = 0
    for n in args:
        s += n
    return s


def mi(*args):
    if type(args) == int:
        return args
    return min(args)


def ma(*args):
    if type(args) == int:
        return args
    return max(args)


def solve(transmission):
    pos = 0
    versions = 0
    # goal is to trans-pile it into an evalable expression
    operations = '('
    type_stack = []
    package_stack = []
    pos_stack = []
    prefix = {0: 'su', 1: 'prod', 2: 'mi', 3: 'ma', 5: 'gt', 6: 'lt', 7: 'eq'}
    while pos < len(transmission) - 7:
        V = bin2int(transmission[pos:pos + 3])
        versions += V
        pos += 3
        T = bin2int(transmission[pos:pos + 3])
        pos += 3
        if operations[-1] not in {'('}:
            operations += ','
        if T == 4:
            number = 0
            while transmission[pos] == 1:
                number = number * (2 ** 4) + bin2int(transmission[pos + 1: pos + 5])
                pos += 5
            number = number * (2 ** 4) + bin2int(transmission[pos + 1: pos + 5])
            if number == 3188:
                pass
            operations += str(number)
            pos += 5
            # reduce package cnt recursively if in package count mode
            while type_stack and type_stack[-1] == 'pck' and package_stack:
                package_stack[-1] -= 1
                if package_stack[-1] == 0:
                    package_stack.pop()
                    type_stack.pop()
                    operations += ')'
                else:
                    break
        else:
            operations += prefix[T] + '('
            if transmission[pos] == 0:
                L = bin2int(transmission[pos + 1:pos + 16])
                pos += 16
                pos_stack.append(pos + L)
                type_stack.append('abs')
            else:
                num_packages = bin2int(transmission[pos + 1:pos + 12])
                package_stack.append(num_packages)
                type_stack.append('pck')
                pos += 12
                pass
        for p in pos_stack:
            if pos == p:        # check if a position based package is done
                operations += ')'
                type_stack.pop()
                # reduce package cnt recursively if in package count mode
                while type_stack and type_stack[-1] == 'pck' and package_stack:
                    package_stack[-1] -= 1
                    if package_stack[-1] == 0:
                        package_stack.pop()
                        type_stack.pop()
                        operations += ')'
                    else:
                        break
    return versions, eval(operations + ')')


if __name__ == '__main__':
    data = parse_input('Day16.in')
    print(*solve(data))
