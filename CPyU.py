#!/usr/bin/env python                                    
import pipeline
import time
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

def ld(pipe):
    # Store
    if pipe.select == 0x3:
        displace = (pipe.val_reg & 0xC0)>>2 + (pipe.val_reg & 0x3F)
        #prog_mem[displace] = r[reg]
    
    # Load Displacement
    elif pipe.select == 0x2:
        displace = (pipe.val_reg & 0xC0)>>2 + (pipe.val_reg & 0x3F)
        #r[reg] = prog_mem[displace]
                
    # Load Immediate
    else:
        r[pipe.dst_reg] = pipe.val_reg
        pipe.stageName = "WB"
        if prog_mem[-1] == "00":
            pipe.stageName = "DONE"

def in_out():
    pass

def add(pipe):
    pipe.currStage += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] + r[pipe.src_reg]
        
def sub(pipe):
    pipe.currStage += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] - r[pipe.src_reg]

def and_op(pipe):
    pipe.currStage += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] & r[pipe.src_reg]

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


def write_to_reg(pipe):
    pipe.currStage += 1
    pipe.stageName = "WB"
    r[pipe.dst_reg] = pipe.alu_reg
    if prog_mem[-1] == "00":
            pipe.stageName = "DONE"

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
        
def do_pipeTwo(mem):
    
    if pipeCheck.clear_for_stage(pipeTwo, "IF") or pipeTwo.stageName == "":
        mem = pipeTwo.instr_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeTwo, "RF"):
        mem = pipeTwo.reg_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeTwo, "ALU"):
        opcode[pipeTwo.instr >> 4](pipeTwo)
    elif pipeCheck.clear_for_stage(pipeTwo, "WB"):
        write_to_reg(pipeTwo)
    
    elif pipeCheck.clear_for_stage(pipeThree, "IF") or pipeThree.stageName == "":
        mem = pipeThree.instr_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeThree, "RF"):
        mem = pipeThree.reg_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeThree, "ALU"):
        opcode[pipeThree.instr >> 4](pipeThree)
    elif pipeCheck.clear_for_stage(pipeThree, "WB"):
        write_to_reg(pipeThree)
    return mem

def do_pipeThree(mem):
    if pipeThree.stageName == "DONE":
        pipeThree.currStage += 1
    if pipeCheck.clear_for_stage(pipeThree, "IF") or pipeThree.stageName == "":
        mem = pipeThree.instr_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeThree, "RF"):
        mem = pipeThree.reg_fetch(mem)
    elif pipeCheck.clear_for_stage(pipeThree, "ALU"):
        opcode[pipeThree.instr >> 4](pipeThree)
    elif pipeCheck.clear_for_stage(pipeThree, "WB"):
        write_to_reg(pipeThree)
    return mem

'''
Main code
'''
pipeOne     = pipeline.Pipeline()
pipeTwo     = pipeline.Pipeline()
pipeThree   = pipeline.Pipeline()
pipeTwo.currStage = 1
pipeThree.currStage = 1
pipeCheck   = pipeline.Controller()
pipeCheck.pipes = [pipeOne, pipeTwo, pipeThree]
get_machine_code('out.a')
while prog_mem:
    if prog_mem[-1] == "00":
        if pipeOne.stageName == "DONE" and pipeTwo.stageName == "DONE" and pipeThree.stageName == "DONE":
            break


    print("Pipe One\n---------")
    print("\t"+str(hex(pipeOne.instr)))
    print("\t"+str(pipeOne.stageName)+", "+str(pipeOne.currStage))
    print("\n")
    print("Pipe Two\n---------")
    print("\t"+str(hex(pipeTwo.instr)))
    print("\t"+str(pipeTwo.stageName)+", "+str(pipeTwo.currStage))
    print("\n")
    print("Pipe Three\n---------")
    print("\t"+str(hex(pipeThree.instr)))
    print("\t"+str(pipeThree.stageName)+", "+str(pipeThree.currStage))
    
    time.sleep(1)
    
    if pipeOne.stageName == "DONE":
        pipeOne.currStage += 1
    if pipeTwo.stageName == "DONE":
        pipeTwo.currStage += 1
    if pipeThree.stageName == "DONE":
        pipeThree.currStage += 1
    
    if pipeCheck.stage_pos(pipeOne):
        
        if pipeCheck.clear_for_stage(pipeOne, "IF") or pipeOne.stageName == "":
            prog_mem = pipeOne.instr_fetch(prog_mem)
            if pipeTwo.stageName == "":
                pipeTwo.currStage += 1
            if pipeThree.stageName == "":
                pipeThree.currStage += 1
        elif pipeCheck.clear_for_stage(pipeOne, "RF"):
            prog_mem = pipeOne.reg_fetch(prog_mem)
        elif pipeCheck.clear_for_stage(pipeOne, "ALU"):
            opcode[pipeOne.instr >> 4](pipeOne)
        elif pipeCheck.clear_for_stage(pipeOne, "WB"):
            write_to_reg(pipeOne)
        else:
            prog_mem = do_pipeTwo(prog_mem)

    elif pipeCheck.stage_pos(pipeTwo):
        prog_mem = do_pipeTwo(prog_mem)
        
    elif pipeCheck.stage_pos(pipeThree):
        prog_mem = do_pipeThree(prog_mem)
    
    




print("R0 is "+str(hex(r[0])))
print("R1 is "+str(hex(r[1])))
print("R2 is "+str(hex(r[2])))
print("R3 is "+str(hex(r[3])))
                        
