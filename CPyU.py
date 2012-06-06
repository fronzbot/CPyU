#!/usr/bin/env python                                    
import pipeline
import time
import argparse

d = {}
goodDispArgs = ['reg', 'pipe', 'flag', 'clock', 'stalls', 'prog_mem', 'data_mem', 'verbose']
parser = argparse.ArgumentParser(prog='CPyU.py', description='Debugging flags for CPyU')
parser.add_argument('--disp', action="store", dest="disp", nargs='+',
                    help='Choose what options to display [reg, pipe, flag, clock, stalls, prog_mem, data_mem, verbose]')
parser.add_argument('--wait', action="store", dest="wait", type=int,
                    help='Choose how long to wait before progressing through program (indicated in seconds)')
results = parser.parse_args()
if results.disp:
    for arg in results.disp:
        d[arg] = True
        
for allArgs in goodDispArgs:
    if allArgs not in d:
        if 'verbose' in d:
            d[allArgs] = True
        else:
            d[allArgs] = False


prog_mem = []
data_mem = []
io_mem   = []

flag = {"C":0, "V":0, "Z":0, "N":0}
r = [0,0,0,0]

hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

def cpy(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "WB"
    r[pipe.dst_reg] = r[pipe.src_reg]
    
def swp(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.src_reg]

def ld(pipe):
    # Store
    if pipe.select == 0x3:
        pipe.mem_reg = r[(pipe.val_reg & 0xC0) >> 6] + (pipe.val_reg & 0x3F)
        #pipe.stageName = "ALU"
    
    # Load Displacement
    elif pipe.select == 0x2:
        pipe.mem_reg = r[(pipe.val_reg & 0xC0)>>6] + (pipe.val_reg & 0x3F)
        #pipe.stageName = "ALU"
                
    # Load Immediate
    else:
        r[pipe.dst_reg] = pipe.val_reg
        #pipe.stageName = "WB"
        if prog_mem[-1] == "00":
            pipe.stageName = "DONE"


def add(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] + r[pipe.src_reg]
    if pipe.alu_reg > 0xFF:
        pipe.alu_reg = 0xFF
        flag["C"] ^= 1
        
def sub(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] - r[pipe.src_reg]
    if pipe.alu_reg < 0:
        pipe.alu_reg = -1*pipe.alu_reg
        flag["N"]^=1

def and_op(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] & r[pipe.src_reg]

def ret():
    pass

def clt():
    pass

def shift(pipe):
    pipe.clockCycle += 1
    #pipe.stageName = "ALU"

    #Arithmetic left shift
    if pipe.select == 0x0:
        pipe.alu_reg = r[pipe.dst_reg] << 1
        if (pipe.alu_reg & 0x180) == 0x180:
            pipe.alu_reg &= 0xFF
            flag["V"] ^= 1
            
    #Logical Left Shift        
    elif pipe.select == 0x1:
        pipe.alu_reg = r[pipe.dst_reg] << 1

    #Arithmetic Right Shift
    elif pipe.select == 0x2:
        pipe.alu_reg = r[pipe.dst_reg] >> 1
        if r[pipe.dst_reg] & 0x80 == 0x80:
            pipe.alu_reg |= 0x80

    #Logical Right Shift        
    elif pipe.select == 0x3:
        pipe.alu_reg = r[pipe.dst_reg] >> 1

def not_op(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "ALU"
    pipe.alu_reg = ~r[pipe.dst_reg]&0xFF
    

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


opcode = {0:cpy, 1:swp, 2:ld, 4:add, 5:sub,
          6:and_op, 7:ret, 8:clt, 9:shift, 10:not_op,
          11:ceq, 12:jump_call_br, 13:mul, 14:div,
          15:nop}

def memory_addressing(pipe):
    #pipe.clockCycle+=1
    #pipe.stageName = "MA"
   
    if (pipe.instr >> 4) == 0x2: # ld/st
        if pipe.select == 0x3:
            data_mem[pipe.mem_reg] = r[pipe.dst_reg]
        elif pipe.select == 0x2:
            r[pipe.dst_reg] = data_mem[pipe.mem_reg]
          
    elif (pipe.instr >> 4) == 0x3: # in/out
        if pipe.select == 0x0:  # Out
            io_mem[pipe.val_reg] = r[pipe.dst_reg]
        elif pipe.select == 0x1:    # In
            r[pipe.dst_reg] = io_mem[pipe.val_reg]
       
    if prog_mem[-1] == "00":
        pipe.stageName == "DONE"
    

def write_to_reg(pipe):
    #pipe.clockCycle += 1
    #pipe.stageName = "WB"
    if pipe.instr >> 4 == 0x1:  #SWAP
        r[pipe.src_reg] = r[pipe.dst_reg]
        
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
            data_mem.append(0x0)
    mc.close()
    if len(prog_mem) > 256:
        print("Error: program memory exceeded!")
        exit(1)
        
    for i in range(len(prog_mem), 256):
        prog_mem.append("00")
        data_mem.append(0x0)
        io_mem.append(0x0)

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
pipeTwo.stalls          = 1
pipeThree.clockCycle    = 1
pipeThree.stalls        = 1
pipeFour.clockCycle     = 1
pipeFour.stalls         = 1
pipeFive.clockCycle     = 1
pipeFive.stalls         = 1


check   = pipeline.Controller()
check.pipes = [pipeOne, pipeTwo, pipeThree, pipeFour, pipeFive]
get_machine_code('out.a')
check.IFQueue.append(pipeOne)
check.IFQueue.append(pipeTwo)
check.IFQueue.append(pipeThree)
check.IFQueue.append(pipeFour)
check.IFQueue.append(pipeFive)
pipeOne.stageName   = "IF"
pipeTwo.stageName   = "IF"
pipeThree.stageName = "IF"
pipeFour.stageName  = "IF"
pipeFive.stageName  = "IF"
while prog_mem:
    if prog_mem[-1] == "00":
        if pipeOne.stageName == "DONE" and pipeTwo.stageName == "DONE" and pipeThree.stageName == "DONE" and pipeFour.stageName == "DONE"  and pipeFive.stageName == "DONE":
            break
        
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

    # DEBUGGING PRINTS
    if d['clock']:
        print("Current Clock Cycle:\t"+str(check.masterClock)+"\n")
    if d['pipe']:
        print("pipeOne :\t"+str(hex(pipeOne.instr))+",\t"+ pipeOne.stageName+",\t"+str(pipeOne.clockCycle))
        print("pipeTwo :\t"+str(hex(pipeTwo.instr))+",\t"+ pipeTwo.stageName+",\t"+str(pipeTwo.clockCycle))
        print("pipeThree :\t"+str(hex(pipeThree.instr))+",\t"+ pipeThree.stageName+",\t"+str(pipeThree.clockCycle))
        print("pipeFour :\t"+str(hex(pipeFour.instr))+",\t"+ pipeFour.stageName+",\t"+str(pipeFour.clockCycle))
        print("pipeFive :\t"+str(hex(pipeFive.instr))+",\t"+ pipeFive.stageName+",\t"+str(pipeFive.clockCycle))
    if d['stalls']:
        print("pipeOne   Stall Count:\t"+str(pipeOne.stalls))
        print("pipeTwo   Stall Count:\t"+str(pipeTwo.stalls))
        print("pipeThree Stall Count:\t"+str(pipeThree.stalls))
        print("pipeFour  Stall Count:\t"+str(pipeFour.stalls))
        print("pipeFive  Stall Count:\t"+str(pipeFive.stalls))
    if d['reg']:
        print("R0 is "+str(hex(r[0])))
        print("R1 is "+str(hex(r[1])))
        print("R2 is "+str(hex(r[2])))
        print("R3 is "+str(hex(r[3])))
    if d['flag']:
        print("C flag is "+str(flag["C"]))
        print("V flag is "+str(flag["V"]))
        print("Z flag is "+str(flag["Z"]))
        print("N flag is "+str(flag["N"]))

    if d['reg'] or d['flag'] or d['pipe']:
        print("---------\n")

    if results.wait:
        time.sleep(results.wait)

    # Check stalls
    if check.masterClock - pipeOne.clockCycle:
        pipeOne.stalls += 1
    if check.masterClock - pipeTwo.clockCycle:
        pipeTwo.stalls += 1
    if check.masterClock - pipeThree.clockCycle:
        pipeThree.stalls += 1
    if check.masterClock - pipeFour.clockCycle:
        pipeFour.stalls += 1
    if check.masterClock - pipeFive.clockCycle:
        pipeFive.stalls += 1
    
    # Loop through pipes
    check.masterClock += 1
    if check.WBQueue:
        doPipe = check.WBQueue.pop(0)
        doPipe.clockCycle += 1
        write_to_reg(doPipe)
        if doPipe.stageName != "DONE":
            check.IFQueue.append(doPipe)
            doPipe.stageName = "IF"
    if check.MAQueue:
        doPipe = check.MAQueue.pop(0)
        doPipe.clockCycle += 1
        memory_addressing(doPipe)
        if doPipe.stageName != "DONE":
            check.IFQueue.append(doPipe)
            doPipe.stageName = "IF"
    if check.ALUQueue:
        doPipe = check.ALUQueue.pop(0)
        doPipe.clockCycle += 1
        opcode[doPipe.instr >> 4](doPipe)
        if (doPipe.instr >> 4) == 0x0 and doPipe.stageName != "DONE":      #COPY
            check.IFQueue.append(doPipe)
            doPipe.stageName = "IF"
        elif (doPipe.instr >> 4) == 0x2 and doPipe.stageName != "DONE":    #LOAD
            if doPipe.mem_reg:
                check.MAQueue.append(doPipe)
                doPipe.stageName = "MA"
            else:
                check.IFQueue.append(doPipe)
                doPipe.stageName = "IF"
        elif doPipe.stageName != "DONE":
            check.WBQueue.append(doPipe)
            doPipe.stageName = "WB"
    if check.RFQueue:
        doPipe = check.RFQueue.pop(0)
        doPipe.clockCycle += 1
        prog_mem = doPipe.reg_fetch(prog_mem)
        if (doPipe.instr >> 4) == 0x3 and doPipe.stageName != "DONE": # IN/OUT
            check.MAQueue.append(doPipe)
            doPipe.stageName = "MA"
        elif doPipe.stageName != "DONE":
            check.ALUQueue.append(doPipe)
            doPipe.stageName = "ALU"
    if not check.RFQueue and check.IFQueue:
        doPipe = check.IFQueue.pop(0)
        doPipe.clockCycle += 1
        prog_mem = doPipe.instr_fetch(prog_mem)
        if doPipe.stageName != "DONE":
            check.RFQueue.append(doPipe)
            doPipe.stageName = "RF"
    



if d['reg']:
    print("R0 is "+str(hex(r[0])))
    print("R1 is "+str(hex(r[1])))
    print("R2 is "+str(hex(r[2])))
    print("R3 is "+str(hex(r[3])))
if d['flag']:
    print(flag)
if d['stalls']:
    print("pipeOne   Stalls:\t"+str(pipeOne.stalls))
    print("pipeTwo   Stalls:\t"+str(pipeTwo.stalls))
    print("pipeThree Stalls:\t"+str(pipeThree.stalls))
    print("pipeFour  Stalls:\t"+str(pipeFour.stalls))
    print("pipeFive  Stalls:\t"+str(pipeFive.stalls))

                        
