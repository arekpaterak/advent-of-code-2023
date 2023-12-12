from __future__ import annotations

import sys
from dataclasses import dataclass
import math

import time

INPUTS = ["input.txt", "example2.txt"]


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

    def is_ghost_start(self) -> bool:
        return self.name[-1] == "A"

    def is_ghost_end(self) -> bool:
        return self.name[-1] == "Z"

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

    print("--- Part Two ---")
    start_nodes = [node for node in nodes.values() if node.is_ghost_start()]

    start_time = time.time()

    cycle_lengths = []
    for start_node in start_nodes:
        current_node = start_node
        step = 0

        while not current_node.is_ghost_end():
            instruction = instructions[step % len(instructions)]

            if instruction == "L":
                current_node = nodes[current_node.left]
            elif instruction == "R":
                current_node = nodes[current_node.right]
            else:
                raise ValueError(f"Unknown instruction {instruction}")

            step += 1

        cycle_lengths.append(step)

    steps = math.lcm(*cycle_lengths)

    end_time = time.time()

    print("Answer:")
    print(steps, end="\n\n")

    print("How long to get the answer?")
    print(f"{end_time - start_time} s\n")

    print("How long would the brute force approach take?")
    current_nodes = start_nodes
    i = 0

    start_time = time.time()
    elapsed_time = None
    while not all([node.is_ghost_end() for node in current_nodes]):
        instruction = instructions[i % len(instructions)]

        current_nodes = [
            nodes[node.left] if instruction == "L" else nodes[node.right]
            for node in current_nodes
        ]
        i += 1

        if i == 1_000_000:
            end_time = time.time()
            elapsed_time = end_time - start_time
            break

    print(f"{elapsed_time * (steps / 1_000_000) / 3600 / 24 / 365 : .1f} years")
