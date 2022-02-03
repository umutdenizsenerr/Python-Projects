import random
import sys


def defineAvailableColumns(n, chessBoard, Row, AllColumns):
    AvailableColumns = []
    for c in AllColumns:
        leftCross = True
        j = c
        i = Row
        while i >= 0 and j >= 0:
            if chessBoard[i][j]:
                leftCross = False
            i -= 1
            j -= 1
        if not leftCross:
            continue
        rightCross = True
        i = Row
        j = c
        while i >= 0 and j < n:
            if chessBoard[i][j]:
                rightCross = False
            i = i - 1
            j = j + 1
        if not rightCross:
            continue
        AvailableColumns.append(c)
    return AvailableColumns


def QueensLasVegas(n):
    chessBoard = [[0 for j in range(n)] for i in range(n)]
    AllColumns = list(range(0, n))
    AvailableColumns = list(range(0, n))
    Column = [None] * n
    R = 0
    while AllColumns:
        if len(AvailableColumns) == 0:
            return False
        C = random.choice(AvailableColumns)
        Column[R] = C
        chessBoard[R][C] = 1
        AllColumns.remove(C)
        R += 1
        AvailableColumns = defineAvailableColumns(n, chessBoard, R, AllColumns)
    return True

def MixedQueensLasVegas(n, k):
    chessBoard = [[0 for j in range(n)] for i in range(n)]
    AllColumns = list(range(0, n))
    AvailableColumns = list(range(0, n))
    Column = [None] * n
    R = 0
    while AllColumns and R <= k - 1:
        if len(AvailableColumns) == 0:
            return MixedQueensLasVegas(n, k)
        C = random.choice(AvailableColumns)
        Column[R] = C
        chessBoard[R][C] = 1
        AllColumns.remove(C)
        R += 1
        AvailableColumns = defineAvailableColumns(n, chessBoard, R, AllColumns)
    return DeterministicSolver(chessBoard, k, n, AllColumns)


def DeterministicSolver(chessBoard, row, N, AllColumns):
    AvailableColumns = defineAvailableColumns(N, chessBoard, row, AllColumns)
    if row >= N:
        return True
    for column in AvailableColumns:
        chessBoard[row][column] = 1
        AllColumns.remove(column)
        if DeterministicSolver(chessBoard, row + 1, N, AllColumns):
            return True
        chessBoard[row][column] = 0
        AllColumns.append(column)
    return False


n_list = [6, 8, 10]
part = sys.argv[1]
if part == "part1":
    for n in n_list:
        successfulTrial = 0
        for m in range(10000):
            successfulTrial += QueensLasVegas(n) 

        print("Las Vegas Algorithm With n =", n)
        print("Number of successful placements is", successfulTrial)
        print("Number of trials is 10000")
        print("Probability that it will come to solution is", successfulTrial / 10000)
        print()
else:
    for n in n_list:
        print("---------------", n, "---------------")
        for k in range(n):
            i = 0
            for a in range(10000):
                if MixedQueensLasVegas(n, k):
                    i += 1
            print("k is", k)
            print("Number of successful placements is", i)
            print("Number of trials is 10000")
            print("Probability that it will come to a solution is", (i / 10000))

