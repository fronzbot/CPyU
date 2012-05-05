#!/usr/bin/env python
import sys
import os
import re

regLookup = {'r0':0x0, 'r1':0x1, 'r2':0x2, 'r3':0x3}
mcFile = "out.a"
        

try:
    f = open(mcFile, 'r')
    f.close()
    os.remove(mcFile)
except IOError:
    f = open(mcFile, 'w')
    f.close()
    
def cpy(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str(0)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def swp(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str(1)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def ld(line):
    instr = line.pop(0)
    gotReg = False
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]

        if (not gotReg) and byte :
            try:
                reg = regLookup[byte]
                gotReg = True
            except KeyError:
                print("Line "+str(lineNum)+": unkown register "+byte)
                exit(1)
        elif byte:
            try:
                val = byte[2:]
                break
            except IndexError:
                print("Line "+str(lineNum)+": value "+byte+" must be hex!")
                exit(1)

    hexVal = str(val)
    if len(hexVal) < 2:
        hexVal = "0"+hexVal
    word = str(2)+str(hex(reg<<2)[2:]).capitalize()+" "+hexVal
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()


def in_out():
    pass

def add(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str(4)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()
        
def sub(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print(len(byte))
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str(5)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def and_op(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str(6)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def ret():
    pass

def clt():
    pass

def shift(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 2:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    if instr == "shla":
        sel = 0x0
    elif instr == "shll":
        sel = 0x1
    elif instr == "shra":
        sel = 0x2
    elif instr == "shrl":
        sel = 0x3
    else:
        print("Line "+str(lineNum)+": unkown command "+instr)
        exit(1)
        
    word = str(9)+str(hex(regs[0]<<2|sel)[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def not_op(line):
    instr = line.pop(0)
    regs = []
    for byte in line:
        byte = byte.split('\n', 1)[0]
        byte = re.sub(r'\,','',byte)
        byte = byte.split(';', 1)[0]
        if len(regs) == 1:
            break
        try:
            regs.append(regLookup[byte])
        except KeyError:
            print("Line "+str(lineNum)+": unkown register "+byte)
            exit(1)

    word = str("A")+str(hex(regs[0]<<2)[2:]).capitalize()
        
    f = open(mcFile, 'a')
    f.write(word+"\n")
    f.close()

def ceq():
    pass

def jump_call_br():
    pass

def mul():
    pass

def div():
    pass

def nop():
    pass




try:
    file = open(sys.argv[1], 'r')
except IndexError:
    print("Error: no file specifed")
    exit(1)
except IOError:
    print("File "+sys.argv[1]+" does not exist")
    exit(1)

lines = []

while True:
    temp = file.readline()
    if not temp:
        break
    lines.append(temp)
file.close()
    

commandTable = {'cpy':0x0, 'swap':0x1, 'ld':0x2, 'st':0x2, 'in':0x3,
                'out':0x3, 'add':0x4, 'sub':0x5, 'and':0x6, 'ceq':0xB,
                'clt':0x8, 'not':0xA, 'mul':0xD, 'div':0xE, 'shla':0x9,
                'shll':0x9, 'shra':0x9, 'shrl':0x9, 'jmp':0xC, 'br':0xC,
                'call':0xC, 'ret':0x7, 'reti':0x7, 'nop':0xF}

opcode = {0:cpy, 1:swp, 2:ld, 3:in_out, 4:add, 5:sub,
          6:and_op, 7:ret, 8:clt, 9:shift, 10:not_op,
          11:ceq, 12:jump_call_br, 13:mul, 14:div,
          15:nop}

lineNum = 1
for line in lines:
    instr = re.sub(r'\:', '', line).split(' ')
    try:
        opcode[commandTable[instr[0]]](instr)
    except KeyError or IndexError:
        print("Line: "+str(lineNum)+" command not found: "+instr[0])
        exit(1)
    lineNum += 1
