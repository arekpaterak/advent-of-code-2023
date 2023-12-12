from __future__ import annotations

import sys
import numpy as np


INPUTS = ["input.txt", "example.txt"]


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [np.array(list(map(lambda x: int(x), line.split()))) for line in lines]
    return lines


def extrapolate_forwards(history: np.ndarray):
    last_values = [history[-1]]
    sequence = history
    while True:
        diff = np.diff(sequence)
        # print(diff)
        last_values.append(diff[-1])
        if all(diff == 0):
            break
        sequence = diff

    return sum(last_values)


def extrapolate_backwards(history: np.ndarray):
    first_values = [history[0]]
    sequence = history
    while True:
        diff = np.diff(sequence)
        # print(diff)
        first_values.append(diff[0])
        if all(diff == 0):
            break
        sequence = diff

    current_value = 0
    for value in first_values[::-1]:
        # print(value)
        current_value = value - current_value

    return current_value


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    report = parse_input(input_file)

    print("--- Part One ---")
    extrapolated_values = []
    for line in report:
        extrapolated_values.append(extrapolate_forwards(line))

    print("Answer:")
    print(sum(extrapolated_values))

    print("--- Part Two ---")
    extrapolated_values = []
    for line in report:
        extrapolated_value = extrapolate_backwards(line)
        # print(extrapolated_value)
        extrapolated_values.append(extrapolated_value)

    print("Answer:")
    print(sum(extrapolated_values))
