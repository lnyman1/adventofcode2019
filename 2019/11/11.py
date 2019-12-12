import os

import matplotlib.pyplot as plt
import numpy as np
import requests
import requests_cache
from intcode import IntCode

def part1(lines):
    return len(paint(lines, 0))


def part2(lines):
    paint_result = paint(lines, 1)
    coords = [k for (k, v) in paint_result.items()]
    max_x = max(coords, key=lambda x: x[0])[0]
    max_y = max(coords, key=lambda y: y[1])[1]

    img = np.zeros((max_y + 1, max_x + 1))
    for h in range(max_x + 1):
        for w in range(max_y + 1):
            img[w][h] = paint_result.get((h, w))
    return img


move_forward = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1)
}

turn_anticlockwise = {
    ">": "^",
    "v": ">",
    "<": "v",
    "^": "<"
}

turn_clockwise = {
    ">": "v",
    "v": "<",
    "<": "^",
    "^": ">"
}


def paint(lines, colour):
    panels = {}
    coord = (0, 0)
    panels[coord] = colour
    direction = "^"

    program = IntCode(lines)

    while not program.halt:
        panels[coord] = program.operation(panels.get(coord) if coord in panels else 0)
        output = program.operation(panels.get(coord) if coord in panels else 0)
        direction = turn_anticlockwise[direction] if output == 0 else turn_clockwise[direction]
        coord = (coord[0] + move_forward[direction][0], coord[1] + move_forward[direction][1])

    return panels


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
    plt.imshow(part2(instruction))
    plt.show()


if __name__ == "__main__":
    main()
