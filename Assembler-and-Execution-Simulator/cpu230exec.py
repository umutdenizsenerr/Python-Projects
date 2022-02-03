import sys

def add(val1, val2):
    c = 0
    newVal = ''
    for i in reversed(range(len(val1))):
        newVal = str((int(val1[i]) + int(val2[i]) + c) % 2) + newVal
        c = (int(val1[i]) + int(val2[i]) + c) // 2
    return newVal

def carry(val1, val2):
    c = 0
    newVal = ''
    for i in reversed(range(len(val1))):
        newVal = str((int(val1[i]) + int(val2[i]) + c) % 2) + newVal
        c = (int(val1[i]) + int(val2[i]) + c) // 2
    if(c == 1):
        return True
    else:
        return False

def complement(val):
    newVal =''
    for element in range(0, 16):
        if val[element] == '0':
            newVal += '1'
        else:
            newVal += '0'
    return newVal

file = open(sys.argv[1], 'r')
txtFileName = sys.argv[1][:-4] + '.txt'
wfile = open(txtFileName, 'w')

registerValueDictionary = {"A": "0000000000000000", "B": "0000000000000000",
                           "C": "0000000000000000", "D": "0000000000000000",
                           "E": "0000000000000000", "S": "1111111111111111", "PC": "0000000000000000"}
registerDictionary = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "S", "0": "PC"}
flagDictionary = {'ZF': 0, 'CF': 0, 'SF': 0}
stack = ["0000000000000000"] * 65536


i = 0
for line in file:
    line = line.strip()
    binaryNum = (bin(int(line,16))[2:].zfill(24))
    opcode = hex(int(binaryNum[:6],2))[2:]
    addMode = binaryNum[6:8]
    operand = hex(int(binaryNum[8:],2))[2:]
    stack[i] = opcode
    stack[i+1] = addMode
    stack[i+2] = operand
    i += 3

