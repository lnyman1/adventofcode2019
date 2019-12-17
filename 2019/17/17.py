import os
import requests
import requests_cache
from intcode import IntCode

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

WALL = "#"
MOVE = "."


def part1(lines):
    grid = create_grid(lines)
    intersections = []
    for cell in grid:
        neighbours = [(cell[0] + i[0], cell[1] + i[1]) for i in directions.values()]
        intersect = [i for i in neighbours if i in grid and grid[i] == WALL]
        if len(intersect) == 4:
            intersections.append(cell)
    return sum(x * y for (x, y) in intersections)


def part2(lines):
    lines[0] = 2
    program = IntCode(lines)

    # L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,L,4,L,10,
    # L,4,L,4,L,10,L,6,R,8,R,10,L,6,L,6,L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,L,4,L,10

    main = "A,B,A,B,C,C,B,A,B,C\n"
    A = "L,4,R,8,L,6,L,10\n"
    B = "L,6,R,8,R,10,L,6,L,6\n"
    C = "L,4,L,4,L,10\n"
    return program.operation([ord(i) for i in main + A + B + C + "n\n"])[-1]


def create_grid(lines):
    program = IntCode(lines)
    grid = {}
    coord = (0, 0)

    output = program.operation([0])

    for element in output:
        if element == 35:
            grid[coord] = WALL
            coord = coord[0] + 1, coord[1]
        elif element == 46:
            grid[coord] = MOVE
            coord = coord[0] + 1, coord[1]
        elif element == 10:
            coord = 0, coord[1] + 1

    # unicode_grid = "".join(chr(i) for i in output).split()
    # for line in unicode_grid:
    #     print(line)

    return grid


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
