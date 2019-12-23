import os

import requests
import requests_cache
from intcode import IntCode


def part1(lines):
    programs = [IntCode(lines) for _ in range(50)]
    [programs[i].add_input(i) for i in range(50)]
    return process_packets(programs, True)


def part2(lines):
    programs = [IntCode(lines) for _ in range(50)]
    [programs[i].add_input(i) for i in range(50)]
    return process_packets(programs, False)


def process_packets(programs, initial):
    idle = [0 for _ in range(50)]
    packet = (None, None)
    previous_y_packet = -1

    while True:
        for i, prog in enumerate(programs):
            addr = prog.get_next_output()
            if addr is None:
                prog.add_input(-1)
                idle[i] += 1
                continue
            x, y = prog.get_x_next_output(2)
            if addr == 255:
                if initial:
                    return y
                # print(addr, x, y)
                packet = (x, y)
            else:
                programs[addr].add_input(x).add_input(y)
            idle[i] = 0

        if all([i > 2 for i in idle]):
            y_value = packet[1]
            if previous_y_packet and previous_y_packet == y_value:
                return previous_y_packet
            previous_y_packet = y_value
            programs[0].add_input(packet[0]).add_input(y_value)


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