while 1:
    opcode = stack[int(registerValueDictionary["PC"], 2)]
    addMode = stack[int(registerValueDictionary["PC"], 2) + 1]
    operand = stack[int(registerValueDictionary["PC"], 2) + 2]


    if opcode == "1": #HALT
        break

    elif opcode == "2": #LOAD
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00": #IMMEDIATE
            registerValueDictionary["A"] ="{:016b}".format(int(operand, 16))
        elif addMode == "01": #REGISTER
            registerValueDictionary["A"] = registerValueDictionary[registerDictionary[operand]]
        elif addMode == '10': #MEMORY IN REG
            registerValueDictionary["A"] = stack[int(registerValueDictionary[registerDictionary[operand]], 2)]
        elif addMode == '11': #MEMORY
            registerValueDictionary["A"] = stack[int(operand, 16)]

    elif opcode == "3":  # STORE
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "01": #REGISTER
            registerValueDictionary[registerDictionary[operand]] = registerValueDictionary["A"]
        elif addMode == '10': #MEMORY IN REG
            stack[int(registerValueDictionary[registerDictionary[operand]], 2)] = registerValueDictionary["A"]
        elif addMode == '11': #MEMORY
            stack[int(operand, 16)] = registerValueDictionary["A"]

    elif opcode == "4":  # ADD
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        flagDictionary['SF'] = 0  # treating all bits as unsigned integer
        if addMode == "00":  #IMMEDIATE
            c = carry(registerValueDictionary["A"], "{:016b}".format(int(operand, 16)))
            registerValueDictionary["A"] = add(registerValueDictionary["A"], "{:016b}".format(int(operand, 16)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == "01":  # REGISTER
            c = carry(registerValueDictionary["A"], registerValueDictionary[registerDictionary[operand]])
            registerValueDictionary["A"] = add(registerValueDictionary["A"], registerValueDictionary[registerDictionary[operand]])
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '10':  #MEMORY IN REG
            c = carry(registerValueDictionary["A"],  stack[int(registerValueDictionary[registerDictionary[operand]], 2)])
            registerValueDictionary["A"] = add(registerValueDictionary["A"],  stack[int(registerValueDictionary[registerDictionary[operand]], 2)])
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '11':  #MEMORY
            c = carry(registerValueDictionary["A"], stack[int(operand, 16)])
            registerValueDictionary["A"] = add(registerValueDictionary["A"], stack[int(operand, 16)])
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        if registerValueDictionary["A"] == "{:016b}".format(0):
            flagDictionary["ZF"] = 1
        else:
            flagDictionary["ZF"] = 0
        if registerValueDictionary["A"][0] == '1':
            flagDictionary["SF"] = 1
        else:
            flagDictionary["SF"] = 0

    elif opcode == "5":  # SUB
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00": #IMMEDIATE
            c = carry(registerValueDictionary['A'], add(complement("{:016b}".format(int(operand, 16))),  "{:016b}".format(1)))
            registerValueDictionary['A'] = add(registerValueDictionary['A'], add(complement("{:016b}".format(int(operand, 16))),  "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == "01":  # REGISTER
            c = carry(registerValueDictionary['A'], add(complement(registerValueDictionary[registerDictionary[operand]]), "{:016b}".format(1)))
            registerValueDictionary['A'] = add(registerValueDictionary['A'], add(complement(registerValueDictionary[registerDictionary[operand]]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '10': #MEMORY IN REG
            c = carry(registerValueDictionary["A"],  add(complement(stack[int(registerValueDictionary[registerDictionary[operand]], 2)]), "{:016b}".format(1)))
            registerValueDictionary["A"] = add(registerValueDictionary["A"],  add(complement(stack[int(registerValueDictionary[registerDictionary[operand]], 2)]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '11': #MEMORY
            c = carry(registerValueDictionary["A"], add(complement(stack[int(operand, 16)]), "{:016b}".format(1)))
            registerValueDictionary["A"] = add(registerValueDictionary["A"], add(complement(stack[int(operand, 16)]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        if registerValueDictionary["A"] == "{:016b}".format(0):
            flagDictionary["ZF"] = 1
        else:
            flagDictionary["ZF"] = 0
        if registerValueDictionary["A"][0] == '1':
            flagDictionary['SF'] = 1
        else:
            flagDictionary['SF'] = 0

    elif opcode == "6":  # INC
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "01": #REGISTER
            c = carry(registerValueDictionary[registerDictionary[operand]], "{:016b}".format(1))
            registerValueDictionary[registerDictionary[operand]] = add(registerValueDictionary[registerDictionary[operand]], "{:016b}".format(1))
            if registerValueDictionary[registerDictionary[operand]] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if registerValueDictionary[registerDictionary[operand]][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
        elif addMode == '10': #MEMORY IN REG
            c = carry(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], "{:016b}".format(1))
            stack[int(registerValueDictionary[registerDictionary[operand]], 2)] = add(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], "{:016b}".format(1))
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
        elif addMode == '11': #MEMORY
            c = carry(stack[int(operand, 16)], "{:016b}".format(1))
            stack[int(operand, 16)] = add(stack[int(operand, 16)], "{:016b}".format(1))
            if stack[int(operand, 16)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if stack[int(operand, 16)][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0

    elif opcode == "7":  # DEC
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "01": #REGISTER
            c = carry(registerValueDictionary[registerDictionary[operand]], add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            registerValueDictionary[registerDictionary[operand]] = add(registerValueDictionary[registerDictionary[operand]], add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            if registerValueDictionary[registerDictionary[operand]] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if registerValueDictionary[registerDictionary[operand]][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
        elif addMode == '10': #MEMORY IN REG
            c = carry(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            stack[int(registerValueDictionary[registerDictionary[operand]], 2)] = add(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
        elif addMode == '11': #MEMORY
            c = carry(stack[int(operand, 16)],  add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            stack[int(operand, 16)] = add(stack[int(operand, 16)],  add(complement("{:016b}".format(1)), "{:016b}".format(1)))
            if  stack[int(operand, 16)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
            if stack[int(operand, 16)][0] == '1':
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0

    elif opcode == "8":  # XOR
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00":  # IMMEDIATE
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) ^ int(operand, 16))
        elif addMode == "01":  # REGISTER
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) ^ int(registerValueDictionary[registerDictionary[operand]] ,2))
        elif addMode == '10': #MEMORY IN REG
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) ^ int(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], 2))
        elif addMode == '11': #MEMORY
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) ^ int(stack[int(operand, 16)], 2))
        if registerValueDictionary["A"] == "{:016b}".format(0):
            flagDictionary['ZF'] = 1
        else:
            flagDictionary['ZF'] = 0
        if registerValueDictionary["A"][0] == '1':
            flagDictionary['SF'] = 1
        else:
            flagDictionary['SF'] = 0

    elif opcode == "9":  # AND
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00":  # IMMEDIATE
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) & int(operand, 16))
        elif addMode == "01":  # REGISTER
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) & int(registerValueDictionary[registerDictionary[operand]] ,2))
        elif addMode == '10': #MEMORY IN REG
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) & int(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], 2))
        elif addMode == '11': #MEMORY
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) & int(stack[int(operand, 16)], 2))
        if registerValueDictionary["A"] == "{:016b}".format(0):
            flagDictionary['ZF'] = 1
        else:
            flagDictionary['ZF'] = 0
        if registerValueDictionary["A"][0] == '1':
            flagDictionary['SF'] = 1
        else:
            flagDictionary['SF'] = 0

    elif opcode == "a":  # OR
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00":  # IMMEDIATE
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) | int(operand, 16))
        elif addMode == "01":  # REGISTER
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) | int(registerValueDictionary[registerDictionary[operand]] ,2))
        elif addMode == '10': #MEMORY IN REG
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) | int(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], 2))
        elif addMode == '11': #MEMORY
            registerValueDictionary["A"] = "{:016b}".format(int(registerValueDictionary["A"], 2) | int(stack[int(operand, 16)], 2))
        if registerValueDictionary["A"] == "{:016b}".format(0):
            flagDictionary['ZF'] = 1
        else:
            flagDictionary['ZF'] = 0
        if registerValueDictionary["A"][0] == '1':
            flagDictionary['SF'] = 1
        else:
            flagDictionary['SF'] = 0

    elif opcode == "b":  # NOT
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == '01': #REGISTER
            registerValueDictionary[registerDictionary[operand]] = complement(registerValueDictionary[registerDictionary[operand]])
            if registerValueDictionary[registerDictionary[operand]][0] == '1': #NEGATIVE SIGN
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
            if registerValueDictionary[registerDictionary[operand]] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
        if addMode == '10': #MEMORY IN REG
            stack[int(registerValueDictionary[registerDictionary[operand]], 2)] = complement(stack[int(registerValueDictionary[registerDictionary[operand]], 2)])
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)][0] == '1':  # NEGATIVE SIGN
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
            if stack[int(registerValueDictionary[registerDictionary[operand]], 2)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0
        if addMode == '11': #MEMORY
            stack[int(operand, 16)] = complement(stack[int(operand, 16)])
            if stack[int(operand, 16)][0] == '1':  # NEGATIVE SIGN
                flagDictionary['SF'] = 1
            else:
                flagDictionary['SF'] = 0
            if stack[int(operand, 16)] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0

    elif opcode == "c":  # SHL
         registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
         if addMode == "01": #REGISTER
             binary = registerValueDictionary[registerDictionary[operand]]
             registerValueDictionary[registerDictionary[operand]] = "{:016b}".format(int(registerValueDictionary[registerDictionary[operand]], 2) << 1)
             if registerValueDictionary[registerDictionary[operand]] == "{:016b}".format(0):
                 flagDictionary['ZF'] = 1
             else:
                 flagDictionary['ZF'] = 0
             if registerValueDictionary[registerDictionary[operand]][0] == '1':
                 flagDictionary['SF'] = 1
             else:
                 flagDictionary['SF'] = 0
             if binary[0] == '1':
                 flagDictionary['CF'] = 1
             else:
                 flagDictionary['CF'] = 0

    elif opcode == "d":  # SHR
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        flagDictionary['SF'] = 0
        if addMode == "01":  # REGISTER
            registerValueDictionary[registerDictionary[operand]] = "{:016b}".format(int(registerValueDictionary[registerDictionary[operand]], 2) >> 1)
            if registerValueDictionary[registerDictionary[operand]] == "{:016b}".format(0):
                flagDictionary['ZF'] = 1
            else:
                flagDictionary['ZF'] = 0

    elif opcode == 'e':  # NOP
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == 'f':  # PUSH
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == '01':  #REGISTER
            stack[int(registerValueDictionary["S"], 2)] = registerValueDictionary[registerDictionary[operand]]
            registerValueDictionary["S"] = add(registerValueDictionary["S"], add(complement("{:016b}".format(2)), "{:016b}".format(1)))

    elif opcode == '10':  # POP
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == '01':  #REGISTER
            registerValueDictionary["S"] = add(registerValueDictionary["S"], "{:016b}".format(2))
            registerValueDictionary[registerDictionary[operand]] = stack[int(registerValueDictionary["S"], 2)]
            stack[int(registerValueDictionary["S"], 2)] = ''

    elif opcode == '11': # CMP
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00":  # IMMEDIATE
            c = carry(registerValueDictionary['A'], add(complement("{:016b}".format(int(operand, 16))), "{:016b}".format(1)))
            compare = add(registerValueDictionary['A'], add(complement("{:016b}".format(int(operand, 16))), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == "01":  # REGISTER
            c = carry(registerValueDictionary['A'], add(complement(registerValueDictionary[registerDictionary[operand]]), "{:016b}".format(1)))
            compare = add(registerValueDictionary['A'], add(complement(registerValueDictionary[registerDictionary[operand]]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '10':  # MEMORY IN REG
            c = carry(registerValueDictionary["A"],add(complement(stack[int(registerValueDictionary[registerDictionary[operand]], 2)]), "{:016b}".format(1)))
            compare = add(registerValueDictionary["A"], add(complement(stack[int(registerValueDictionary[registerDictionary[operand]], 2)]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        elif addMode == '11':  # MEMORY
            c = carry(registerValueDictionary["A"], add(complement(stack[int(operand, 16)]), "{:016b}".format(1)))
            compare = add(registerValueDictionary["A"], add(complement(stack[int(operand, 16)]), "{:016b}".format(1)))
            if c:
                flagDictionary['CF'] = 1
            else:
                flagDictionary['CF'] = 0
        if compare == "{:016b}".format(0):
            flagDictionary["ZF"] = 1
        else:
            flagDictionary["ZF"] = 0
        if compare[0] == '1':
            flagDictionary['SF'] = 1
        else:
            flagDictionary['SF'] = 0

    elif opcode == '12':  # JMP
        if addMode == '00':
            registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))

    elif opcode == '13':  # JZ || JE
        if addMode == '00':
            if flagDictionary['ZF'] == 1:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '14':  # JNZ || JNE
        if addMode == '00':
            if flagDictionary['ZF'] == 0:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '15':  # JC
        if addMode == '00':
            if flagDictionary['CF'] == 1:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '16':  # JNC
        if addMode == '00':
            if flagDictionary['CF'] == 0:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '17':  # JA
        if addMode == '00':
            if flagDictionary['SF'] == 0 and flagDictionary['ZF'] == 0:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '18':  # JAE
        if addMode == '00':
            if flagDictionary['SF'] == 0 and flagDictionary['ZF'] == 1:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '19':  # JB
        if addMode == '00':
            if flagDictionary['SF'] == 1 and flagDictionary['ZF'] == 0: # CF = 0 ?
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '1a':  # JBE
        if addMode == '00':
            if flagDictionary['SF'] == 1 and flagDictionary['ZF'] == 1:
                registerValueDictionary["PC"] = "{:016b}".format(int(operand, 16))
            else:
                registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == '1b':  # READ
        input_user = input()
        if addMode == '01': #REGISTER
            registerValueDictionary[registerDictionary[operand]] = "{:016b}".format(ord(input_user[0]))
            registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        elif addMode == '10': #MEMORY IN REG
            stack[int(registerValueDictionary[registerDictionary[operand]], 2)] = "{:016b}".format(ord(input_user[0]))
            registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        elif addMode == '11': #MEMORY
            stack[int(operand, 16)] = "{:016b}".format(ord(input_user[0]))
            registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')

    elif opcode == "1c":  # PRINT
        registerValueDictionary["PC"] = add(registerValueDictionary["PC"], '0000000000000011')
        if addMode == "00": #IMMEDIATE
            wfile.write(chr(int(operand, 16)))
            wfile.write("\n")
        elif addMode == "01": #REGISTER
            wfile.write(chr(int(registerValueDictionary[registerDictionary[operand]], 2)))
            wfile.write("\n")
        elif addMode == '10': #MEMORY IN REG
            wfile.write(chr(int(stack[int(registerValueDictionary[registerDictionary[operand]], 2)], 2)))
            wfile.write("\n")
        elif addMode == '11': #MEMORY
            wfile.write(chr(int(stack[operand]), 2))
            wfile.write("\n")

