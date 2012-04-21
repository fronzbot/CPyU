#!/usr/bin/python                                    

prog_mem = []
data_mem = []

r0 = 0
r1 = 0
r2 = 0
r3 = 0

hexLookup = {'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

def cpy_swp():
        pass

def ld():
        pass

def in_out():
        pass

def add():
        pass

def sub():
        pass

def and_op():
        pass

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

def reti():
        pass

def nop():
        pass


'''
Get Instructions
'''
def get_instructions():
        instr = prog_mem.pop()
        try:
                instr_high = hexLookup[instr[0]]*16
        except KeyError:
                instr_high = instr[0]
        try:
                instr_low = hexLookup[instr[1]]
        except KeyError:
                instr_low = instr[1]

        return intr_high|instr_low


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
		

opcode = {1:cpy_swp, 2:ld, 3:in_out, 4:add, 5:sub,
          6:and_op, 7:ret, 8:clt, 9:shift, 10:not_op,
          11:ceq, 12:jump_call_br, 13:mul, 14:div,
          15:reti, 0:nop}


'''
Main code
'''
get_machine_code('machine.a')

while not prog_mem.empty():
        todo = get_instrustions()

                        
