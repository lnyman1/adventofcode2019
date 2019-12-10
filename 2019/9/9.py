import os
import requests
import requests_cache


def part1(lines):
    return operation(lines, 1)


def part2(lines):
    return operation(lines, 2)


def operation(lines, input):
    memory = lines + [0] * 200  # extra memory required
    pointer = 0
    relative_base = 0
    output = 0

    while pointer < len(lines):
        code = parse(memory[pointer])
        opcode = code[0]

        if opcode == 99:
            return output

        param1 = process_param(code, memory, pointer, 1, relative_base)
        param2 = process_param(code, memory, pointer, 2, relative_base)
        param3 = process_param(code, memory, pointer, 3, relative_base)

        if opcode == 1:
            memory[param3] = memory[param1] + memory[param2]
            pointer += 4
        elif opcode == 2:
            memory[param3] = memory[param1] * memory[param2]
            pointer += 4
        elif opcode == 3:
            memory[param1] = input
            pointer += 2
        elif opcode == 4:
            output = memory[param1]
            pointer += 2
        elif opcode == 5:
            pointer = memory[param2] if memory[param1] != 0 else add(pointer, 3)
        elif opcode == 6:
            pointer = memory[param2] if memory[param1] == 0 else add(pointer, 3)
        elif opcode == 7:
            value = 1 if memory[param1] < memory[param2] else 0
            memory[param3] = value
            pointer += 4
        elif opcode == 8:
            value = 1 if memory[param1] == memory[param2] else 0
            memory[param3] = value
            pointer += 4
        elif opcode == 9:
            relative_base += memory[param1]
            pointer += 2


def add(pointer, value):
    pointer += value
    return pointer


def process_param(code, instruction, pointer, idx, relative_base):
    mode = code[idx]
    if mode == 0:
        return instruction[pointer + idx]
    elif mode == 1:
        return pointer + idx
    elif mode == 2:
        return instruction[pointer + idx] + relative_base


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
    instruction = list(map(int, lines))
    print(part1(instruction))
    print(part2(instruction))


if __name__ == "__main__":
    main()
