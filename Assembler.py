#!/usr/bin/env python
import sys
import os
import re

regLookup = {'r0':0x0, 'r1':0x1, 'r2':0x2, 'r3':0x3}
mcFile = "hex/out.a"   

class Assembler:
    def __init__(self):
        pass

    def open_mc(self):
        try:
            f = open(mcFile, 'r')
            f.close()
            os.remove(mcFile)
        except IOError:
            f = open(mcFile, 'w')
            f.close()
    
    def cpy(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str(0)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def swp(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str(1)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def ld(self, line):
        instr   = line.pop(0)
        gotReg  = False
        memAddr = False
        displace = False
        for byte in line:
            byte = byte.split('\n', 1)[0]
            byte = re.sub(r'\,','',byte)
            byte = byte.split(';', 1)[0]
            if (not gotReg) and byte :
                try:
                    reg = regLookup[byte]
                    gotReg = True
                except KeyError:
                    print("Line "+str(lineNum)+": unknown register "+byte)
                    exit(1)
            elif byte:
                try:
                    if byte[0] == "r":
                        displaceReg = regLookup[byte]
                        displace = True
                        memAddr  = True
                    else:
                        val = byte[2:]
                        displace = False
                    if not displace:
                        break
                except IndexError:
                    print("Line "+str(lineNum)+": value "+byte+" must be hex!")
                    exit(1)
                    
        if instr == "st":
            sel = 0x3
        elif memAddr:
            sel = 0x2
        else:
            sel = 0x0
        if memAddr:
            if len(val) > 1:
                try:
                    valMSB = int(val[0])
                    if valMSB > 3:
                        print("Line "+str(lineNum)+": Invalid displacement value!")
                        exit(1)
                except ValueError:
                    print("Line "+str(lineNum)+": Invalid displacement value!")
                    exit(1)
                hexVal = str(displaceReg<<2|valMSB)+str(val[1])
            else:
                hexVal = str(displaceReg<<2)+str(val)
        else:
            hexVal = str(val)
        if len(hexVal) < 2:
            hexVal = "0"+hexVal
        if memAddr:
            word = str(2)+str(hex(reg<<2|sel)[2:]).capitalize()+" "+hexVal
        else:
            word = str(2)+str(hex(reg<<2|sel)[2:]).capitalize()+" "+hexVal
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    
    def in_out(self, line):
        gotReg  = False
        instr = line.pop(0)
        for byte in line:
            byte = byte.split('\n', 1)[0]
            byte = re.sub(r'\,','',byte)
            byte = byte.split(';', 1)[0]
            if (not gotReg) and byte:
                try:
                    reg = regLookup[byte]
                    gotReg = True
                except KeyError:
                    print("Line "+str(lineNum)+": unknown register "+byte)
                    exit(1)
            elif byte:
                val = byte[2:]
                break
            
        if instr == "in":
            sel = 0x1
        elif instr == "out":
            sel = 0x0
    
        hexVal = str(val)
        if len(hexVal) < 2:
            hexVal = "0"+hexVal    
        word = str(3)+str(hex(reg<<2|sel)[2:]).capitalize()+" "+hexVal
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def add(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str(4)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
            
    def sub(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str(5)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def and_op(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str(6)+str(hex(regs[0]<<2|regs[1])[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def ret(self):
        pass
    
    def clt(self):
        pass
    
    def shift(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
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
            print("Line "+str(lineNum)+": unknown command "+instr)
            exit(1)
            
        word = str(9)+str(hex(regs[0]<<2|sel)[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def not_op(self, line):
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
                print("Line "+str(lineNum)+": unknown register "+byte)
                exit(1)
    
        word = str("A")+str(hex(regs[0]<<2)[2:]).capitalize()
            
        f = open(mcFile, 'a')
        f.write(word+"\n")
        f.close()
    
    def ceq(self):
        pass
    
    def jump_call_br(self):
        pass
    
    def mul(self):
        pass
    
    def div(self):
        pass
    
    def nop(self):
        pass
    
    
    # open does not work on files with underscore in name (for some reason)
    # so this prompts a warning until a real solution is found
    def compiler(self, asmFile):
        self.open_mc()
        
        if re.search(r'\_', asmFile):
            print("Error: file cannot contain '_' in name")
            exit(1)
           
        try:
            file = open(asmFile, 'r')
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
        
        opcode = {0:self.cpy, 1:self.swp, 2:self.ld, 3:self.in_out, 4:self.add, 5:self.sub,
                  6:self.and_op, 7:self.ret, 8:self.clt, 9:self.shift, 10:self.not_op,
                  11:self.ceq, 12:self.jump_call_br, 13:self.mul, 14:self.div,
                  15:self.nop}
        
        lineNum = 1
        
        for line in lines:
            instr = re.sub(r'\:', '', line).split(' ')
            if instr[0] == '\n':
                return
            try:
                opcode[commandTable[instr[0]]](instr)
            except KeyError or IndexError:
                print("Line "+str(lineNum)+": command not found: "+instr[0])
                return
            lineNum += 1
            
