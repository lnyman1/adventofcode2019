import os
import requests
import requests_cache

def part1(lines):
    return ()


def part2(lines):
    return ()

def get_input_file():
    requests_cache.install_cache('../cache')
    url = 'https://adventofcode.com/' + os.path.abspath(__file__).split('/')[-3] + '/day/' + __file__.split('.')[
        0] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines

def main():
    lines = get_input_file()

    print(part1(list(lines)))
    print(part2(list(lines)))

if __name__ == "__main__":
    main()