import sys
import re


INPUTS = ["input.txt", "example1.txt", "example2.txt"]


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def solve_part_one(lines):
    calibration_values = []
    for line in lines:
        digits = [int(c) for c in line if c.isdigit()]
        first_digit, last_digit = digits[0], digits[-1]
        calibration_values.append(first_digit * 10 + last_digit)

    print("--- Part One ---\n")
    print(
        f"What is the sum of all of the calibration values?\n{sum(calibration_values)}"
    )


def solve_part_two(lines):
    words2digits = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    calibration_values = []

    for line in lines:
        for word, digit in words2digits.items():
            line = line.replace(word, f"{word}{digit}{word}")

        digits = [int(c) for c in line if c.isdigit()]
        first_digit, last_digit = digits[0], digits[-1]
        calibration_values.append(first_digit * 10 + last_digit)

    print("--- Part Two ---\n")
    print(
        f"What is the sum of all of the calibration values?\n{sum(calibration_values)}"
    )


if __name__ == "__main__":
    part = sys.argv[1]
    input_file_index = sys.argv[2]
    input_file = INPUTS[int(input_file_index)]

    lines = parse_input(input_file)

    match part:
        case "1":
            solve_part_one(lines)
        case "2":
            solve_part_two(lines)
        case _:
            print("Invalid value as a part of the problem to solve.")
