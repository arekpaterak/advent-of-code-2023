from __future__ import annotations
from enum import Enum, auto
from functools import reduce, total_ordering
import random

import sys
from dataclasses import dataclass
import math
import numpy as np
import re
import itertools
import sympy


INPUTS = ["input.txt", "example1_1.txt", "example1_2.txt"]


@dataclass
class Node:
    name: str
    left: str = None
    right: str = None

    @classmethod
    def from_string(cls, string) -> Node:
        name, children = string.split(" = ")
        children = children.replace("(", "").replace(")", "").split(",")

        left_name, right_name = [child.strip() for child in children]

        return cls(name, left_name, right_name)

    def is_start(self) -> bool:
        if self.name == "AAA":
            return True
        else:
            return False

    def is_end(self) -> bool:
        if self.name == "ZZZ":
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.name} = ({self.left}, {self.right})"


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.read().splitlines()
    lines = [line.strip() for line in lines]

    instructions = lines[0]

    nodes = {}

    for line in lines[2:]:
        node = Node.from_string(line)
        nodes[node.name] = node

    return instructions, nodes


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    instructions, nodes = parse_input(input_file)

    print("--- Part One ---")
    start_node = nodes["AAA"]
    current_node = start_node
    i = 0

    while not current_node.is_end():
        instruction = instructions[i % len(instructions)]

        if instruction == "L":
            current_node = nodes[current_node.left]
        elif instruction == "R":
            current_node = nodes[current_node.right]
        else:
            raise ValueError(f"Unknown instruction {instruction}")

        i += 1

    print("Answer:")
    print(i)
