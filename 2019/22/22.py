import os
import re
from collections import deque
from sympy import mod_inverse

import requests
import requests_cache

NEW_STACK = "deal into new stack"
INCREMENT = "deal with increment "
CUT = "cut "


def part1(lines):
    deck = shuffle(lines)
    return deck.index(2019)


# ax + b
# a^2x + ab + b
# a^3x + a^2b + ab + b
# a^n * x + (a^(n-1) + a^(n-2) + a^(n-3) ... + 1) * b
# geometric sum = (a^n - 1)/(a - 1)
# total = a^nx + b(a^n - 1)/(a - 1)
def part2(lines):
    deck_size = 119315717514047
    x = 2020
    n = 101741582076661
    a, b = reverse_shuffle(lines, deck_size)
    A = pow(a, n, deck_size)
    return (A * x + b * (A - 1) * mod_inverse(a - 1, deck_size)) % deck_size


def shuffle(lines):
    deck = deque(range(10007))
    for line in lines:
        if line == NEW_STACK:
            deck = stack(deck)
            continue
        number = int(re.findall(r"-?\d+", line)[0])
        if line.startswith(CUT):
            deck = cut(deck, number)
        elif line.startswith(INCREMENT):
            deck = increment(deck, number)
    return deck


def stack(deck):
    deck.reverse()
    return deque(deck)


def cut(deck, number):
    deck.rotate(-number)
    return deque(deck)


def increment(deck, number):
    result = [-1 for _ in range(len(deck))]
    for i in range(0, len(deck) * number, number):
        result[i % len(result)] = deck.popleft()
    return deque(result)


def reverse_shuffle(lines, deck_size):
    a = 1
    b = 0
    lines.reverse()
    for line in lines:
        if line == NEW_STACK:
            a, b = reverse_stack(a, b)
            continue
        number = int(re.findall(r"-?\d+", line)[0])
        if line.startswith(INCREMENT):
            a, b = reverse_increment(a, b, number, deck_size)
        elif line.startswith(CUT):
            a, b = reverse_cut(a, b, number)
    return a, b


def reverse_stack(a, b):
    return -a, (-b - 1)


def reverse_cut(a, b, n):
    return a, (b + n)


def reverse_increment(a, b, n, deck_size):
    return a * pow(n, deck_size - 2, deck_size), b * pow(n, deck_size - 2, deck_size)


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
