import fileinput
import math

lines = list(fileinput.input())


def part1():
    return sum(map(calc, map(int, lines)))


def part2():
    return sum(map(recursive_calc, map(int, lines)))


def recursive_calc(x):
    fuel = calc(x)
    if fuel <= 0:
        return 0
    return fuel + recursive_calc(fuel)


def calc(x):
    return math.trunc(x / 3) - 2


print(part1())
print(part2())
