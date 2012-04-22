#!/usr/bin/python                                    

prog_mem = []
data_mem = []



r = [0,0,0,0]

hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

def cpy():
        pass

def swp():
        pass

def ld(reg):
        val = get_byte()
        if reg & 0x3:
                pass
        else:
             reg = (reg & 0xC)>>2
             r[reg] = val       

def in_out():
        pass

def add(reg):
        reg2 = reg & 0x3
        reg1 = (reg & 0xC)>>2
        r[reg1] = r[reg1]+r[reg2]
        
def sub(reg):
        reg2 = reg & 0x3
        reg1 = (reg & 0xC)>>2
        r[reg1] = r[reg1]-r[reg2]

def and_op(reg):
        reg2 = reg & 0x3
        reg1 = (reg & 0xC)>>2
        r[reg1] = r[reg1]&r[reg2]

def ret():
        pass

def clt():
        pass

def shift():
        pass

def not_op():
        pass

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


'''
Get Instructions
'''
def get_byte():
        instr = prog_mem.pop()
        instr_high = hexLookup[instr[0]]*16
        instr_low = hexLookup[instr[1]]
        
        return instr_high|instr_low


'''
Parse machine code and store in program memory
'''
def get_machine_code(filename):
        mc = open(filename, 'r')
        while True:
                line = mc.readline()
                if not line:
                        break
                instruction = line.rstrip().split(' ')
                for instr in instruction:
                        prog_mem.append(instr)
        mc.close()
        prog_mem.reverse()
		

opcode = {0:cpy, 1:swp, 2:ld, 3:in_out, 4:add, 5:sub,
          6:and_op, 7:ret, 8:clt, 9:shift, 10:not_op,
          11:ceq, 12:jump_call_br, 13:mul, 14:div,
          15:nop}


'''
Main code
'''
get_machine_code('machine.a')
while prog_mem:
        todo = get_byte()
        opcode[todo>>4](todo)

print("R0 is "+str(hex(r[0])))
print("R1 is "+str(hex(r[1])))
print("R2 is "+str(hex(r[2])))
print("R3 is "+str(hex(r[3])))
                        
