import sys
from dataclasses import dataclass
import math


INPUTS = ["input.txt", "example.txt"]


def parse_input_lines(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def parse_lines_to_games(lines):
    games = []
    for i, line in enumerate(lines):
        game = Game(i + 1)

        _, line = line.split(":")
        line = line.strip()

        subsets = [subset.strip() for subset in line.split(";")]
        for subset in subsets:
            red, blue, green = 0, 0, 0
            cubes = [cube.strip() for cube in subset.split(",")]
            for cube in cubes:
                number, colour = cube.split(" ")
                number = int(number)
                if colour == "red":
                    red = number
                elif colour == "blue":
                    blue = number
                elif colour == "green":
                    green = number

            game.subsets.append(CubeSet(red, blue, green))

        games.append(game)
    return games


@dataclass
class CubeSet:
    red: int
    blue: int
    green: int

    @property
    def power(self) -> int:
        return math.prod([self.red, self.blue, self.green])


class Game:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.subsets: list[CubeSet] = []

    def is_possible(self, bag: CubeSet) -> bool:
        for subset in self.subsets:
            if (
                subset.red > bag.red
                or subset.blue > bag.blue
                or subset.green > bag.green
            ):
                return False
        return True

    def minimal_bag(self) -> CubeSet:
        red = max([subset.red for subset in self.subsets])
        blue = max([subset.blue for subset in self.subsets])
        green = max([subset.green for subset in self.subsets])
        return CubeSet(red, blue, green)


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]

    lines = parse_input_lines(input_file)

    games = parse_lines_to_games(lines)

    print("--- Part One ---\n")
    bag = CubeSet(12, 13, 14)
    possible_games = [game for game in games if game.is_possible(bag)]
    print(
        f"What is the sum of the IDs of the possible games?\n{sum([game.id for game in possible_games])}"
    )

    print("\n--- Part Two ---\n")
    minimal_bags = [game.minimal_bag() for game in games]
    print(
        f"What is the sum of the power of the minimum set of cubes that must have been present for each game?\n{sum([bag.power for bag in minimal_bags])}"
    )
