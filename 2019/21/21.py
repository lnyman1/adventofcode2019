import os
import requests
import requests_cache
from intcode import IntCode


def part1(lines):
    program = IntCode(lines)

    inputs = [
        "NOT A J\n",
        "NOT B T\n",
        "OR T J\n",
        "NOT C T\n",
        "OR T J\n",
        "AND D J\n",
        "WALK\n"
    ]

    output = program.operation([ord(i) for i in "".join(inputs)])
    return output[-1]


def part2(lines):
    program = IntCode(lines)

    inputs = [
        "NOT A J\n",
        "NOT B T\n",
        "OR T J\n",
        "NOT C T\n",
        "OR T J\n",
        "AND D J\n",
        "NOT T T\n",
        "OR E T\n",
        "OR H T\n",
        "AND T J\n",
        "RUN\n",
    ]

    output = program.operation([ord(i) for i in "".join(inputs)])
    return output[-1]


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
