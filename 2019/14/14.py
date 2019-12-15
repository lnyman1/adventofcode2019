import math
import os
import re
from collections import defaultdict
from typing import List

import requests
import requests_cache


class Chemical:
    amount: int
    name: str

    def __init__(self, amount, name):
        self.amount = int(amount)
        self.name = name

    @staticmethod
    def parse(line):
        elements = line.split(" ")
        return Chemical(elements[0], elements[1])


class Reaction:
    inputs: List[Chemical]
    output: Chemical

    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output


def part1(lines):
    return get_requirement(get_reactions(lines), 1)


def part2(lines):
    return binary_search(0, 1e12, get_reactions(lines))


def get_reactions(lines):
    reactions = defaultdict()
    for line in lines:
        inputs, output = line.split(" => ")
        reaction = Reaction([Chemical.parse(i) for i in re.findall(r'\d+ \w+', inputs)],
                            [Chemical.parse(i) for i in re.findall(r'\d+ \w+', output)][0])
        reactions[reaction.output.name] = reaction
    return reactions


def binary_search(first, last, reactions):
    high = last
    while last - first > 1:
        val = first + (last - first) // 2
        if get_requirement(reactions, val) > high:
            last = val
        else:
            first = val
    return first


def get_requirement(reactions, quantity):
    result = 0
    requirements = [Chemical(quantity, "FUEL")]
    available = {}

    while len(requirements) != 0:
        req = requirements.pop()
        equation = reactions.get(req.name)
        amount_required = equation.output.amount

        available_amount = available[req.name] if req.name in available else 0
        amount_used = min(req.amount, available_amount)
        req.amount -= amount_used
        available[req.name] = math.ceil(req.amount / amount_required) * amount_required + available_amount - amount_used - req.amount

        for ins in equation.inputs:
            amount_needed = math.ceil(req.amount / amount_required) * ins.amount
            if ins.name == "ORE":
                result += amount_needed
            else:
                requirements.append(Chemical(amount_needed, ins.name))

    return result


def get_input_file():
    requests_cache.install_cache('../cache')
    path = os.path.abspath(__file__).split('/')
    url = 'https://adventofcode.com/' + path[-3] + '/day/' + path[-2] + '/input'
    lines = requests.get(url, cookies={"session": os.environ['SESSION']}).text.strip().splitlines()
    return lines


def main():
    lines = get_input_file()

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
