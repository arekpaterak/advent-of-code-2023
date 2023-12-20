from __future__ import annotations

import sys
from dataclasses import dataclass
import matplotlib.pyplot as plt

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


INPUTS = [
    "input.txt",
    "example.txt",
]


@dataclass
class Lagoon:
    dig_plan: list[tuple[str, int, str]]
    limited_boundary_points: list[Point]
    boundary_points_number: int
    polygon: Polygon

    @classmethod
    def from_input(cls, input_file: str) -> Lagoon:
        dig_plan = []

        with open(input_file, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        for line in lines:
            direction, meters, colour = line.split()
            dig_plan.append((direction, int(meters), colour.strip("(#)")))

        return cls.from_dig_plan(dig_plan)

    @classmethod
    def from_dig_plan(cls, dig_plan: list[tuple[str, int, str]]) -> Lagoon:
        point = Point(0, 0)
        limited_boundary_points = [point]
        boundary_points_number = 0
        for _, _, colour in dig_plan:
            encoded_distance = colour[:5]
            match int(colour[-1]):
                case 0:
                    direction = "R"
                case 1:
                    direction = "D"
                case 2:
                    direction = "L"
                case 3:
                    direction = "U"
                case _:
                    raise ValueError(f"Invalid direction value: {colour[-1]}")
            meters = int(encoded_distance, 16)

            boundary_points_number += meters
            match direction:
                case "U":
                    point = Point(point.x, point.y + meters)
                case "R":
                    point = Point(point.x + meters, point.y)
                case "D":
                    point = Point(point.x, point.y - meters)
                case "L":
                    point = Point(point.x - meters, point.y)
            limited_boundary_points.append(point)

        polygon = Polygon([[point.x, point.y] for point in limited_boundary_points])

        return cls(dig_plan, limited_boundary_points, boundary_points_number, polygon)

    @property
    def cubic_meters(self) -> int:
        # using Pick's theorem
        return int(self.polygon.area + 1 + self.boundary_points_number / 2)

    def visualise(self) -> None:
        x, y = self.polygon.exterior.xy
        plt.scatter(x, y, marker="s")
        plt.show()


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    lagoon = Lagoon.from_input(input_file)

    print("--- Part Two ---")
    print("Answer:")
    print(lagoon.cubic_meters)
