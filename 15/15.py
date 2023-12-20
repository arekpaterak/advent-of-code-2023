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


INPUTS = [
    "input.txt",
    "example.txt",
]


def parse_input(input_file: str) -> list[str]:
    with open(input_file, "r") as f:
        lines = f.read().replace("\n", "")
    return lines.split(",")


def hash(string: str):
    current_value = 0
    for character in string:
        ascii_code = ord(character)
        current_value += ascii_code
        current_value *= 17
        current_value %= 256
    return current_value


@dataclass
class Lens:
    label: str
    focal_length: int

    def focusing_power(self, box_number, slot_number):
        return (box_number + 1) * (slot_number + 1) * self.focal_length

    def __str__(self) -> str:
        return f"[{self.label} {self.focal_length}]"

    def __repr__(self) -> str:
        return str(self)


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    initialization_sequence = parse_input(input_file)

    print("--- Part One ---")
    print("Answer:")
    print(sum(hash(step) for step in initialization_sequence))

    print("--- Part Two ---")

    boxes: list[list[Lens]] = [[] for _ in range(256)]

    for step in initialization_sequence:
        if "-" in step:
            label = step[:-1]
            box_index = hash(label)
            box = boxes[box_index]
            for lens in box:
                if lens.label == label:
                    box.remove(lens)
                    break
        else:
            label, focal_length = step.split("=")
            lens = Lens(label, int(focal_length))
            box_index = hash(label)
            box = boxes[box_index]
            for i, existing_lens in enumerate(box):
                if existing_lens.label == label:
                    box[i] = lens
                    break
            else:
                box.append(lens)

        # print(step)
        # for box_index, box in enumerate(boxes):
        #     if box:
        #         print(f"Box {box_index}: {box}")

    print("Answer:")
    focusing_powers = [
        lens.focusing_power(box_index, lens_index)
        for box_index, box in enumerate(boxes)
        for lens_index, lens in enumerate(box)
    ]
    print(sum(focusing_powers))
