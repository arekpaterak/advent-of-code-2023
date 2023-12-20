import os
import sys


day = sys.argv[1]

os.mkdir(f"{day}")

with open("default/default.py", "r") as f:
    default_py = f.read()

with open(f"{day}/{day}.py", "w") as f:
    f.write(default_py)

files = ["example.txt", "input.txt"]
for file in files:
    with open(f"{day}/{file}", "w") as f:
        pass
