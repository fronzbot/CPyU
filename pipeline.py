hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

stages = ["IF", "RF", "ALU", "WB"]
def cpy():
    pass

def swp():
    pass

def ld(pipe, r, prog_mem):
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

def add(pipe, r, prog_mem):
    pipe.currStage += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] + r[pipe.src_reg]
        
def sub(pipe, r, prog_mem):
    pipe.currStage += 1
    pipe.stageName = "ALU"
    pipe.alu_reg = r[pipe.dst_reg] - r[pipe.src_reg]

def and_op(pipe, r, prog_mem):
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


def write_to_reg(pipe, r):
    pipe.currStage += 1
    pipe.stageName = "WB"
    r[pipe.dst_reg] = pipe.alu_reg
    if prog_mem[-1] == "00":
            pipe.stageName = "DONE"

            
def pipe_data(pipe, control, mem, registers, num):
    for otherPipe in control.pipes:
        if otherPipe == pipe:
            if control.stage_pos(pipe):
                if control.clear_for_stage(pipe, "IF") or pipe.stageName == "":
                    mem = pipe.instr_fetch(mem)
                elif control.clear_for_stage(pipe, "RF"):
                    mem = pipe.reg_fetch(mem)
                elif control.clear_for_stage(pipe, "ALU"):
                    opcode[pipe.instr >> 4](pipe, registers, mem)
                elif control.clear_for_stage(pipe, "WB"):
                    write_to_reg(pipe, registers)
        else:
            if otherPipe.stageName == "DONE" or otherPipe.stageName == "":
                otherPipe.currStage += 1
    
    return [mem, registers]

class Controller(object):
    def __init__(self):
        self.pipes = []
        self.ifClocked  = False
        self.rfClocked  = False
        self.aluClocked = False
        self.wbClocked  = False

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

    def next_stage(self, stage):
        if stage == "IF" and not self.ifClocked:
            return True
        elif stage == "RF" and not self.rfClocked:
            return True
        elif stage == "ALU" and not self.aluClocked:
            return True
        elif stage == "WB" and not self.wbClocked:
            return True
        else:
            return False
    
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
