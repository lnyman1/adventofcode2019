import os
import requests
import requests_cache

def part1(numbers):
    base_pattern = [0, 1, 0, -1]
    phase = 0
    while phase < 100:
        phase_result = []
        for i in range(len(numbers)):
            phase_result.append(abs(sum(numbers[j] * base_pattern[((j + 1) // (i + 1)) % 4] for j in range(len(numbers)))) % 10)
        numbers = phase_result
        phase += 1

    return int(''.join(map(str, numbers[0:8])))

def part2(numbers):
    inputs = numbers * 10000
    offset = int(''.join(map(str, inputs[:7])))

    for phase in range(100):
        phase_result = sum(inputs[i] for i in range(offset, len(inputs), 1))
        for i in range(offset, len(inputs), 1):
            phase_result -= inputs[i]
            inputs[i] = abs(phase_result + inputs[i]) % 10

    return int(''.join(map(str, inputs[offset:offset + 8])))


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip()
    return lines


def main():
    lines = get_input_file()
    numbers = [int(d) for d in str(lines)]
    print(part1(numbers))
    print(part2(numbers))


if __name__ == "__main__":
    main()
