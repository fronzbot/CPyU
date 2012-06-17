#!/usr/bin/env python                                    
from packages.architecture import pipeline
from packages.architecture import Instructions
import time
import argparse
import gui

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
        
pause = 0
def main():
    global pause
    '''Main CPU Architecture'''
    mem   = Memory()
        
    pipes = Pipes() 
    check = pipeline.Controller()
    check.pipes = [pipes.pipeOne, pipes.pipeTwo, pipes.pipeThree, pipes.pipeFour, pipes.pipeFive]
    
    get_machine_code('hex/out.a', mem)

    pipes.start_pipes(check)

    # Update Pipe Stages
    app.canvas.pipeOne.update(pipes.pipeOne.stageName)
    app.canvas.pipeTwo.update(pipes.pipeTwo.stageName)
    app.canvas.pipeThree.update(pipes.pipeThree.stageName)
    app.canvas.pipeFour.update(pipes.pipeFour.stageName)
    app.canvas.pipeFive.update(pipes.pipeFive.stageName)
    
    # Update Program Memory on screen
    i = 0
    mem.prog.reverse()
    for val in mem.prog:
        app.canvas.progMem.update(val, i)
        i += 1
    mem.prog.reverse()

    app.update()
    
    while mem.prog:
        time.sleep(1)
        
        if mem.prog[-1] == "00":
            if pipes.done(check):
                break

        while pause:
            app.update()
            
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

        '''
        # Check stalls
        pipes.check_stalls(check)
        
        # Loop through pipes
        # This is where all the CPU logic is
        check.masterClock += 1

        # Perform instruction in Write-Back Queue
        if check.WBQueue:
            doPipe = check.WBQueue.pop(0)
            doPipe.clockCycle += 1
            Instructions.write_to_reg(doPipe, mem)  # Write to the register
            if doPipe.stageName != "DONE":
                check.IFQueue.append(doPipe)    # Send to Instruction-Fetch Queue
                doPipe.stageName = "IF"

        # Perform instruction in Memory-Write/Read Queue        
        if check.MAQueue:
            doPipe = check.MAQueue.pop(0)
            doPipe.clockCycle += 1
            Instructions.memory_addressing(doPipe, mem) # Write/Read from Memory
            if doPipe.stageName != "DONE":
                check.IFQueue.append(doPipe)            # Send to Instruction-Fetch Queue
                doPipe.stageName = "IF"

        # Perform instruction in ALU Queue    
        if check.ALUQueue:
            doPipe = check.ALUQueue.pop(0)
            doPipe.clockCycle += 1
            opcode[doPipe.instr >> 4](doPipe, mem)
            if (doPipe.instr >> 4) == 0x0 and doPipe.stageName != "DONE":   # If the instruction is to copy
                check.IFQueue.append(doPipe)                                # Send to Instruction-Fetch Queue
                doPipe.stageName = "IF"
            elif (doPipe.instr >> 4) == 0x2 and doPipe.stageName != "DONE": # If the instruction is to load
                if doPipe.mem_reg:                                          # if there is a memory address
                    check.MAQueue.append(doPipe)                            # Send to Memory Write/Read queue
                    doPipe.stageName = "MA"
                else:
                    check.IFQueue.append(doPipe)                            # Otherwise send to Instruction-Fetch Queue
                    doPipe.stageName = "IF"
            elif doPipe.stageName != "DONE":                                # If instruction is complete    
                check.WBQueue.append(doPipe)                                # Send to Write-Back Queue
                doPipe.stageName = "WB"

        # Perform instruction in Register-Fetch Queue
        if check.RFQueue:
            doPipe = check.RFQueue.pop(0)
            doPipe.clockCycle += 1
            mem.prog = doPipe.reg_fetch(mem.prog)
            if (doPipe.instr >> 4) == 0x3 and doPipe.stageName != "DONE":   # If the instruction is IN or OUT
                check.MAQueue.append(doPipe)                                # Send to Memory Write/Read Queue
                doPipe.stageName = "MA"
            elif doPipe.stageName != "DONE":                                # Otherise if instruction is complete
                check.ALUQueue.append(doPipe)                               # Send to ALU Queue
                doPipe.stageName = "ALU"

        # Check if nothing in Register-Fetch and Instruction-Fetch has at least one instruction
        if not check.RFQueue and check.IFQueue:                             
            doPipe = check.IFQueue.pop(0)               # Do instruction and send to Register-Fetch Queue
            doPipe.clockCycle += 1
            mem.prog = doPipe.instr_fetch(mem.prog)
            if doPipe.stageName != "DONE":
                check.RFQueue.append(doPipe)
                doPipe.stageName = "RF"

        
        # Update screen every clock cycle
        '''Pipe Stage Update'''
        app.canvas.pipeOne.update(pipes.pipeOne.stageName)
        app.canvas.pipeTwo.update(pipes.pipeTwo.stageName)
        app.canvas.pipeThree.update(pipes.pipeThree.stageName)
        app.canvas.pipeFour.update(pipes.pipeFour.stageName)
        app.canvas.pipeFive.update(pipes.pipeFive.stageName)
        
        '''Register Update'''
        app.canvas.r0.update(hex(mem.r[0])[2:])
        app.canvas.r1.update(hex(mem.r[1])[2:])
        app.canvas.r2.update(hex(mem.r[2])[2:])
        app.canvas.r3.update(hex(mem.r[3])[2:])

        '''Flag Update'''
        app.canvas.C_flag.update(str(mem.flag['C']))
        app.canvas.N_flag.update(str(mem.flag['N']))
        app.canvas.V_flag.update(str(mem.flag['V']))
        app.canvas.Z_flag.update(str(mem.flag['Z']))
        
        app.update()


    # Update screen when program finished
    app.canvas.r0.update(hex(mem.r[0])[2:])
    app.canvas.r1.update(hex(mem.r[1])[2:])
    app.canvas.r2.update(hex(mem.r[2])[2:])
    app.canvas.r3.update(hex(mem.r[3])[2:])
    app.canvas.C_flag.update(str(mem.flag['C']))
    app.canvas.N_flag.update(str(mem.flag['N']))
    app.canvas.V_flag.update(str(mem.flag['V']))
    app.canvas.Z_flag.update(str(mem.flag['Z']))
    app.update()

def pause_sim():
    global pause
    pause = 1
    app.runBtn.configure(command=run_sim)

def run_sim():
    global pause
    pause = 0
    app.runBtn.configure(command=main)

if __name__ == '__main__':
    app = gui.App(None)
    app.title("CPyU - A Python CPU Simulator")
    app.runBtn.configure(command=main)
    app.pauseBtn.configure(command=pause_sim)
    app.mainloop()
