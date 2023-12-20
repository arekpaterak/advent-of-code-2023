from __future__ import annotations
from enum import Enum, auto
from functools import reduce, total_ordering
import random

import sys
from dataclasses import dataclass
import math
from time import sleep
import numpy as np
import re
import itertools
import sympy


INPUTS = [
    "input.txt",
    "example.txt",
]


class Direction:
    def __init__(self, vertical: int, horizontal: int):
        if vertical == 0 or horizontal == 0:
            self.vertical = vertical
            self.horizontal = horizontal
        else:
            raise ValueError("Direction must be either vertical or horizontal.")

    @classmethod
    def from_string(cls, string: str) -> Direction:
        if string == "up":
            return cls(-1, 0)
        elif string == "down":
            return cls(1, 0)
        elif string == "left":
            return cls(0, -1)
        elif string == "right":
            return cls(0, 1)
        else:
            raise ValueError(f"Invalid direction string: {string}")

    def reflect(self, mirror: str) -> Direction:
        match mirror:
            case "/":
                if self.vertical == 0:
                    # (0, 1) -> (-1, 0)
                    # (0, -1) -> (1, 0)
                    return Direction(-self.horizontal, 0)
                else:
                    # (1, 0) -> (0, -1)
                    # (-1, 0) -> (0, 1)
                    return Direction(0, -self.vertical)
            case "\\":
                if self.vertical == 0:
                    # (0, 1) -> (1, 0)
                    # (0, -1) -> (-1, 0)
                    return Direction(self.horizontal, 0)
                else:
                    # (1, 0) -> (0, 1)
                    # (-1, 0) -> (0, -1)
                    return Direction(0, self.vertical)
            case _:
                raise ValueError(f"Invalid mirror: {mirror}")

    def split(self) -> tuple[Direction, Direction]:
        if self.vertical == 0:
            return (Direction(-1, 0), Direction(1, 0))
        else:
            return (Direction(0, -1), Direction(0, 1))

    def __iter__(self):
        yield self.vertical
        yield self.horizontal

    def __hash__(self) -> int:
        return hash((self.vertical, self.horizontal))

    def __eq__(self, other):
        return self.vertical == other.vertical and self.horizontal == other.horizontal


@dataclass
class Contraption:
    grid: np.ndarray
    energized_grid: np.ndarray

    @classmethod
    def from_input(cls, input_file) -> Contraption:
        with open(input_file, "r") as f:
            lines = f.readlines()
        grid = np.array([list(line.strip()) for line in lines])
        energized_grid = np.full_like(grid, ".")
        return cls(grid, energized_grid)

    def beam(self, position: tuple[int, int], direction: Direction):
        self.reset()

        todo: set[tuple[tuple[int, int], Direction]] = set([(position, direction)])
        done: set[tuple[tuple[int, int], Direction]] = set()

        while todo:
            position, direction = todo.pop()
            i, j = position

            if i < 0 or j < 0 or i >= self.grid.shape[0] or j >= self.grid.shape[1]:
                continue

            self.energized_grid[i, j] = "#"

            if (position, direction) in done:
                continue

            done.add((position, direction))

            tile = self.grid[i, j]
            match tile:
                case "/" | "\\":
                    direction = direction.reflect(tile)
                    di, dj = direction
                    todo.add(((i + di, j + dj), direction))
                case "|" if direction.vertical == 0:
                    directions = direction.split()
                    for direction in directions:
                        di, dj = direction
                        todo.add(((i + di, j + dj), direction))
                case "-" if direction.horizontal == 0:
                    directions = direction.split()
                    for direction in directions:
                        di, dj = direction
                        todo.add(((i + di, j + dj), direction))
                case _:
                    di, dj = direction
                    todo.add(((i + di, j + dj), direction))

    def reset(self):
        self.energized_grid[:, :] = "."


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    print("--- Part One ---")
    contraption = Contraption.from_input(input_file)
    contraption.beam((0, 0), Direction.from_string("right"))

    print("Answer:")
    print(np.count_nonzero(contraption.energized_grid == "#"))

    print("--- Part Two ---")
    contraption = Contraption.from_input(input_file)

    energized_tiles_per_configuration = set()
    for i in range(contraption.grid.shape[0]):
        for direction, j in zip(["right", "left"], [0, contraption.grid.shape[1] - 1]):
            contraption.beam((i, j), Direction.from_string(direction))
            energized_tiles = np.count_nonzero(contraption.energized_grid == "#")
            energized_tiles_per_configuration.add(energized_tiles)

    for j in range(contraption.grid.shape[1]):
        for direction, i in zip(["down", "up"], [0, contraption.grid.shape[0] - 1]):
            contraption.beam((i, j), Direction.from_string(direction))
            energized_tiles = np.count_nonzero(contraption.energized_grid == "#")
            energized_tiles_per_configuration.add(energized_tiles)

    print("Answer:")
    print(max(energized_tiles_per_configuration))
