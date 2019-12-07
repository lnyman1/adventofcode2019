import itertools
import os
import requests
import requests_cache


def part1(lines):
    permutations = list(itertools.permutations(range(5)))
    results = set()
    for permutation in permutations:
        output = [0]
        for phase in permutation:
            output = operation(lines, phase, output[0])
        results.add(output[0])
    return max(results)


def part2(lines):
    permutations = list(itertools.permutations(range(5, 10)))
    return max(feedback_loop(lines, permutations))

def feedback_loop(lines, permutations):
    results = set()
    for permutation in permutations:
        amps = [[i for i in lines] for _ in range(len(permutation))]
        pointers = [0 for _ in range(len(permutation))]
        amp_idx = 0
        inputs = [0]
        use_phase = True
        while True:
            output = operation(amps[amp_idx], permutation[amp_idx], inputs[-1], pointers[amp_idx], use_phase)
            if output[2]:
                break
            pointers[amp_idx] = output[1]
            inputs.append(output[0])
            amp_idx = (amp_idx + 1) % len(amps)
            if amp_idx == 0:
                use_phase = False

        results.add(inputs[-1])
    return results

def operation(instruction, phase, inputs, pointer=0, phase_flag=True):
    output = 0
    for _ in range(len(instruction)):
        code = parse(instruction[pointer])
        opcode = code[0]

        if opcode == 99:
            return output, pointer, True

        param1 = process_param(code, instruction, pointer, 1)
        param2 = process_param(code, instruction, pointer, 2) if opcode != 4 else 0
        param3 = process_param(code, instruction, pointer, 3) if opcode != 4 else 0

        if opcode == 1:
            instruction[param3] = instruction[param1] + instruction[param2]
            pointer += 4
        elif opcode == 2:
            instruction[param3] = instruction[param1] * instruction[param2]
            pointer += 4
        elif opcode == 3:
            instruction[param1] = phase if phase_flag else inputs
            phase_flag = False
            pointer += 2
        elif opcode == 4:
            output = instruction[param1]
            pointer += 2
            return output, pointer, False
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
    instruction = list(map(int, lines))
    print(part1(instruction))
    print(part2(instruction))


if __name__ == "__main__":
    main()
