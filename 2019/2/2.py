import os
import requests
import requests_cache


def part1(lines):
    # position 1 with the value 12 and replace position 2 with the value 2
    result = operation(lines, 12, 2)
    return result[0]


def part2(lines):
    original = lines[:]
    for i in range(100):
        for j in range(100):

            lines = operation(original, i, j)

            if lines[0] == 19690720:
                return 100 * i + j


def operation(lines, noun, verb):
    numbers = [int(x) for x in lines]
    numbers[1] = noun
    numbers[2] = verb

    for i in range(0, len(numbers), 4):
        opcode = numbers[i]

        if opcode == 99:
            return numbers

        idx1 = numbers[i + 1]
        idx2 = numbers[i + 2]
        output_pos = numbers[i + 3]

        if opcode == 1:
            numbers[output_pos] = numbers[idx1] + numbers[idx2]

        elif opcode == 2:
            numbers[output_pos] = numbers[idx1] * numbers[idx2]

def get_input_file():
    requests_cache.install_cache('../cache')
    url = 'https://adventofcode.com/' + os.path.abspath(__file__).split('/')[-3] + '/day/' + __file__.split('.')[
        0] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().split(",")
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
