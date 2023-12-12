from __future__ import annotations

import sys
from dataclasses import dataclass
import numpy as np
import itertools


INPUTS = [
    "input.txt",
    "example.txt",
]


@dataclass
class Universe:
    image: np.ndarray[np.ndarray[str]]
    galaxies: list[Galaxy]

    @classmethod
    def from_input(cls, filename) -> Universe:
        with open(filename) as file:
            image = np.array(
                [np.array(list(line.strip())) for line in file.readlines()]
            )

        universe = cls(image, [])

        universe.galaxies = universe.find_galaxies()

        return universe

    def find_galaxies(self) -> list[Galaxy]:
        galaxies = []
        for x, row in enumerate(self.image):
            for y, cell in enumerate(row):
                if cell == "#":
                    galaxies.append(Galaxy(len(galaxies) + 1, (x, y)))

        return galaxies

    def expand_image(self, rate: int = 2) -> None:
        if rate > 2:
            raise ValueError("Too big expansion rate to handle this way!")

        new_image = self.image.copy()

        x = 0
        for row in self.image:
            if all(cell == "." for cell in row):
                new_image = np.insert(new_image, x, ".", axis=0)
                x += 1

            x += 1

        y = 0
        for column in self.image.T:
            if all(cell == "." for cell in column):
                new_image = np.insert(new_image, y, ".", axis=1)
                y += 1
            y += 1

        self.image = new_image
        self.galaxies = self.find_galaxies()

    def expand_coordinates(self, rate: int) -> np.ndarray[np.ndarray[tuple[int, int]]]:
        coordinates = np.empty_like(self.image, dtype=object)
        for x, row in enumerate(coordinates):
            for y, cell in enumerate(row):
                coordinates[x][y] = (x, y)

        offset = 0
        for x, row in enumerate(self.image):
            for y, cell in enumerate(row):
                _coordinates = coordinates[x][y]
                coordinates[x][y] = (_coordinates[0] + offset, _coordinates[1])

            if all(cell == "." for cell in row):
                offset += rate - 1

        offset = 0
        for y, column in enumerate(self.image.T):
            for x, cell in enumerate(column):
                _coordinates = coordinates[x][y]
                coordinates[x][y] = (_coordinates[0], _coordinates[1] + offset)

            if all(cell == "." for cell in column):
                offset += rate - 1

        return coordinates

    def apply_coordinates_to_galaxies(
        self, coordinates: np.ndarray[np.ndarray[tuple[int, int]]]
    ) -> None:
        for galaxy in self.galaxies:
            galaxy.coordinates = coordinates[galaxy.coordinates]


@dataclass
class Galaxy:
    number: int
    coordinates: tuple[int, int]

    def find_shorthest_path(self, other: Galaxy) -> int:
        def manhattan_distance(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        return manhattan_distance(self.coordinates, other.coordinates)


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    print("--- Part One ---")
    universe = Universe.from_input(input_file)

    universe.expand_image()

    shorthest_paths = []
    for galaxy, other in itertools.combinations(universe.galaxies, 2):
        shorthest_paths.append(galaxy.find_shorthest_path(other))

    print("Answer:")
    print(sum(shorthest_paths))

    print("--- Part Two ---")
    universe = Universe.from_input(input_file)

    expansion_rate = 1_000_000
    new_coordinates = universe.expand_coordinates(expansion_rate)
    universe.apply_coordinates_to_galaxies(new_coordinates)

    shorthest_paths = []
    for galaxy, other in itertools.combinations(universe.galaxies, 2):
        shorthest_paths.append(galaxy.find_shorthest_path(other))

    print("Answer:")
    print(sum(shorthest_paths))
