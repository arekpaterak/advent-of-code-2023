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


@dataclass
class Platform:
    grid: np.ndarray

    @classmethod
    def from_input(cls, input_file) -> Platform:
        with open(input_file) as f:
            lines = f.readlines()
            grid = np.array([list(line.strip()) for line in lines])
        return cls(grid)

    def cycle(self) -> None:
        for _ in range(4):
            self.tilt_north()
            self.rotate_right()

    def rotate_right(self) -> None:
        self.grid = np.rot90(self.grid, -1)

    def tilt_north(self) -> None:
        for col in range(self.grid.shape[1]):
            for row in range(1, self.grid.shape[0]):
                if self.grid[row, col] == "O":
                    while self.grid[row - 1, col] == "." and row > 0:
                        self.grid[row, col] = "."
                        self.grid[row - 1, col] = "O"

                        row -= 1

    def total_load(self) -> int:
        # total_load = 0
        # for i, row in enumerate(self.grid):
        #     load = self.grid.shape[0] - i
        #     rounded_rocks_count = np.count_nonzero(row == "O")
        #     total_load += rounded_rocks_count * load

        load = np.arange(self.grid.shape[0], 0, -1)
        rounded_rocks_count = np.count_nonzero(self.grid == "O", axis=1)
        total_load = np.sum(rounded_rocks_count * load)
        return total_load


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    platform = Platform.from_input(input_file)

    print("--- Part One ---")
    platform.tilt_north()

    print("Answer:")
    print(platform.total_load())

    print("--- Part Two ---")
    platform = Platform.from_input(input_file)

    encountered_grid_states = {}
    i = 0
    while i < 10**9:
        i += 1
        platform.cycle()
        grid_representation = platform.grid.tobytes()

        if grid_representation in encountered_grid_states:
            loop_length = i - encountered_grid_states[grid_representation]
            i += ((10**9 - i) // loop_length) * loop_length
        encountered_grid_states[grid_representation] = i

    print("Answer:")
    print(platform.total_load())
