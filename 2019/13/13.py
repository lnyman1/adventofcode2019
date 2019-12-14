import os

import requests
import requests_cache
from intcode import IntCode


def part1(lines):
    program = IntCode(lines)
    result = 0
    output = 0
    while not program.halt:
        for _ in range(3):
            output = program.operation(0)
        if output == 2:
            result += 1
    return result


def part2(lines):
    lines[0] = 2
    program = IntCode(lines)

    ball = 0
    paddle = 0
    game = {}
    score = 0
    output = 0

    while not program.halt:
        for i in range(3):  # x, y tile_id
            output = program.operation(joystick(ball, paddle))
            game[i] = output
        if game[0] == -1 and game[1] == 0 and output != -1:
            score = game[2]
        if game[2] == 3:
            paddle = game[0]
        elif game[2] == 4:
            ball = game[0]

    return score


def joystick(ball, paddle):
    return 0 if ball == paddle else -1 if ball < paddle else 1


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
