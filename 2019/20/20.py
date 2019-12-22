import os

import networkx as nx
import requests
import requests_cache

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

WALL = "#"
OPEN = "."

START = "AA"
END = "ZZ"


def part1(lines):
    grid = create_grid(lines)
    portals = get_portal_map(grid)
    graph = create_graph(grid, portals, 1)
    return nx.shortest_path_length(graph, (0, get_start(portals)), (0, get_end(portals)))


def part2(lines):
    grid = create_grid(lines)
    portals = get_portal_map(grid)
    graph = create_graph(grid, portals, len(portals))
    return nx.shortest_path_length(graph, (0, get_start(portals)), (0, get_end(portals)))


def create_grid(lines):
    grid = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x, y)] = lines[y][x]
    return grid


def create_graph(grid, portals, number_levels):
    graph = nx.DiGraph()
    for level in range(number_levels):
        for node in grid.keys():
            if grid[node] != OPEN:
                continue
            for direction in directions.values():
                pos = new_pos(direction, node)
                if grid.get(pos) == OPEN:
                    graph.add_edge((level, node), (level, pos))

        for i in portals.keys():
            if i != START and i != END:
                graph.add_edge((level, portals[i][1]), (level if number_levels == 1 else level + 1, portals[i][0]))
                graph.add_edge((level, portals[i][0]), (level if number_levels == 1 else level - 1, portals[i][1]))
    return graph


def get_portal_map(grid):
    result = {}
    for node, area in grid.items():
        if not area.isalpha():
            continue
        neighbours = get_neighbours(node)
        portal_element = meets_portal_criteria(neighbours, grid)
        entrance = get_entrance(neighbours, grid)
        if len(entrance) == 0:
            continue
        for cell in portal_element:
            portal = "".join([grid[i] for i in sorted([node, cell])])
            if portal not in result.keys():
                result[portal] = [None, None]
            i = 0 if is_outside(grid, entrance[0]) else 1
            result[portal][i] = entrance[0]

    return result


def get_neighbours(node):
    return [new_pos(node, d) for d in directions.values()]


def meets_portal_criteria(neighbours, grid):
    return [i for i in filter(lambda a: a in grid and grid[a].isalpha(), neighbours)]


def get_entrance(neighbours, grid):
    return [i for i in filter(lambda a: a in grid and grid[a] == OPEN, neighbours)]


def get_start(portals):
    return [portals[i][0] for i in portals if i == START][0]


def get_end(portals):
    return [portals[i][0] for i in portals if i == END][0]


def is_outside(grid, node):
    x = {c[0] for c in grid.keys()}
    y = {c[1] for c in grid.keys()}
    return get_grid_min(node[0], x) or get_grid_max(node[0], x) or get_grid_min(node[1], y) or get_grid_max(node[1], y)


def get_grid_min(node, i):
    return abs(node - min(i)) <= 2


def get_grid_max(node, i):
    return abs(node - max(i)) <= 2


def new_pos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.splitlines()
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
