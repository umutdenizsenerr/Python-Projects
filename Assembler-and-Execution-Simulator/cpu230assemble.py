import sys
import re
def converter(op,adr,oper):
    s_op = str(op)
    s_adr = str(adr)
    s_oper = str(oper)
    opcode = int(s_op, 16)
    addrmode = int(s_adr, 16)
    operand = int(s_oper, 16)

    bopcode = format(opcode, '06b')
    baddrmode = format(addrmode, '02b')
    boperand = format(operand, '016b')
    bin = '0b' + bopcode + baddrmode + boperand
    ibin = int(bin[2:], 2);
    instr = format(ibin, '06x')
    return instr

def error():
    print("error")
    quit()  # sys.exit("error")

file0 = open(sys.argv[1], 'r')
labels = []
labelsDictionary = {}
registerDictionary = {"A" : 1, "B" : 2, "C" : 3, "D" : 4, "E" : 5, "S" : 6, "PC" : 0 }
instructionDictionary = {"HALT" : 0x01,"LOAD" : 0x02,
                         "STORE" : 0x03,"ADD" : 0x04,
                         "SUB" : 0x05,"INC" : 0x06,
                         "DEC" : 0x07,"XOR" : 0x08,
                         "AND" : 0x09,"OR" : 0x0A,
                         "NOT" : 0x0B,"SHL" : 0x0C,
                         "SHR" : 0x0D,"NOP" : 0x0E,
                         "PUSH" : 0x0F,"POP" : 0x10,
                         "CMP" : 0x11,"JMP" : 0x12,
                         "JZ" : 0x13,"JE" : 0x13,
                         "JNZ" : 0x14,"JNE" : 0x14,
                         "JC" : 0x15,"JNC" : 0x16,
                         "JA" : 0x17,"JAE" : 0x18,
                         "JB" : 0x19,"JBE" : 0x1A,
                         "READ" : 0x1B,"PRINT" : 0x1C}
memoryAddress = 0
for line in file0:
    line = line.strip()
    words = line.split(" ")
    while ' ' in words:
        words.remove('')
    if line.rstrip():
        if words[-1][-1] != ":":
            memoryAddress += 3
        else:
            if words[-1][:-1].upper() in labels:
                error()
            else:
                labelsDictionary[words[-1][:-1].upper()] = hex(memoryAddress)
                labels.append(words[-1][:-1].upper())

file = open(sys.argv[1], 'r')
binName = sys.argv[1][:-4] + '.bin'
wfile = open(binName, 'w')

for line in file:
    line = line.strip()
    words = line.split(" ")
    while '' in words:
        words.remove('')
    if line.rstrip():
        if words[-1][-1] != ":":
            if words[0].upper() in instructionDictionary:
                opcode = hex(instructionDictionary[words[0].upper()])
            else:
                error()
            if len(words) == 2:
                if words[1][0] == "'" and words[1][-1] == "'": #Character
                    addMode = 0
                    operand = hex(ord(words[1][1:-1]))
                elif words[1][0] == "[" and words[1][-1] == "]": #Memory Address
                    if words[1][1:-1].upper() in registerDictionary:
                        addMode = 2
                        operand = registerDictionary[words[1][1:-1].upper()]
                    else:
                        addMode = 3
                        operand = words[1][1:-1]
                elif words[1].upper() in registerDictionary.keys(): #Register
                    addMode = 1
                    operand = registerDictionary[words[1].upper()]
                elif words[1].upper() in labelsDictionary.keys(): #Label
                    addMode = 0
                    operand = labelsDictionary[words[1].upper()]
                elif words[1][0].isdigit(): #HexNumber >> Immediate
                    addMode = 0
                    operand = words[1]
                else:
                    error()
            elif len(words) == 1:   #HALT or NOP
                if words[0].upper() == 'HALT' or words[0].upper() == 'NOP':
                    pass
                else:
                    error()
                addMode = 0
                operand = 0
            else:
                error()


            wfile.write(converter(opcode,addMode,operand))
            wfile.write("\n")
