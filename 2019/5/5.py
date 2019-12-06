import os
import requests
import requests_cache


def part1(lines):
    return operation(lines, 1)


def part2(lines):
    return operation(lines, 5)


def operation(lines, input):
    output = 0
    pointer = 0

    instruction = [int(x) for x in lines]

    for _ in range(len(instruction)):
        code = parse(instruction[pointer])

        opcode = code[0]

        if opcode == 99:
            return output

        param1 = process_param(code, instruction, pointer, 1)
        param2 = process_param(code, instruction, pointer, 2)
        param3 = process_param(code, instruction, pointer, 3)

        if opcode == 1:
            instruction[param3] = instruction[param1] + instruction[param2]
            pointer += 4
        elif opcode == 2:
            instruction[param3] = instruction[param1] * instruction[param2]
            pointer += 4
        elif opcode == 3:
            instruction[param1] = input
            pointer += 2
        elif opcode == 4:
            output = instruction[param1]
            pointer += 2
        elif opcode == 5:
            pointer = instruction[param2] if instruction[param1] != 0 else add(pointer, 3)
        elif opcode == 6:
            pointer = instruction[param2] if instruction[param1] == 0 else add(pointer, 3)
        elif opcode == 7:
            value = 1 if instruction[param1] < instruction[param2] else 0
            instruction[param3] = value
            pointer += 4
        elif opcode == 8:
            value = 1 if instruction[param1] == instruction[param2] else 0
            instruction[param3] = value
            pointer += 4


def add(pointer, value):
    pointer += value
    return pointer


def process_param(code, instruction, pointer, idx):
    return pointer + idx if code[idx] == 1 else instruction[pointer + idx]


def parse(instruction):
    DE = instruction % 100
    C = instruction // 100 % 10
    B = instruction // 1000 % 10
    A = instruction // 10000 % 10
    return DE, C, B, A


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().split(",")
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
