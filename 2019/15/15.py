import os
from collections import defaultdict
import networkx as nx
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
OXYGEN = "x"
MOVE = "."


def part1(lines):
    program = IntCode(lines)
    grid = create_grid(program)

    graph = nx.Graph()
    for coord, area in grid.items():
        if not area == WALL:
            graph.add_node(coord)
            new_positions = [new_pos(coord, d) for d in directions.values()]
            not_blocking = [i for i in new_positions if not grid[i] == WALL]
            for edge in not_blocking:
                graph.add_edge(coord, edge)
    path = nx.shortest_path_length(graph, (0, 0), get_target(grid))

    return path


def part2(lines):
    program = IntCode(lines)
    grid = create_grid(program)
    return fill_oxygen(grid, get_target(grid), 0, 0)


def get_target(grid):
    return [i for i in grid if grid[i] == OXYGEN][0]


def new_pos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def create_grid(program):
    known_cells = defaultdict(int)
    grid = defaultdict(str)
    pos = (0, 0)

    while not program.halt and sum(known_cells.values()) < 10000:  # arbitrary high number
        direction = find_next_area(grid, pos, known_cells)
        output = program.operation(direction)
        move = directions[direction]
        known_cells[pos] += 1

        if output == 0:
            new_position = new_pos(pos, move)
            grid[new_position] = WALL

        else:
            pos = new_pos(pos, move)
            grid[pos] = MOVE if output == 1 else OXYGEN

    return grid


def find_next_area(grid, pos, known_cells):
    new_positions = [{"id": d[0], "pos": new_pos(pos, d[1])} for d in directions.items()]
    idx = [x for x in new_positions if x["pos"] not in grid]
    if len(idx) > 0:
        return idx[0]["id"]

    least_visited_cells = 10000  # arbitrary high number
    least_visited = {}

    not_blocked_positions = [x for x in new_positions if grid[x["pos"]] != "#"]
    for i in not_blocked_positions:
        if least_visited_cells > known_cells[i["pos"]]:
            least_visited_cells = known_cells[i["pos"]]
            least_visited = i
    return least_visited["id"]


def fill_oxygen(grid, target, time, total):
    new_positions = [new_pos(target, d) for d in directions.values()]
    for pos in new_positions:
        if grid[pos] == MOVE:
            grid[pos] = OXYGEN
            total = fill_oxygen(grid, pos, time + 1, total)
    return max(time, total)


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
