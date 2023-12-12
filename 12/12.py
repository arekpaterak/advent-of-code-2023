from __future__ import annotations
from enum import Enum, auto
from functools import cache, reduce, total_ordering
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
        for line in f.readlines():
            springs, damaged_groups_sizes = line.strip().split()
            yield springs, list(map(int, damaged_groups_sizes.split(",")))


# Part One
def get_all_arrangements(springs, start=0):
    arrangements = []
    for i, spring in enumerate(springs):
        if i < start:
            continue
        if spring == "?":
            arrangements += get_all_arrangements(
                springs[:i] + "#" + springs[i + 1 :], i + 1
            )
            arrangements += get_all_arrangements(
                springs[:i] + "." + springs[i + 1 :], i + 1
            )
            break
    else:
        arrangements.append(springs)

    return arrangements


def check_consistency(string_arrangement, criteria):
    arrangement_groups_sizes = []
    in_group = False
    for spring in string_arrangement:
        if spring == "#":
            if in_group:
                arrangement_groups_sizes[-1] += 1
            else:
                in_group = True
                arrangement_groups_sizes.append(1)
        elif spring == ".":
            in_group = False
        else:
            raise Exception(f"Unexpected spring: {spring}")

    return arrangement_groups_sizes == criteria


# Part Two
@cache
def get_number_of_possible_arrangements(springs, groups_sizes, current_group_size=0):
    if len(springs) == 0:
        if len(groups_sizes) == 0 and current_group_size == 0:
            return 1
        elif len(groups_sizes) == 1 and groups_sizes[0] == current_group_size:
            return 1
        else:
            return 0

    match springs[0]:
        case "?":
            return get_number_of_possible_arrangements(
                "#" + springs[1:], groups_sizes, current_group_size
            ) + get_number_of_possible_arrangements(
                "." + springs[1:], groups_sizes, current_group_size
            )
        case "#":
            return get_number_of_possible_arrangements(
                springs[1:], groups_sizes, current_group_size + 1
            )
        case ".":
            if current_group_size > 0:
                if groups_sizes and groups_sizes[0] == current_group_size:
                    return get_number_of_possible_arrangements(
                        springs[1:], groups_sizes[1:], 0
                    )
                else:
                    return 0
            else:
                return get_number_of_possible_arrangements(springs[1:], groups_sizes)
        case _:
            raise Exception(f"Unexpected spring: {springs[0]}")


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    records = list(parse_input(input_file))

    print("--- Part One ---")
    possible_arrangements_count = 0
    # for springs, criteria in records:
    #     all_arrangements = get_all_arrangements(springs)
    #     possible_arrangements = [
    #         arrangement
    #         for arrangement in all_arrangements
    #         if check_consistency(arrangement, criteria)
    #     ]
    #     possible_arrangements_count += len(possible_arrangements)

    for springs, group_sizes in records:
        possible_arrangements_count += get_number_of_possible_arrangements(
            springs, tuple(group_sizes)
        )

    print("Answer:")
    print(possible_arrangements_count)

    print("--- Part Two ---")
    possible_arrangements_count = 0
    for springs, group_sizes in records:
        possible_arrangements_count += get_number_of_possible_arrangements(
            "?".join([springs] * 5), tuple(5 * group_sizes)
        )

    print("Answer:")
    print(possible_arrangements_count)
