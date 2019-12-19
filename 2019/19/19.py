import os
import requests
import requests_cache
from intcode import IntCode
from collections import Counter


def part1(lines):
    grid = {}

    for y in range(50):
        for x in range(50):
            program = IntCode(lines)
            output = program.operation([x, y])

            if output[0] == 0:
                grid[(x, y)] = "."
            elif output[0] == 1:
                grid[(x, y)] = "#"

    return len([(x, y) for (x, y) in grid if grid[(x, y)] == "#"])


def part2(lines):
    y = 99
    x = 0
    while True:
        if tractor_beam(lines, x, y) == 0:
            x += 1
            continue
        elif tractor_beam(lines, x + 99, y - 99) == 1:
            return x * 10000 + y - 99
        y += 1


def tractor_beam(lines, x, y):
    program = IntCode(lines)
    return program.operation([x, y])[0]


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().split(",")
    return lines


def main():
    lines = get_input_file()
    instruction = [int(x) for x in lines]

    print(part1(instruction))
    print(part2(instruction))


if __name__ == "__main__":
    main()
