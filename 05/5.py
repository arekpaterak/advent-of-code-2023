from __future__ import annotations
from functools import reduce

import sys
from dataclasses import dataclass


INPUTS = ["input.txt", "example.txt"]


@dataclass
class AlmanacMap:
    name: str
    rules: list[tuple[int, int, int]]

    def __call__(self, x: int) -> int:
        for destination_range_start, source_range_start, range_length in self.rules:
            if source_range_start <= x < source_range_start + range_length:
                return destination_range_start + (x - source_range_start)
        else:
            return x

    def inverse(self, x: int) -> int:
        for destination_range_start, source_range_start, range_length in self.rules:
            if destination_range_start <= x < destination_range_start + range_length:
                return source_range_start + (x - destination_range_start)
        else:
            return x


@dataclass
class Almanac:
    seeds: list[int]
    maps: list[AlmanacMap]

    @classmethod
    def from_input(cls, lines: list[str]) -> Almanac:
        seeds = [int(seed) for seed in lines[0].split(" ")[1:]]
        maps = []
        for line in lines[2:]:
            if line:
                if "map" in line:
                    name = line.replace(":", "")
                    rules = []
                elif line[0].isdigit():
                    destination_range_start, source_range_start, range_length = [
                        int(x) for x in line.split(" ")
                    ]

                    rules.append(
                        (
                            destination_range_start,
                            source_range_start,
                            range_length,
                        )
                    )
            else:
                maps.append(AlmanacMap(name, rules))
        else:
            maps.append(AlmanacMap(name, rules))

        return Almanac(seeds, maps)

    def map_all(self, x: int) -> int:
        return reduce(lambda x, map: map(x), self.maps, x)

    def map_all_inverse(self, x: int) -> int:
        return reduce(lambda x, map: map.inverse(x), self.maps[::-1], x)

    def real_seeds_ranges(self):
        for i in range(0, len(self.seeds), 2):
            start, range_length = self.seeds[i], self.seeds[i + 1]
            yield start, start + range_length

    def is_real_seed(self, x: int) -> bool:
        for start, end in self.real_seeds_ranges():
            if start <= x < end:
                return True
        else:
            return False


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    with open(input_file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    almanac = Almanac.from_input(lines)

    print("--- Part One ---")
    print(
        "What is the lowest location number that corresponds to any of the initial seed numbers?"
    )
    location_numbers = []
    for seed in almanac.seeds:
        mapped_number = almanac.map_all(seed)
        location_numbers.append(mapped_number)
    print(min(location_numbers))

    print("--- Part Two ---")
    print(
        "What is the lowest location number that corresponds to any of the initial seed numbers?"
    )

    # an inverse brute force method

    location_number = 0
    while True:
        mapped_number = almanac.map_all_inverse(location_number)

        if almanac.is_real_seed(mapped_number):
            break
        else:
            location_number += 1

    print(location_number)
