hexLookup = {'0':0, '1':1, '2':2, '3':3, '4':4,
             '5':5, '6':6, '7':7, '8':8, '9':9,
             'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

class Pipeline(object):
    def __init__(self):
        self.instr      = 0
        self.dst_reg    = 0
        self.src_reg    = 0
        self.val_reg    = 0
        self.alu_reg    = 0
        self.dm_reg     = 0
        self.select     = 0
        self.currStage  = 0
        self.stageName  = ""

    def get_byte(self, val):
        high = hexLookup[val[0]] << 4
        low  = hexLookup[val[1]]
        return high|low

    def instr_fetch(self, mem):
        self.currStage += 1
        self.stageName = "IF"
        self.instr = self.get_byte(mem.pop())
        return mem

    def reg_fetch(self, mem):
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
