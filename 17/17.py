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


# def parse_input(input_file):
#     with open(input_file, "r") as f:
#         lines = f.readlines()
#     lines = [line.strip() for line in lines]
#     grid = np.array([[int(heat_loss) for heat_loss in line] for line in lines])
#     return grid


class CityBlock:
    def __init__(self, coordinates, heat_loss):
        self.coordinates = coordinates
        self.heat_loss = heat_loss
        self.neighbours = []

    def __repr__(self):
        return f"CityBlock({self.coordinates}, {self.heat_loss})"


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Map:
    graph: dict[tuple[int, int], CityBlock]

    @classmethod
    def from_input(cls, input_file):
        with open(input_file, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        grid = np.array([[int(heat_loss) for heat_loss in line] for line in lines])

        graph = {}
        for x, y in np.ndindex(grid.shape):
            graph[(x, y)] = CityBlock((x, y), grid[x, y])

        for x, y in np.ndindex(grid.shape):
            if x > 0:
                graph[(x, y)].neighbours.append(graph[(x - 1, y)])
            if x < grid.shape[0] - 1:
                graph[(x, y)].neighbours.append(graph[(x + 1, y)])
            if y > 0:
                graph[(x, y)].neighbours.append(graph[(x, y - 1)])
            if y < grid.shape[1] - 1:
                graph[(x, y)].neighbours.append(graph[(x, y + 1)])

        return cls(graph)


def find_best_path_with_modified_dijkstra(
    graph: dict[tuple[int, int], CityBlock],
    start: tuple[int, int],
    end: tuple[int, int],
):
    cumulative_heat_loss = {city_block: math.inf for city_block in graph.values()}
    previous = {city_block: None for city_block in graph.values()}
    queue = list(graph.values())
    cumulative_heat_loss[graph[start]] = 0

    while queue:
        current = min(queue, key=lambda block: cumulative_heat_loss[block])
        queue.remove(current)

        # if current.coordinates == end:
        #     break

        three_previous = []
        current_previous = previous[current]
        while current_previous is not None:
            three_previous.append(current_previous)
            current_previous = previous[current_previous]
            if len(three_previous) == 3:
                break

        for neighbour in current.neighbours:
            if neighbour not in queue:
                continue

            if neighbour is previous[current]:
                continue

            if len(three_previous) == 3:
                if all(
                    block.coordinates[0] == neighbour.coordinates[0]
                    for block in [current] + three_previous
                ):
                    continue
                if all(
                    block.coordinates[1] == neighbour.coordinates[1]
                    for block in [current] + three_previous
                ):
                    continue

            alt = cumulative_heat_loss[current] + neighbour.heat_loss
            if alt < cumulative_heat_loss[neighbour]:
                cumulative_heat_loss[neighbour] = alt
                previous[neighbour] = current

    return cumulative_heat_loss, previous


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    map = Map.from_input(input_file)

    print("--- Part One ---")

    print("Answer:")
    hl, p = find_best_path_with_modified_dijkstra(map.graph, (0, 0), (12, 12))

    previous = p[map.graph[(12, 12)]]
    while previous is not None:
        print(previous.coordinates)
        previous = p[previous]

    print(hl[map.graph[(12, 12)]])

    print("--- Part Two ---")
    print("Answer:")
