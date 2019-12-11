from collections import defaultdict
import math
import os.path
import requests
import requests_cache


def part1(coords):
    return len(location(coords))


def part2(coords):
    result = next(iter(location(coords)[199]))
    return result[0] * 100 + result[1]


def location(coords):
    result = {}
    for asteroid in coords:
        visible_asteroids = get_visible(asteroid, coords)
        if len(visible_asteroids) > len(result):
            result = visible_asteroids
    return result


def get_visible(source, all_asteroids):
    result = defaultdict(set)

    for target in all_asteroids:
        if source == target:
            continue
        dx = target[0] - source[0]
        dy = target[1] - source[1]
        distance = math.gcd(abs(dx), abs(dy))
        result[(dx // distance, dy // distance)].add(target)

    return [result[k] for k in sorted(result.keys(), key=lambda a: (math.atan2(a[1], a[0]) * (180/math.pi) + 90) % 360)]

def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines


def main():
    lines = get_input_file()
    coords = list((x, y) for y, line in enumerate(lines) for x, a in enumerate(line) if a == '#')

    print(part1(coords))
    print(part2(coords))


if __name__ == "__main__":
    main()
