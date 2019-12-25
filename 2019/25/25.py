import os
import re

import random
import requests
import requests_cache
from intcode import IntCode

directions = {
    1: "south",
    2: "north",
    3: "west",
    4: "east"
}

CANT_GO_WAY = "You can't go that way."
PRESSURE = "== Pressure-Sensitive Floor =="
HEAVIER = "Alert! Droids on this ship are heavier than the detected value!"
LIGHTER = "Alert! Droids on this ship are lighter than the detected value!"


def part1(lines):
    program = IntCode(lines)
    random.seed(2)
    forbidden_objects = ["photons", "infinite loop", "escape pod", "giant electromagnet", "molten lava"]
    objects_to_collect = []
    objects_to_take = []
    while True:
        program.operation()
        output = program.take_output()
        output_words = "".join([chr(i) for i in output])
        print(output_words)

        if CANT_GO_WAY in output_words:
            break

        if PRESSURE in output_words:
            if HEAVIER not in output_words and LIGHTER not in output_words:
                return (re.findall(r'typing \d+', output_words)[0]).split(" ")[1]
            program.reset()
            objects_to_take = []
            for object in objects_to_collect:
                if not not random.getrandbits(1):
                    objects_to_take.append(object)

        for word in output_words.split("\n"):
            if word.startswith("- "):
                out_word = word[2:]

                if out_word not in directions.values() and out_word not in forbidden_objects and out_word in objects_to_take:
                    print("Taken: " + out_word)
                    [program.add_input(ord(i)) for i in "take " + out_word + "\n"]

                if out_word not in directions.values() and out_word not in forbidden_objects and out_word not in objects_to_collect:
                    print("Found new object: " + out_word)
                    objects_to_collect.append(out_word)

        generate_command(output_words, program)


def generate_command(output_words, program):
    while True:
        next_dir = directions.get(random.randint(1, len(directions)))
        if next_dir in output_words:
            print(">> " + next_dir)
            c = [ord(i) for i in next_dir + "\n"]
            for i in c:
                program.add_input(i)
            break


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


if __name__ == "__main__":
    main()


