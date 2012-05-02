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
    pipe.clockCycle += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] + r[pipe.src_reg]
        
def sub(pipe):
    pipe.clockCycle += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] - r[pipe.src_reg]

def and_op(pipe):
    pipe.clockCycle += 1
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
    pipe.clockCycle += 1
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
        



'''
Main code
'''
pipeOne     = pipeline.Pipeline()
pipeTwo     = pipeline.Pipeline()
pipeThree   = pipeline.Pipeline()
pipeFour    = pipeline.Pipeline()
pipeFive    = pipeline.Pipeline()

pipeTwo.clockCycle      = 1
pipeThree.clockCycle    = 1
pipeFour.clockCycle     = 1
pipeFive.clockCycle     = 1


check   = pipeline.Controller()
check.pipes = [pipeOne, pipeTwo, pipeThree, pipeFour, pipeFive]
get_machine_code('out.a')
check.IFQueue.append(pipeOne)
check.IFQueue.append(pipeTwo)
check.IFQueue.append(pipeThree)
check.IFQueue.append(pipeFour)
check.IFQueue.append(pipeFive)
while prog_mem:
    if prog_mem[-1] == "00":
        if pipeOne.stageName == "DONE" and pipeTwo.stageName == "DONE" and pipeThree.stageName == "DONE" and pipeFour.stageName == "DONE"  and pipeFive.stageName == "DONE":
            break


    print("Pipe One\n---------")
    print("\t"+str(hex(pipeOne.instr)))
    print("\t"+str(pipeOne.stageName)+", "+str(pipeOne.clockCycle))
    print("\n")
    print("Pipe Two\n---------")
    print("\t"+str(hex(pipeTwo.instr)))
    print("\t"+str(pipeTwo.stageName)+", "+str(pipeTwo.clockCycle))
    print("\n")
    print("Pipe Three\n---------")
    print("\t"+str(hex(pipeThree.instr)))
    print("\t"+str(pipeThree.stageName)+", "+str(pipeThree.clockCycle))
    print("\n")
    print("Pipe Four\n---------")
    print("\t"+str(hex(pipeFour.instr)))
    print("\t"+str(pipeFour.stageName)+", "+str(pipeFour.clockCycle))
    print("\n")
    print("Pipe Five\n---------")
    print("\t"+str(hex(pipeFive.instr)))
    print("\t"+str(pipeFive.stageName)+", "+str(pipeFive.clockCycle))
    print("\n")

    if pipeOne.stageName == "DONE":
        check.clear_pipe(pipeOne)
    if pipeTwo.stageName == "DONE":
        check.clear_pipe(pipeTwo)
    if pipeThree.stageName == "DONE":
        check.clear_pipe(pipeThree)
    if pipeFour.stageName == "DONE":
        check.clear_pipe(pipeFour)
    if pipeFive.stageName == "DONE":
        check.clear_pipe(pipeFive)
            
    time.sleep(1)


    while check.WBQueue:
        doPipe = check.WBQueue.pop(0)
        write_to_reg(doPipe)
        check.IFQueue.append(doPipe)
    while check.ALUQueue:
        doPipe = check.ALUQueue.pop(0)
        opcode[doPipe.instr >> 4](doPipe)
        if (doPipe.instr >> 4) != 0x2:
            check.WBQueue.append(doPipe)
        else:
            check.IFQueue.append(doPipe)
    while check.RFQueue:
        doPipe = check.RFQueue.pop(0)
        prog_mem = doPipe.reg_fetch(prog_mem)
        check.ALUQueue.append(doPipe)
    if not check.RFQueue and check.IFQueue:
        doPipe = check.IFQueue.pop(0)
        prog_mem = doPipe.instr_fetch(prog_mem)
        check.RFQueue.append(doPipe)
    




print("R0 is "+str(hex(r[0])))
print("R1 is "+str(hex(r[1])))
print("R2 is "+str(hex(r[2])))
print("R3 is "+str(hex(r[3])))
                        
