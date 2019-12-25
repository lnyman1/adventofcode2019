import os

import requests
import requests_cache

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

BUG = "#"
EMPTY = "."


def part1(lines):
    grid = create_grid(lines)
    previous_layout = set()

    while True:
        biodiversity = calc_biodiversity(grid)
        if biodiversity in previous_layout:
            return biodiversity
        previous_layout.add(biodiversity)
        grid = apply_minute(grid)


def part2(lines):
    grid_from_input = create_grid(lines)
    iterations = 200
    grids_with_depth = [{} for _ in range(iterations)]
    grids_with_depth[int(iterations / 2)] = grid_from_input
    for _ in range(iterations):
        grids_with_depth = iterate(grids_with_depth, iterations, get_coords_size(grid_from_input))
    return sum([cell.count(BUG) for grid in grids_with_depth for cell in grid.values()])

def get_coords_size(grid_from_input):
    x = max(grid_from_input)[0] - min(grid_from_input)[0]
    y = max(grid_from_input)[1] - min(grid_from_input)[1]
    return x, y

def total_neighbours(grids, coord, depth, iterations, size):
    neighbours = 0
    x = size[0] / 2
    y = size[1] / 2
    if coord != (x, y):
        neighbours += sum([grids[depth].get(new_pos(coord, direction), EMPTY).count(BUG) for direction in directions.values()])

    higher_level = depth + 1
    if depth < iterations - 1:
        switcher = {
            0: (x - 1, y),
            4: (x + 1, y)
        }
        neighbours += add_cell(coord[0], grids[higher_level], switcher.get(coord[0]), size[0])

        switcher = {
            0: (x, y - 1),
            4: (x, y + 1)
        }
        neighbours += add_cell(coord[1], grids[higher_level], switcher.get(coord[1]), size[1])

    lower_level = depth - 1
    if coord in get_neighbours((x, y)) and depth > 0:
        switcher = {
            (x, y - 1): get_x_coords(0, size),
            (x - 1, y): get_y_coords(0, size),
            (x, y + 1): get_x_coords(size[0], size),
            (x + 1, y): get_y_coords(size[1], size)
        }
        coords = switcher.get(coord)
        neighbours += sum([grids[lower_level][coord].count(BUG) for coord in coords if coord in grids[lower_level]])

    return neighbours


def get_x_coords(i, size):
    return {(x, i) for x in range(size[0] + 1)}


def get_y_coords(i, size):
    return {(i, y) for y in range(size[1] + 1)}


def iterate(grids, iterations, size):
    new_grids = [{} for _ in range(0, len(grids))]
    for depth, grid in enumerate(grids):
        for y in range(size[1] + 1):
            for x in range(size[0] + 1):
                new_grids[depth][(x, y)] = rules_with_depth(grids, grid, iterations, depth, (x, y), size)
    return new_grids


def add_cell(i, grid, coords, size):
    return 1 if (i == 0 or i == size) and coords in grid and grid[coords] == BUG else 0


def apply_minute(grid):
    state = grid.copy()
    for key, value in grid.items():
        state[key] = rules(key, value, grid)
    return state


def rules(cell, value, grid):
    if value == BUG:
        return BUG if get_number_of_adjacent_bugs(cell, grid) == 1 else EMPTY
    number_of_adjacent_bugs = get_number_of_adjacent_bugs(cell, grid)
    return BUG if 1 <= number_of_adjacent_bugs <= 2 else EMPTY


def rules_with_depth(grids, grid, iterations, depth, coord, size):
    neighbours = total_neighbours(grids, coord, depth, iterations, size)
    if coord in grid and grid[coord] == BUG:
        return BUG if neighbours == 1 else EMPTY
    else:
        return BUG if 1 <= neighbours <= 2 else EMPTY


def get_number_of_adjacent_bugs(cell, grid):
    return len([i for i in get_neighbours(cell) if i in grid and grid[i] == BUG])


def get_neighbours(node):
    return [new_pos(node, d) for d in directions.values()]


def new_pos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def calc_biodiversity(grid):
    result = 0
    power = 1
    for key, value in grid.items():
        if value == BUG:
            result += power
        power *= 2
    return result


def create_grid(lines):
    grid = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x, y)] = lines[y][x]
    return grid


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
