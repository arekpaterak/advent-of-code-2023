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


INPUTS = ["input.txt", "example.txt"]


if __name__ == "__main__":
    input_file_index = sys.argv[1]
    input_file = INPUTS[int(input_file_index)]
