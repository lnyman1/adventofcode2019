from collections import Counter


def part1(lower, upper):
    possibilities = set()
    for i in range(lower, upper, 1):
        if rulesPart1(i):
            possibilities.add(i)
    return len(possibilities)


def part2(lower, upper):
    possibilities = set()
    for i in range(lower, upper, 1):
        if rulesPart2(i):
            possibilities.add(i)
    return len(possibilities)


def rulesPart1(number):
    char = [int(d) for d in str(number)]
    char.sort()
    if number != int(''.join(str(n) for n in char)):
        return False
    counter = Counter(char)
    result = [i for i, j in counter.items() if j > 1]
    if len(result) < 1:
        return False
    return True


def rulesPart2(number):
    char = [int(d) for d in str(number)]
    char.sort()
    if number != int(''.join(str(n) for n in char)):
        return False
    counter = Counter(char)
    result = [i for i, j in counter.items() if j == 2]
    if len(result) < 1:
        return False
    return True


def main():
    lower = 278384
    upper = 824795

    print(part1(lower, upper))
    print(part2(lower, upper))


if __name__ == "__main__":
    main()
