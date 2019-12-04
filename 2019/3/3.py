import os
import requests
import requests_cache
from collections import defaultdict

directions = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (1, 1),
    "D": (1, -1)
}


def part1(lines):
    origin = (0, 0)
    result = crossed_wire_calc(lines, origin)
    crossings = set(result[0]).intersection(set(result[1]))
    return min(manhatten_dist(coord, origin) for coord in crossings)


def part2(lines):
    origin = (0, 0)
    result = crossed_wire_calc(lines, origin)
    crossings = set(result[0]).intersection(set(result[1]))
    return min(result[0][coord] + result[1][coord] for coord in crossings)


def crossed_wire_calc(lines, origin):
    result = defaultdict(map)
    for line in range(len(lines)):
        steps_taken = 0
        coords = {}
        pos = list(origin)
        for steps in lines[line].split(","):

            direction, value = steps[0], int(steps[1:])
            new_pos = directions[direction]

            for _ in range(value):
                pos[new_pos[0]] += new_pos[1]
                steps_taken += 1
                if tuple(pos) not in coords:
                    coords[tuple(pos)] = steps_taken

        result[line] = coords
    return result

def manhatten_dist(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


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
