#!/usr/bin/env python                                    

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

def ld(opts):
    # opts = [register, selection, value]
    reg = opts[0]
    sel = opts[1]
    val = opts[2]
    # Store
    if sel == 0x3:
        displace = (val & 0xC0)>>2 + (val & 0x3F)
        prog_mem[displace] = r[reg]
    
    # Load Displacement
    elif sel == 0x2:
        displace = (val & 0xC0)>>2 + (val & 0x3F)
        r[reg] = prog_mem[displace]
                
    # Load Immediate
    else:
        r[reg] = val

def in_out():
    pass

def add(opts):
    # opts = [dest register, src register]
    dst = opts[0]
    src = opts[1]
    r[dst] = r[dst] + r[src]
        
def sub(opts):
    # opts = [dest register, src register]
    dst = opts[0]
    src = opts[1]
    r[dst] = r[dst] - r[src]

def and_op(opts):
    # opts = [dest register, src register]
    dst = opts[0]
    src = opts[1]
    r[dst] = r[dst] & r[src]

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


opcode = {0:cpy, 1:swp, 2:ld, 3:in_out, 4:add, 5:sub,
          6:and_op, 7:ret, 8:clt, 9:shift, 10:not_op,
          11:ceq, 12:jump_call_br, 13:mul, 14:div,
          15:nop}

'''
Instruction Fetch
'''
def instr_fetch():
    return get_byte(prog_mem.pop())

'''
Register Fetch
'''
def reg_fetch(byte):
    instr = byte >> 4
    # ld immediate, ld displacement, st; in, out
    if instr == 0x2 or instr == 0x3:
        nextWord = get_byte(prog_mem.pop())
        reg = (byte & 0xC) >> 2
        selection = (byte & 0x3)
        reg_list = [reg, selection, nextWord]

    # jmp, br, call
    elif instr == 0xC:
        pass
    
    # shla, shll, shra, shrl
    elif instr == 0x9:
        reg = (byte & 0xC) >> 2
        selection = (byte & 0x3)
        reg_list = [reg, selection]

    # ret, reti
    elif instr == 0x7:
        reg = (byte & 0x3)
        selection = (byte & 0xC) >> 2
        reg_list = [reg, selection]

    # everything else
    else:
        dest = (byte & 0xC) >> 2
        src  = (byte & 0x3)
        reg_list = [dest, src]

    return reg_list
        

'''
Convert string to numeric
'''
def get_byte(val):
    instr_high = hexLookup[val[0]]<<4
    instr_low = hexLookup[val[1]]
        
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
    if len(prog_mem) > 256:
        print("Error: program memory exceeded!")
        exit(1)
        
    for i in range(len(prog_mem), 256):
        prog_mem.append("00")

    prog_mem.reverse()
        

'''
Main code
'''
get_machine_code('out.a')
while prog_mem:
    if prog_mem[-1] == "00":
        break
    todo = instr_fetch()
    opts = reg_fetch(todo)
    opcode[todo>>4](opts)

print("R0 is "+str(hex(r[0])))
print("R1 is "+str(hex(r[1])))
print("R2 is "+str(hex(r[2])))
print("R3 is "+str(hex(r[3])))
                        
