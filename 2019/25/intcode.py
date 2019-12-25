from collections import deque
from typing import List


class IntCode:
    lines: List[int]
    memory: List[int]
    pointer: int
    relative_base: int
    halt: bool
    result: List[int]
    inputs: deque

    def __init__(self, lines):
        self.lines = lines
        self.memory = lines + [0] * 100000  # extra memory required
        self.pointer = 0
        self.relative_base = 0
        self.halt = False
        self.result = []
        self.inputs = deque()

    def operation(self):
        while self.pointer < len(self.memory):
            code = self.parse(self.memory[self.pointer])
            opcode = code[0]

            if opcode == 99:
                self.halt = True
                return self.result

            param1 = self.process_param(code, 1)
            param2 = self.process_param(code, 2)
            param3 = self.process_param(code, 3)

            if opcode == 1:
                self.memory[param3] = self.memory[param1] + self.memory[param2]
                self.pointer += 4
            elif opcode == 2:
                self.memory[param3] = self.memory[param1] * self.memory[param2]
                self.pointer += 4
            elif opcode == 3:
                if len(self.inputs) == 0:
                    return
                self.memory[param1] = self.inputs.popleft()
                self.pointer += 2
            elif opcode == 4:
                output = self.memory[param1]
                self.pointer += 2
                self.result.append(output)
            elif opcode == 5:
                self.pointer = self.memory[param2] if self.memory[param1] != 0 else self.add(3)
            elif opcode == 6:
                self.pointer = self.memory[param2] if self.memory[param1] == 0 else self.add(3)
            elif opcode == 7:
                value = 1 if self.memory[param1] < self.memory[param2] else 0
                self.memory[param3] = value
                self.pointer += 4
            elif opcode == 8:
                value = 1 if self.memory[param1] == self.memory[param2] else 0
                self.memory[param3] = value
                self.pointer += 4
            elif opcode == 9:
                self.relative_base += self.memory[param1]
                self.pointer += 2

    def add(self, value):
        self.pointer += value
        return self.pointer

    def add_input(self, value):
        self.inputs.append(value)
        return self

    def take_output(self):
        output = self.result
        self.result = []
        return output

    def process_param(self, code, idx):
        mode = code[idx]
        if mode == 0:
            return self.memory[self.pointer + idx]
        elif mode == 1:
            return self.pointer + idx
        elif mode == 2:
            return self.memory[self.pointer + idx] + self.relative_base

    def reset(self):
        self.memory = self.lines + [0] * 100000  # extra memory required
        self.pointer = 0
        self.relative_base = 0
        self.halt = False
        self.result = []
        self.inputs = deque()

    def parse(self, instruction):
        DE = instruction % 100
        C = instruction // 100 % 10
        B = instruction // 1000 % 10
        A = instruction // 10000 % 10
        return DE, C, B, A
