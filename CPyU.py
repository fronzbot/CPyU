#!/usr/bin/env python                                    
import pipeline
import time
import argparse
import Instructions

hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}


opcode = {0:Instructions.cpy, 1:Instructions.swp, 2:Instructions.ld, 4:Instructions.add, 5:Instructions.sub,
          6:Instructions.and_op, 7:Instructions.ret, 8:Instructions.clt, 9:Instructions.shift, 10:Instructions.not_op,
          11:Instructions.ceq, 12:Instructions.jump_call_br, 13:Instructions.mul, 14:Instructions.div,
          15:Instructions.nop}

class Memory(object):
    '''Memory Class for registers and stacks'''
    def __init__(self):
        self.r = [0, 0, 0, 0]
        self.prog = []
        self.data = []
        self.io   = []
        self.flag = {"C":0, "V":0, "Z":0, "N":0}

    def check_if_finished(self, pipe):
        if self.prog[-1] == "00":
            pipe.stageName = "DONE"

class Pipes(object):
    '''Handles pipe objects which are defined in pipeline.py'''
    def __init__(self):
        # Create pipelines
        self.pipeOne   = pipeline.Pipeline()
        self.pipeTwo   = pipeline.Pipeline()
        self.pipeThree = pipeline.Pipeline()
        self.pipeFour  = pipeline.Pipeline()
        self.pipeFive  = pipeline.Pipeline()

        # Initialize pipes
        self.pipeTwo.clockCycle      = 1
        self.pipeTwo.stalls          = 1
        self.pipeThree.clockCycle    = 1
        self.pipeThree.stalls        = 1
        self.pipeFour.clockCycle     = 1
        self.pipeFour.stalls         = 1
        self.pipeFive.clockCycle     = 1
        self.pipeFive.stalls         = 1

    def start_pipes(self, controller):
        controller.IFQueue.append(self.pipeOne)
        controller.IFQueue.append(self.pipeTwo)
        controller.IFQueue.append(self.pipeThree)
        controller.IFQueue.append(self.pipeFour)
        controller.IFQueue.append(self.pipeFive)

        self.pipeOne.stageName   = "IF"
        self.pipeTwo.stageName   = "IF"
        self.pipeThree.stageName = "IF"
        self.pipeFour.stageName  = "IF"
        self.pipeFive.stageName  = "IF"

    def done(self, controller):
        if self.pipeOne.stageName != "DONE":
            return False
        else:
             controller.clear_pipe(self.pipeOne)  
        if self.pipeTwo.stageName != "DONE":
            return False
        else:
            controller.clear_pipe(self.pipeTwo)  
        if self.pipeThree.stageName != "DONE":
            return False
        else:
            controller.clear_pipe(self.pipeThree) 
        if self.pipeFour.stageName != "DONE":
            return False
        else:
            controller.clear_pipe(self.pipeFour)
        if self.pipeFive.stageName != "DONE":
            return False
        else:
            controller.clear_pipe(self.pipeFive)

        return True

    def check_stalls(self, controller):
        if controller.masterClock - self.pipeOne.clockCycle:
            self.pipeOne.stalls += 1
        if controller.masterClock - self.pipeTwo.clockCycle:
            self.pipeTwo.stalls += 1
        if controller.masterClock - self.pipeThree.clockCycle:
            self.pipeThree.stalls += 1
        if controller.masterClock - self.pipeFour.clockCycle:
            self.pipeFour.stalls += 1
        if controller.masterClock - self.pipeFive.clockCycle:
            self.pipeFive.stalls += 1
        
            
def get_machine_code(filename, memory):
    '''Parse machine code and store in program memory'''
    mc = open(filename, 'r')
    while True:
        line = mc.readline()
        if not line:
            break
        instruction = line.rstrip().split(' ')
        for instr in instruction:
            memory.prog.append(instr)
            memory.data.append(0x0)
    mc.close()
    if len(memory.prog) > 256:
        print("Error: program memory exceeded!")
        exit(1)
        
    for i in range(len(memory.prog), 256):
        memory.prog.append("00")
        memory.data.append(0x0)
        memory.io.append(0x0)

    # Flips memory so top of stack is at end of list
    memory.prog.reverse()
        

def main():
    '''Main CPU Architecture'''
    mem   = Memory()
    pipes = Pipes() 
    check = pipeline.Controller()
    check.pipes = [pipes.pipeOne, pipes.pipeTwo, pipes.pipeThree, pipes.pipeFour, pipes.pipeFive]
    
    get_machine_code('out.a', mem)

    pipes.start_pipes(check)
    
    while mem.prog:
        if mem.prog[-1] == "00":
            if pipes.done(check):
                break
            
        #if pipeOne.stageName == "DONE":
        #    check.clear_pipe(pipeOne)
        #if pipeTwo.stageName == "DONE":
        #    check.clear_pipe(pipeTwo)
        #if pipeThree.stageName == "DONE":
        #    check.clear_pipe(pipeThree)
        #if pipeFour.stageName == "DONE":
        #    check.clear_pipe(pipeFour)
        #if pipeFive.stageName == "DONE":
        #    check.clear_pipe(pipeFive)
        '''
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
        '''
        # Check stalls
        pipes.check_stalls(check)
        
        # Loop through pipes
        # This is where all the CPU logic is
        check.masterClock += 1
        if check.WBQueue:
            doPipe = check.WBQueue.pop(0)
            doPipe.clockCycle += 1
            Instructions.write_to_reg(doPipe, mem)
            if doPipe.stageName != "DONE":
                check.IFQueue.append(doPipe)
                doPipe.stageName = "IF"
        if check.MAQueue:
            doPipe = check.MAQueue.pop(0)
            doPipe.clockCycle += 1
            Instructions.memory_addressing(doPipe, mem)
            if doPipe.stageName != "DONE":
                check.IFQueue.append(doPipe)
                doPipe.stageName = "IF"
        if check.ALUQueue:
            doPipe = check.ALUQueue.pop(0)
            doPipe.clockCycle += 1
            opcode[doPipe.instr >> 4](doPipe, mem)
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
            mem.prog = doPipe.reg_fetch(mem.prog)
            if (doPipe.instr >> 4) == 0x3 and doPipe.stageName != "DONE": # IN/OUT
                check.MAQueue.append(doPipe)
                doPipe.stageName = "MA"
            elif doPipe.stageName != "DONE":
                check.ALUQueue.append(doPipe)
                doPipe.stageName = "ALU"
        if not check.RFQueue and check.IFQueue:
            doPipe = check.IFQueue.pop(0)
            doPipe.clockCycle += 1
            mem.prog = doPipe.instr_fetch(mem.prog)
            if doPipe.stageName != "DONE":
                check.RFQueue.append(doPipe)
                doPipe.stageName = "RF"
        
    print("R0 is "+str(hex(mem.r[0])))
    print("R1 is "+str(hex(mem.r[1])))
    print("R2 is "+str(hex(mem.r[2])))
    print("R3 is "+str(hex(mem.r[3])))

'''
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
'''
if __name__ == '__main__':
    main()
