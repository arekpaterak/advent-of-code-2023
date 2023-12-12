from __future__ import annotations

import sys
import numpy as np


INPUTS = [
    "input.txt",
    "example1.txt",
    "example2_1.txt",
]


def parse_input(input_file: str) -> np.ndarray:
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    return np.array([np.array(list(line)) for line in lines])


pipes_to_directions: dict[str, str] = {
    "|": "NS",
    "-": "WE",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
}


def get_next_pipe_with_direction(
    grid: np.ndarray, x: int, y: int, last_direction: str
) -> tuple[tuple[int, int], str]:
    def get_direction(pipe: str, last_direction: str) -> str:
        if pipe == "S":
            return last_direction
        else:
            return pipes_to_directions[pipe].replace(
                opposite_direction(last_direction), ""
            )

    pipe = grid[x, y]
    direction = get_direction(pipe, last_direction)

    match direction:
        case "N":
            return (x - 1, y), direction
        case "S":
            return (x + 1, y), direction
        case "E":
            return (x, y + 1), direction
        case "W":
            return (x, y - 1), direction


def is_pipe(grid: np.ndarray, x: int, y: int) -> bool:
    return not grid[x, y] == "."


def find_start(grid: np.ndarray) -> tuple[int, int]:
    indexes = np.where(grid == "S")
    return indexes[0][0], indexes[1][0]


def substitute_start(grid: np.ndarray, start_directions: str) -> np.ndarray:
    grid = grid.copy()

    x, y = find_start(grid)

    for symbol, directions in pipes_to_directions.items():
        if set(directions) == set(start_directions):
            grid[x, y] = symbol
            break

    return grid


def opposite_direction(direction: str) -> str:
    match direction:
        case "N":
            return "S"
        case "S":
            return "N"
        case "E":
            return "W"
        case "W":
            return "E"


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    grid = parse_input(input_file)

    print("--- Part One ---")
    start_tile = find_start(grid)

    loop = []
    for direction in ["N", "E", "S", "W"]:
        next_tile = get_next_pipe_with_direction(grid, *start_tile, direction)
        if is_pipe(grid, *next_tile[0]):
            loop.append(next_tile[0])
            break

    start_direction = direction

    while grid[next_tile[0]] != "S":
        (x, y), direction = next_tile
        next_tile = get_next_pipe_with_direction(grid, x, y, direction)
        loop.append(next_tile[0])

    print("Answer:")
    print(len(loop[:-1]) // 2 + 1)

    end_direction = opposite_direction(direction)

    print("--- Part Two ---")

    cleaned_grid = np.full_like(grid, ".")
    for x, y in loop:
        cleaned_grid[x, y] = grid[x, y]
    cleaned_grid = substitute_start(cleaned_grid, start_direction + end_direction)

    inside = 0
    for row in cleaned_grid:
        stack = []
        parity = True
        for pipe in row:
            match pipe:
                case ".":
                    if not parity:
                        inside += 1
                case "|":
                    last_element = stack[-1] if stack else None
                    if not last_element == "|":
                        stack.append("|")
                        parity = not parity
                    else:
                        stack.pop()
                        parity = not parity
                case "-":
                    continue
                case "L":
                    stack.append("L")
                case "F":
                    stack.append("F")
                case "J":
                    last_element = stack[-1] if stack else None
                    if last_element == "L":
                        stack.pop()
                    elif last_element == "F":
                        stack.pop()
                        parity = not parity
                case "7":
                    last_element = stack[-1] if stack else None
                    if last_element == "F":
                        stack.pop()
                    elif last_element == "L":
                        stack.pop()
                        parity = not parity
                case _:
                    raise Exception("Unknown tile")

    print("Answer:")
    print(inside)
