# Authors: Leyla Yayladere - Umut Deniz Sener
# Student ids: 2018400216 - 2018400225
# Compiling
# Working
# We assume that N is always divisible by number of processor - 1
# can run with mpiexec -n [Number of Processors] python3 simulator.py [input file name] [output file name]
import sys
from mpi4py import MPI


# arrange the attacks of the "o" towers to "+" towers in upper/bottom rows according to their attack power and pattern
# returns an array that contains the damages in each column corresponding defender row
# example:
# Attacker = ["o", ".", ".", "+"] Defender = [".", "+", ".","o"]
# Damages = [0, -1, 0, 0]
def DifferentLineAttack_o(Attacker, Defender):
    Damages = [0] * len(Attacker)
    if len(Defender) == 0:
        return Damages
    for i in range(len(Attacker)):
        if Attacker[i] == "o":
            if Defender[i] == "+":
                Damages[i] -= 1
            if i != 0:
                if Defender[i - 1] == "+":
                    Damages[i - 1] -= 1
            if i != len(Attacker) - 1:
                if Defender[i + 1] == "+":
                    Damages[i + 1] -= 1
    return Damages


# arrange the attacks of the "+" towers to "o" towers in upper/bottom rows according to their attack power and pattern
# returns an array that contains the damages in each column corresponding defender row
# example:
# Attacker = ["o", ".", ".", "+"] Defender = [".", "+", ".","o"]
# Damages = [0, 0, 0, -2]
def DifferentLineAttack_x(Attacker, Defender):
    Damages = [0] * len(Attacker)
    if len(Defender) == 0:
        return Damages
    for i in range(len(Attacker)):
        if Attacker[i] == "+":
            if Defender[i] == "o":
                Damages[i] -= 2
    return Damages


# arrange the attacks of the "o" towers to "+" towers in same row according to their attack power and pattern
# returns an array that contains the damages in each column corresponding defender row
# example:
# Attacker = ["+", "o", "+", "o"]
# Damages = [-1, 0, -2, 0]
def SameLineAttack_o(Attacker):
    Damages = [0] * len(Attacker)
    for i in range(len(Attacker)):
        if Attacker[i] == "o":
            if i != 0:
                if Attacker[i - 1] == "+":
                    Damages[i - 1] -= 1
            if i != len(Attacker) - 1:
                if Attacker[i + 1] == "+":
                    Damages[i + 1] -= 1
    return Damages


# arrange the attacks of the "+" towers to "o" towers in same row according to their attack power and pattern
# returns an array that contains the damages in each column corresponding defender row
# example:
# Attacker = ["+", "o", "+", "o"]
# Damages = [0, -4, 0, -2]
def SameLineAttack_x(Attacker):
    Damages = [0] * len(Attacker)
    for i in range(len(Attacker)):
        if Attacker[i] == "+":
            if i != 0:
                if Attacker[i - 1] == "o":
                    Damages[i - 1] -= 2
            if i != len(Attacker) - 1:
                if Attacker[i + 1] == "o":
                    Damages[i + 1] -= 2
    return Damages


# update the health map of towers according to damage taken
# example:
# CurrentHealths = [[3, 4], [3, 1]] Damages = [[-2, -1], [-4, -2]]
# UpdatedHealths = [[1, 3], [-1, -1]]
def HealthUpdater(CurrentHealths, Damages):
    UpdatedHealths = [0] * len(CurrentHealths)
    if len(Damages) == 0:
        return CurrentHealths
    for i in range(len(CurrentHealths)):
        UpdatedHealths[i] = int(CurrentHealths[i]) + Damages[i]
    return UpdatedHealths


# destroy the towers if their health smaller than or equal to 0
# example:
# CurrentData = [["o", "."], ["+", "o"]] CurrentHealths = [[2, 0], [-2, -4]]
# CurrentData(which is returned) = [["o", "."], [".", "."]]
def Destroyer(CurrentData, CurrentHealths):
    for i in range(len(CurrentHealths)):
        for j in range(len(CurrentHealths[0])):
            if CurrentHealths[i][j] <= 0:
                CurrentData[i][j] = "."
    return CurrentData

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
p = size - 1

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], "w")

