We have 4 different function in our code named as defineAvailableColums(), QueensLasVegas(), MixedQueensLasVegas() and DeterministicSolver(). What these functions do can be understood basically by their names.

For the first part, Las Vegas algorithm is applied by QueensLasVegas() function which takes one parameter n (size of table).
For the second part, combination of Las Vegas and deterministic algorithm is applied by MixedQueensLasVegas() function which takes two parameter n (size of table) and k (number of randomly selected columns). Las Vegas part is very similar to first part but it just run over and over if it gives incorrect result and for deterministic part, we wrote DeterministicSolver() function.

To run our code for part1, you can write to console "python3 main.py part1" and then you will see the requested output on console.

To run our code for part2, you can write to console "python3 main.py part2" and then you will see the requested output on console.