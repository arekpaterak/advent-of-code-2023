# Day 12

## The initial idea: 

A combination of all conceivable springs arrangements filtered by consistency with the criteria and the condition records.

## The solution to Part One:

Branching on '?' and checking the consistency of the resulting arrangements afterwards.

## The solution to Part Two:

Sadly, It is not original as it was inspired by posts on Reddit (I looked at one particular solution, thought about it and typed something similar, then combined elements from another to make even more elegant solution).

However, I learned a lot about:
- Dynamic Programming 
- using @cache from functools (don't use lists as arguments for a cached function, use tuples instead)