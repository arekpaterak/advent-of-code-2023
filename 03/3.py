import sys
import math
import numpy as np


INPUTS = ["input.txt", "example.txt"]


def parse_input(input_file) -> np.ndarray:
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    array = np.array([np.array(list(line)) for line in lines])
    return array


def pad_array(array: np.ndarray, symbol: str) -> np.ndarray:
    padded_array = np.zeros((array.shape[0] + 2, array.shape[1] + 2), dtype=str)
    padded_array[1:-1, 1:-1] = array
    padded_array[0, :] = symbol
    padded_array[-1, :] = symbol
    padded_array[:, 0] = symbol
    padded_array[:, -1] = symbol
    return padded_array


def is_symbol(character: str) -> bool:
    return not character.isdigit() and character != "."


def adjacent_symbols(array: np.ndarray, i: int, j: int) -> list:
    adjacent_symbols = []
    for i_offset in [-1, 0, 1]:
        for j_offset in [-1, 0, 1]:
            if i_offset == 0 and j_offset == 0:
                continue
            adjacent_character = array[i + i_offset, j + j_offset]
            if is_symbol(adjacent_character):
                adjacent_symbols.append(adjacent_character)
    return adjacent_symbols


def find_adjacent_numbers(array: np.ndarray, i: int, j: int) -> list:
    adjacent_numbers = []
    checked = set()
    for i_offset in [-1, 0, 1]:
        for j_offset in [-1, 0, 1]:
            if i_offset == 0 and j_offset == 0:
                continue
            adjacent_character = array[i + i_offset, j + j_offset]
            if (
                adjacent_character.isdigit()
                and (i + i_offset, j + j_offset) not in checked
            ):
                number, checked = find_whole_number(
                    array, i + i_offset, j + j_offset, checked
                )
                adjacent_numbers.append(number)
                checked.add((i + i_offset, j + j_offset))
    return adjacent_numbers


def find_whole_number(
    array: np.ndarray, i: int, j: int, checked: set[tuple[int, int]]
) -> int:
    number_str = ""
    for j_left in range(j, -1, -1):
        character = array[i, j_left]
        if character.isdigit():
            number_str = character + number_str
            checked.add((i, j_left))
        else:
            break
    for j_right in range(j + 1, array.shape[1]):
        character = array[i, j_right]
        if character.isdigit():
            number_str += character
            checked.add((i, j_right))
        else:
            break
    return int(number_str), checked


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    engine_schematic = parse_input(input_file)

    engine_schematic = pad_array(engine_schematic, symbol=".")

    print("--- Part One ---\n")

    part_numbers = []
    for i in range(engine_schematic.shape[0]):
        start_of_number = None
        end_of_number = None
        number_str = ""
        adjacent_symbol = False
        for j in range(engine_schematic.shape[1]):
            character = engine_schematic[i, j]
            if character.isdigit():
                number_str += character
                if start_of_number is None:
                    start_of_number = j
                end_of_number = j
                if adjacent_symbols(engine_schematic, i, j):
                    adjacent_symbol = True
            else:
                if start_of_number is not None:
                    if adjacent_symbol:
                        part_numbers.append(int(number_str))
                    start_of_number = None
                    end_of_number = None
                    number_str = ""
                    adjacent_symbol = False

    print("What is the sum of all of the part numbers in the engine schematic?")
    print(sum(part_numbers))

    print("\n--- Part Two ---\n")
    GEAR_SYMBOL = "*"
    gears = []
    for i in range(engine_schematic.shape[0]):
        for j in range(engine_schematic.shape[1]):
            character = engine_schematic[i, j]
            if character == GEAR_SYMBOL:
                adjacent_numbers = find_adjacent_numbers(engine_schematic, i, j)
                if len(adjacent_numbers) == 2:
                    print(adjacent_numbers)
                    gears.append(adjacent_numbers)

    print("What is the sum of all of the gear ratios in your engine schematic?")
    gear_ratios = [math.prod(gear) for gear in gears]
    print(sum(gear_ratios))
