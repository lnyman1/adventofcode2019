from collections import deque
import requests
import requests_cache
import os
import networkx as nx
from dataclasses import dataclass

directions = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}

ENTRANCE = "@"
WALL = "#"
OPEN = "."


class Robot:
    start_pos: tuple
    keys_in_grid: dict
    keys_to_collect: set
    key_to_key_path: dict

    def __init__(self, start, grid, keys_in_grid):
        graph = create_graph(start, grid)
        robot_keys_in_grid = {}
        for k in keys_in_grid:
            if keys_in_grid[k] in graph.nodes:
                robot_keys_in_grid[k] = keys_in_grid[k]
        robot_keys_to_collect = {k for k in key_letters_in_grid(keys_in_grid) if keys_in_grid[k] in graph.nodes}
        paths = create_key_to_key_paths(start, graph, robot_keys_in_grid)

        self.start_pos = start
        self.keys_in_grid = robot_keys_in_grid
        self.keys_to_collect = robot_keys_to_collect
        self.key_to_key_path = paths


@dataclass(frozen=True)
class Key:
    letter: str
    position: tuple
    path_length: int


@dataclass(unsafe_hash=True)
class CacheKey:
    robot_position: tuple
    keys_collected: str

    def __init__(self, robot_position, keys_collected):
        self.robot_position = robot_position
        self.keys_collected = ''.join(sorted(keys_collected))


@dataclass(frozen=True)
class QueueEntry:
    positions: tuple
    path_length: int
    keys_collected: tuple


def part1(lines):
    grid = create_grid(lines)
    start = get_start_positions(grid)[0]
    keys_in_grid = get_keys_in_grid(grid)
    return shortest_path([Robot(start, grid, keys_in_grid)], grid, key_letters_in_grid(keys_in_grid))


def part2(lines):
    grid = create_grid(lines)
    grid = modify_grid_starting_pos(grid, get_start_positions(grid)[0])
    starts = get_start_positions(grid)
    keys_in_grid = get_keys_in_grid(grid)
    robots = [Robot(start, grid, keys_in_grid) for start in starts]
    return shortest_path(robots, grid, key_letters_in_grid(keys_in_grid))


def create_grid(lines):
    grid = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            grid[(x, y)] = lines[x][y]
    return grid


def get_start_positions(grid):
    return [i for i in grid if grid[i] == ENTRANCE]


def new_pos(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def get_potential_keys():
    return {chr(i) for i in range(ord('a'), ord('z') + 1)}


def get_keys_in_grid(grid):
    return dict((value, key) for key, value in filter(lambda a: a[1] in get_potential_keys(), grid.items()))


def key_letters_in_grid(keys_in_grid):
    return {i for i in keys_in_grid.keys()}


def modify_grid_starting_pos(grid, start):
    grid[start] = WALL
    for d in directions.values():
        grid[new_pos(start, d)] = WALL
    for x in [-1, 1]:
        for y in [-1, 1]:
            grid[new_pos(start, (x, y))] = ENTRANCE
    return grid


def create_graph(start, grid):
    graph = nx.Graph()
    queue = deque([start])
    visited_node = set()
    while queue:
        node = queue.popleft()
        if node in visited_node:
            continue
        visited_node.add(node)
        for direction in directions.values():
            pos = new_pos(node, direction)
            if grid[pos] != WALL and pos not in visited_node:
                graph.add_edge(node, pos)
                queue.append(pos)
    return graph


def create_key_to_key_paths(start, graph, keys_in_grid):
    paths = {}
    keys_in_grid[ENTRANCE] = start
    for letter in keys_in_grid.keys():
        keys = key_letters_in_grid(keys_in_grid)
        keys.remove(letter)
        source = keys_in_grid[letter]
        for key in keys:
            target = keys_in_grid[key]
            paths[(source, target)] = nx.shortest_path(graph, source, target)
            paths[(target, source)] = paths[source, target][::-1]
    return paths


def find_keys(pos, grid, cells, keys_to_collect, keys_in_grid, paths):
    keys = []
    for key in keys_to_collect:
        path = paths[(pos, keys_in_grid[key])]
        if any(grid[i] not in cells for i in path):
            continue
        keys.append(Key(key, keys_in_grid[key], len(path) - 1))
    return keys


def get_robot_keys(grid, robots, robot_keys_collected, robot_position):
    robot_keys = []
    cells = get_potential_keys()
    cells.add(ENTRANCE)
    cells.add(OPEN)
    cells.update(set(k.upper() for k in robot_keys_collected))
    for i, pos in enumerate(robot_position):
        robot = robots[i]
        keys = find_keys(pos, grid, cells, robot.keys_to_collect - set(robot_keys_collected), robot.keys_in_grid,
                         robot.key_to_key_path)
        sorted_keys = sorted(keys, key=lambda k: k.path_length)
        for key in sorted_keys:
            robot_keys.append((i, key))
    return robot_keys


def shortest_path(robots, grid, keys_to_collect):
    robot_positions = tuple(r.start_pos for r in robots)
    queue = deque([QueueEntry(robot_positions, 0, ())])
    key_retrieved = -1
    path_cache = {}
    path_result = []

    while queue:
        queue_entry = queue.popleft()
        robot_position = queue_entry.positions
        path_length = queue_entry.path_length
        robot_keys_collected = queue_entry.keys_collected

        if 0 <= key_retrieved <= path_length:
            continue

        if len(keys_to_collect) == len(robot_keys_collected):
            key_retrieved = path_length
            path_result.append(path_length)

        key = CacheKey(robot_position, robot_keys_collected)

        if key in path_cache:
            path, robot_keys = path_cache[key]
            if path <= path_length:
                continue
        else:
            robot_keys = get_robot_keys(grid, robots, robot_keys_collected, robot_position)

        path_cache[key] = path_length, robot_keys
        for i, k in robot_keys:
            positions = robot_position[:i] + (k.position,) + robot_position[i + 1:]
            queue.append(QueueEntry(positions, path_length + k.path_length, robot_keys_collected + (k.letter,)))

    return min(path_result)


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
