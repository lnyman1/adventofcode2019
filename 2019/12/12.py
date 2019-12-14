import math
import os
import re

import requests
import requests_cache


def part1(lines):
    moons = get_moons(lines)

    for i in range(1000):
        moons = step(moons)

    return sum((abs(x) + abs(y) + abs(z)) * (abs(a) + abs(b) + abs(c)) for x, y, z, a, b, c in moons)

def part2(lines):
    moons = get_moons(lines)

    x_result = [-1, set()]
    y_result = [-1, set()]
    z_result = [-1, set()]

    count = 0
    while True:
        if x_result[0] > 0 and y_result[0] > 0 and z_result[0] > 0:
            break
        moons = step(moons)
        x_result = process(x_result[0], x_result[1], count, moons, 0)
        y_result = process(y_result[0], y_result[1], count, moons, 1)
        z_result = process(z_result[0], z_result[1], count, moons, 2)
        count += 1

    return lcm(x_result[0], lcm(y_result[0], z_result[0]))

def get_moons(lines):
    moons = []
    for line in lines:
        x, y, z = map(int, re.findall(r'-?\d+', line))
        moons.append([x, y, z, 0, 0, 0])
    return moons

def step(moons):
    seen = []
    result = moons[:]
    for x in range(len(moons)):
        for y in range(len(moons)):
            for z in range(3):
                if (moons[y], moons[x]) in seen or x == y:
                    continue
                if moons[x][z] < moons[y][z]:
                    result[x][3+z] += 1
                    result[y][3+z] -= 1
                elif moons[x][z] > moons[y][z]:
                    result[x][3+z] -= 1
                    result[y][3+z] += 1
            seen.append((moons[x], moons[y]))

    return [[x + a, y + b, z + c, a, b, c] for x, y, z, a, b, c in result]

def process(axis, seen, count, moons, idx):
    if axis < 0:
        coords = str([item for sublist in [[a[idx], a[idx + 3]] for a in moons] for item in sublist])
        if coords in seen:
            axis = count
        else:
            seen.add(coords)
    return axis, seen

def lcm(a, b):
    return a * b // math.gcd(a, b)

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
