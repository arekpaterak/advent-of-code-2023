import sys
from dataclasses import dataclass
import math
import numpy as np
import re


INPUTS = ["input.txt", "example.txt"]


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    for line in lines:
        _, line = line.split(":")

        line = line.strip()
        winning_numbers, own_numbers = line.split("|")
        winning_numbers = re.sub(" +", " ", winning_numbers).strip().split(" ")
        own_numbers = re.sub(" +", " ", own_numbers).strip().split(" ")

        winning_numbers = [int(number) for number in winning_numbers]
        own_numbers = [int(number) for number in own_numbers]

        yield winning_numbers, own_numbers


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    cards = list(parse_input(input_file))
    cards2matches = {i: 0 for i, _ in enumerate(cards, 1)}
    cards_counter = {i: 1 for i, _ in enumerate(cards, 1)}

    points = 0

    for i, card in enumerate(cards, 1):
        winning_numbers, own_numbers = card
        matches = 0
        for number in own_numbers:
            if number in winning_numbers:
                matches += 1

        if matches:
            points += 2 ** (matches - 1)
            cards2matches[i] = matches

    print("--- Part One ---")
    print("How many points are the cards worth in total?")
    print(points)

    print("--- Part Two ---")
    print("How many total scratchcards do you end up with?")

    for i, (card, matches) in enumerate(cards2matches.items(), 1):
        for j in range(i + 1, i + matches + 1):
            cards_counter[j] += 1 * cards_counter[i]

    print(sum(cards_counter.values()))