input_lines = infile.readlines()
firstLine = input_lines[0].split()
N = int(firstLine[0])
Wave = int(firstLine[1])
Tower = int(firstLine[2])
input_lines.pop(0)

BattleField = [[["." for k in range(N)] for j in range(N)] for i in range(1)] + [
    [["0" for k in range(N)] for j in range(N)] for i in range(1)]

for w in range(Wave):

    if rank == 0:  # Manager Process
        index = 0
        for j in range(2):
            coordinates = input_lines[j + (2 * w)].split(", ")

            #  initialize the location map and health map for the towers as 3D array
            for i in range(Tower):
                x_y = coordinates[0 + i].split(" ")
                if index % 2 == 0:
                    if BattleField[0][int(x_y[0])][int(x_y[1])] == ".":
                        BattleField[0][int(x_y[0])][int(x_y[1])] = 'o'
                        BattleField[1][int(x_y[0])][int(x_y[1])] = 6
                else:
                    if BattleField[0][int(x_y[0])][int(x_y[1])] == ".":
                        BattleField[0][int(x_y[0])][int(x_y[1])] = '+'
                        BattleField[1][int(x_y[0])][int(x_y[1])] = 8
            index += 1

        #  distribute the data to each worker process accordingly their rank and the total number of processors
        #  in the beginning of each wave
        for p_num in range(p):
            comm.send(BattleField[1][p_num * (N // p):(p_num + 1) * (N // p)], dest=p_num + 1, tag=5)
            comm.send(BattleField[0][p_num * (N // p):(p_num + 1) * (N // p)], dest=p_num + 1, tag=10)

        #  collect the data from each worker process accordingly their rank and the total number of processors
        #  at the end of each wave
        for p_num in range(p):
            BattleField[1][p_num * (N // p):(p_num + 1) * (N // p)] = comm.recv(source=p_num + 1, tag=23)
            BattleField[0][p_num * (N // p):(p_num + 1) * (N // p)] = comm.recv(source=p_num + 1, tag=22)

        # write the output at the end of the last wave
        if w == Wave - 1:
            for U in range(N):
                for L in range(N):
                    outfile.write(BattleField[0][U][L])
                    outfile.write(" ")
                outfile.write("\n")
            infile.close()
            outfile.close()

    else:  # Worker Processes
        if rank % 2 == 0:  # Worker Processes with even rank

            healths = comm.recv(source=0, tag=5)  # receive a group of N//p adjacent rows of health map of the towers
            data = comm.recv(source=0, tag=10)  # receive a group of N//p adjacent rows of location map of the towers

            # initialize necessary arrays
            UpperLine = ["."] * N
            BottomLine = ["."] * N
            SameLineDamageTaken = [0] * (N // p)
            UpperDamageTaken = [0] * (N // p)
            BottomDamageTaken = [0] * (N // p)
            
            # simulate the game for 8 rounds in each wave
            for round in range(8):
                
                # Communication Part of Two Adjacent Processors
                
                if rank != p:  # send the corresponding cells of location map of the towers to the bottom neighbour
                    comm.send(data[len(data) - 1], dest=rank + 1, tag=11)
                if rank != 1:  # send the corresponding cells of location map of the towers to the upper neighbour
                    comm.send(data[0], dest=rank - 1, tag=12)
                    
                if rank != 1:  # receive the corresponding cells of location map of the towers from the upper neighbour
                    UpperLine = comm.recv(source=rank - 1, tag=13)
                if rank != p:  # receive the corresponding cells of location map of the towers from the bottom neighbour
                    BottomLine = comm.recv(source=rank + 1, tag=14)

                for i in range(N // p):  # let the war begin :) 
                    SameLineDamageTaken[i] = HealthUpdater(SameLineAttack_x(data[i]), SameLineAttack_o(data[i]))
                    if i == 0:
                        UpperDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(UpperLine, data[i]),
                                                            DifferentLineAttack_o(UpperLine, data[i]))
                    else:
                        UpperDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(data[i - 1], data[i]),
                                                            DifferentLineAttack_o(data[i - 1], data[i]))
                    if i == N // p - 1:
                        BottomDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(BottomLine, data[i]),
                                                             DifferentLineAttack_o(BottomLine, data[i]))
                    else:
                        BottomDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(data[i + 1], data[i]),
                                                             DifferentLineAttack_o(data[i + 1], data[i]))

                    healths[i] = HealthUpdater(healths[i], SameLineDamageTaken[i])

                    healths[i] = HealthUpdater(healths[i], UpperDamageTaken[i])

                    healths[i] = HealthUpdater(healths[i], BottomDamageTaken[i])

                data = Destroyer(data, healths)

            # send the corresponding cells of updated location map of the towers to the manager process after each wave
            comm.send(data, dest=0, tag=22)
            # send the corresponding cells of updated health map of the towers to the manager process after each wave
            comm.send(healths, dest=0, tag=23)

        else:  # Worker Processes with odd rank

            healths = comm.recv(source=0, tag=5)  # receive a group of N//p adjacent rows of health map of the towers
            data = comm.recv(source=0, tag=10)  # receive a group of N//p adjacent rows of location map of the towers

            # initialize necessary arrays
            UpperLine = ["."] * N
            BottomLine = ["."] * N
            SameLineDamageTaken = [0] * (N // p)
            UpperDamageTaken = [0] * (N // p)
            BottomDamageTaken = [0] * (N // p)

            # simulate the game for 8 rounds in each wave
            for round in range(8):

                # Communication Part of Two Adjacent Processors

                if rank != 1:  # receive the corresponding cells of location map of the towers from the upper neighbour
                    UpperLine = comm.recv(source=rank - 1, tag=11)
                if rank != p:  # receive the corresponding cells of location map of the towers from the bottom neighbour
                    BottomLine = comm.recv(source=rank + 1, tag=12)
                    
                if rank != p:  # send the corresponding cells of location map of the towers to the bottom neighbour
                    comm.send(data[len(data) - 1], dest=rank + 1, tag=13)
                if rank != 1:  # send the corresponding cells of location map of the towers to the upper neighbour
                    comm.send(data[0], dest=rank - 1, tag=14)

                for i in range(N // p):  # let the war begin :) 
                    SameLineDamageTaken[i] = HealthUpdater(SameLineAttack_x(data[i]), SameLineAttack_o(data[i]))
                    if i == 0:
                        UpperDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(UpperLine, data[i]),
                                                            DifferentLineAttack_o(UpperLine, data[i]))
                    else:
                        UpperDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(data[i - 1], data[i]),
                                                            DifferentLineAttack_o(data[i - 1], data[i]))
                    if i == N // p - 1:
                        BottomDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(BottomLine, data[i]),
                                                             DifferentLineAttack_o(BottomLine, data[i]))
                    else:
                        BottomDamageTaken[i] = HealthUpdater(DifferentLineAttack_x(data[i + 1], data[i]),
                                                             DifferentLineAttack_o(data[i + 1], data[i]))

                    healths[i] = HealthUpdater(healths[i], SameLineDamageTaken[i])

                    healths[i] = HealthUpdater(healths[i], UpperDamageTaken[i])

                    healths[i] = HealthUpdater(healths[i], BottomDamageTaken[i])

                data = Destroyer(data, healths)

            # send the corresponding cells of updated location map of the towers to the manager process after each wave
            comm.send(data, dest=0, tag=22)
            # send the corresponding cells of updated health map of the towers to the manager process after each wave
            comm.send(healths, dest=0, tag=23)


