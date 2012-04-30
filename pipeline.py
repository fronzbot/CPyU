hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

stages = ["IF", "RF", "ALU", "WB"]

class Controller(object):
    def __init__(self):
        self.pipes = []

    def clear_for_stage(self, pipeToCheck, stage):
        prevStage = stages[stages.index(stage)-1]
        for pipe in self.pipes:
            if pipe == pipeToCheck:
                next
            if pipe.stageName == stage or pipeToCheck.stageName != prevStage:
                return False
        
        return True

    def stage_pos(self, pipeToCheck):
        for pipe in self.pipes:
            if pipe == pipeToCheck:
                next
            if pipeToCheck.currStage > pipe.currStage or pipeToCheck.stageName == "DONE":
                return False

        return True

    
class Pipeline(object):
    '''Class defines a pipeline for processor use'''
    def __init__(self):
        self.instr      = 0         # Instruction -> 8 bits
        self.dst_reg    = 0         # Destination register name (int)
        self.src_reg    = 0         # Source register name (int)
        self.val_reg    = 0         # Value for 2 byte Instruction Words
        self.alu_reg    = 0         # Value output of ALU ops
        self.select     = 0         # Selction bits for certain instructions
        self.currStage  = 0         # Current stage number
        self.stageName  = ""        # Current stage name

    def get_byte(self, val):
        '''Converts hex string to int'''
        high = hexLookup[val[0]] << 4
        low  = hexLookup[val[1]]
        return high|low

    def instr_fetch(self, mem):
        '''Retrieves instruction from memory'''
        self.currStage += 1
        self.stageName = "IF"
        self.instr = self.get_byte(mem.pop())
        if self.instr == 0x0:
            self.stageName = "DONE"
        return mem

    def reg_fetch(self, mem):
        '''Parses instruction word for registers and selection bits'''
        self.currStage += 1
        self.stageName = "RF"
        op = self.instr >> 4
        # ld immediate, ld displacement, st; in, out
        if op == 0x2 or op == 0x3:
            self.val_reg = self.get_byte(mem.pop())
            if op == 0x3:
                pass
            elif op == 0x2:
                self.select = (self.instr & 0x3)
                if (self.instr & 0x1):
                    self.src_reg = (self.instr & 0xC) >> 2
                else:
                    self.dst_reg = (self.instr & 0xC) >> 2
    
        # jmp, br, call
        elif op == 0xC:
            pass
        
        # shla, shll, shra, shrl
        elif op == 0x9:
            self.dst_reg = (self.instr & 0xC) >> 2
            self.select = (self.instr & 0x3)
    
        # ret, reti
        elif op == 0x7:
            self.dst_reg = (self.instr & 0x3)
            self.select = (self.instr & 0xC) >> 2

        # everything else
        else:
            self.dst_reg  = (self.instr & 0xC) >> 2
            self.src_reg  = (self.instr & 0x3)
        
        return mem
