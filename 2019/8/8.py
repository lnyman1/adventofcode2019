import os
import numpy as np
import matplotlib.pyplot as plt
import requests
import requests_cache

width = 25
height = 6

def part1(lines):
    layers = np.array(lines).reshape(-1, height, width)
    layer_min_zero = min(layers, key=lambda a: (a == 0).sum())
    return (layer_min_zero == 1).sum() * (layer_min_zero == 2).sum()


def part2(lines):
    layers = np.array(lines).reshape(-1, height, width)
    img = np.zeros((height, width))
    for h in range(height):
        for w in range(width):
            for layer in range(int(len(lines) / (height * width))):
                if layers[layer][h][w] == 2:
                    continue
                img[h][w] = 1 if layers[layer][h][w] == 1 else 0
                break
    return img

def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip()
    return lines


def main():
    lines = get_input_file()
    numbers = list(map(int, lines))

    print(part1(numbers))
    plt.imsave("part2.png", part2(numbers))


if __name__ == "__main__":
    main()
