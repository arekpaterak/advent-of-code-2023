from __future__ import annotations
from functools import reduce
import random

import sys
from dataclasses import dataclass
import math
import numpy as np
import re
import itertools
import sympy


INPUTS = ["input.txt", "example.txt"]


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    times = lines[0].split()[1:]
    times = [int(time) for time in times]

    distances = lines[1].split()[1:]
    distances = [int(distance) for distance in distances]

    return times, distances


def distance(time: int, speed: int) -> int:
    return time * speed


def get_options(time: int) -> list[int]:
    traveled_distances = []
    for time_charging in range(0, time + 1):
        time_left = time - time_charging
        speed = time_charging
        traveled_distance = distance(time_left, speed)
        traveled_distances.append(traveled_distance)

    return traveled_distances


def get_number_of_ways_to_beat_record(time: int, record_distance: int) -> int:
    t = sympy.Symbol("t")
    d = sympy.Symbol("d")
    x = sympy.Symbol("x")
    equation = sympy.Eq(d, (t - x) * x)
    equation = equation.subs(t, time)
    equation = equation.subs(d, record_distance)

    roots = sympy.solve(equation, x)
    return math.ceil(roots[1]) - math.floor(roots[0]) - 1


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    times, record_distances = parse_input(input_file)

    print("--- Part One ---")

    margin_of_error = 1
    for time, record_distance in zip(times, record_distances):
        options = get_options(time)
        number_of_ways_to_beat_record = len(
            list(filter(lambda x: x > record_distance, options))
        )

        margin_of_error *= number_of_ways_to_beat_record

    print("Answer:")
    print(margin_of_error)

    margin_of_error = 1
    for time, record_distance in zip(times, record_distances):
        number_of_ways_to_beat_record = get_number_of_ways_to_beat_record(
            time, record_distance
        )
        margin_of_error *= number_of_ways_to_beat_record
    print("Answer (calculated smartly):")
    print(margin_of_error)

    print("--- Part Two ---")
    real_time = "".join([str(time) for time in times])
    real_time = int(real_time)

    real_record_distance = "".join(
        [str(record_distance) for record_distance in record_distances]
    )
    real_record_distance = int(real_record_distance)

    options = get_options(real_time)
    number_of_ways_to_beat_record = len(
        list(filter(lambda x: x > real_record_distance, options))
    )

    print("Answer:")
    print(number_of_ways_to_beat_record)

    number_of_ways_to_beat_record = get_number_of_ways_to_beat_record(
        real_time, real_record_distance
    )
    print("Answer (calculated smartly):")
    print(number_of_ways_to_beat_record)
