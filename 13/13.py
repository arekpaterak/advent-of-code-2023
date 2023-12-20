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


def parse_input(input_file):
    with open(input_file, "r") as f:
        patterns = f.read().split("\n\n")

    patterns = [pattern.split("\n") for pattern in patterns]
    patterns = [
        np.array([np.array(list(row)) for row in pattern]) for pattern in patterns
    ]

    return patterns


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    patterns = parse_input(input_file)

    print("--- Part One ---")

    number = 0
    for pattern in patterns:
        found_reflection = False
        for col in range(pattern.shape[1] - 1):
            if col < pattern.shape[-1] // 2:
                left_part = pattern[:, : col + 1]
                right_part = pattern[:, col + 1 : col + 1 + left_part.shape[1]]
            else:
                right_part = pattern[:, col + 1 :]
                left_part = pattern[:, col + 1 - right_part.shape[1] : col + 1]

            # mirror right part
            mirrored_right_part = np.flip(right_part, axis=1)
            if np.array_equal(left_part, mirrored_right_part):
                number += col + 1
                found_reflection = True
                break

        if found_reflection:
            continue

        for row in range(pattern.shape[0] - 1):
            if row < pattern.shape[0] // 2:
                top_part = pattern[: row + 1, :]
                bottom_part = pattern[row + 1 : row + 1 + top_part.shape[0], :]
            else:
                bottom_part = pattern[row + 1 :, :]
                top_part = pattern[row + 1 - bottom_part.shape[0] : row + 1, :]

            # mirror bottom part
            mirrored_bottom_part = np.flip(bottom_part, axis=0)
            if np.array_equal(top_part, mirrored_bottom_part):
                number += (row + 1) * 100
                break

    print("Answer:")
    print(number)

    print("--- Part Two ---")

    number = 0
    for pattern in patterns:
        found_reflection = False
        for col in range(pattern.shape[1] - 1):
            if col < pattern.shape[-1] // 2:
                left_part = pattern[:, : col + 1]
                right_part = pattern[:, col + 1 : col + 1 + left_part.shape[1]]
            else:
                right_part = pattern[:, col + 1 :]
                left_part = pattern[:, col + 1 - right_part.shape[1] : col + 1]

            # mirror right part
            mirrored_right_part = np.flip(right_part, axis=1)
            if len(np.where((left_part == mirrored_right_part) == False)[0]) == 1:
                number += col + 1
                found_reflection = True
                break

        if found_reflection:
            continue

        for row in range(pattern.shape[0] - 1):
            if row < pattern.shape[0] // 2:
                top_part = pattern[: row + 1, :]
                bottom_part = pattern[row + 1 : row + 1 + top_part.shape[0], :]
            else:
                bottom_part = pattern[row + 1 :, :]
                top_part = pattern[row + 1 - bottom_part.shape[0] : row + 1, :]

            # mirror bottom part
            mirrored_bottom_part = np.flip(bottom_part, axis=0)
            if len(np.where((top_part == mirrored_bottom_part) == False)[0]) == 1:
                number += (row + 1) * 100
                break

    print("Answer:")
    print(number)
