import os
import requests
import requests_cache
import math


def part1(lines):
    return sum(map(calc, map(int, lines)))


def part2(lines):
    return sum(map(recursive_calc, map(int, lines)))


def recursive_calc(x):
    fuel = calc(x)
    if fuel <= 0:
        return 0
    return fuel + recursive_calc(fuel)


def calc(x):
    return math.trunc(x / 3) - 2


def get_input_file():
    requests_cache.install_cache('../cache')
    url = 'https://adventofcode.com/' + os.path.abspath(__file__).split('/')[-3] + '/day/' + __file__.split('.')[
        0] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
