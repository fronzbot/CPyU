
def memory_addressing(pipe, memory):

    if (pipe.instr >> 4) == 0x2: # ld/st
        if pipe.select == 0x3:
            memory.data[pipe.mem_reg] = memory.r[pipe.dst_reg]
        elif pipe.select == 0x2:
            memory.r[pipe.dst_reg] = memory.data[pipe.mem_reg]
          
    elif (pipe.instr >> 4) == 0x3: # in/out
        if pipe.select == 0x0:  # Out
            memory.io[pipe.val_reg] = memory.r[pipe.dst_reg]
        elif pipe.select == 0x1:    # In
            memory.r[pipe.dst_reg] = memory.io[pipe.val_reg]
       
    memory.check_if_finished(pipe)
    

def write_to_reg(pipe, memory):

    if pipe.instr >> 4 == 0x1:  #SWAP
        memory.r[pipe.src_reg] = memory.r[pipe.dst_reg]
        
    memory.r[pipe.dst_reg] = pipe.alu_reg
    
    memory.check_if_finished(pipe)

            
def cpy(pipe, memory):
    memory.r[pipe.dst_reg] = memory.r[pipe.src_reg]
    
def swp(pipe, memory):
    pipe.alu_reg = memory.r[pipe.src_reg]

def ld(pipe, memory):
    # Store
    if pipe.select == 0x3:
        pipe.mem_reg = memory.r[(pipe.val_reg & 0xC0) >> 6] + (pipe.val_reg & 0x3F)
    
    # Load Displacement
    elif pipe.select == 0x2:
        pipe.mem_reg = memory.r[(pipe.val_reg & 0xC0)>>6] + (pipe.val_reg & 0x3F)
                
    # Load Immediate
    else:
        memory.r[pipe.dst_reg] = pipe.val_reg
        memory.check_if_finished(pipe)


def add(pipe, memory):
    pipe.alu_reg = memory.r[pipe.dst_reg] + memory.r[pipe.src_reg]
    if pipe.alu_reg > 0xFF:
        pipe.alu_reg = 0xFF
        memory.flag["C"] ^= 1
        
def sub(pipe, memory):
    pipe.alu_reg = memory.r[pipe.dst_reg] - memory.r[pipe.src_reg]
    if pipe.alu_reg < 0:
        pipe.alu_reg = -1*pipe.alu_reg
        memory.flag["N"]^=1

def and_op(pipe, memory):
    pipe.alu_reg = memory.r[pipe.dst_reg] & memory.r[pipe.src_reg]

def ret():
    pass

def clt():
    pass

def shift(pipe, memory):
    pipe.clockCycle += 1
    #Arithmetic left shift
    if pipe.select == 0x0:
        pipe.alu_reg = memory.r[pipe.dst_reg] << 1
        if (pipe.alu_reg & 0x180) == 0x180:
            pipe.alu_reg &= 0xFF
            memory.flag["V"] ^= 1
            
    #Logical Left Shift        
    elif pipe.select == 0x1:
        pipe.alu_reg = memory.r[pipe.dst_reg] << 1

    #Arithmetic Right Shift
    elif pipe.select == 0x2:
        pipe.alu_reg = memory.r[pipe.dst_reg] >> 1
        if memory.r[pipe.dst_reg] & 0x80 == 0x80:
            pipe.alu_reg |= 0x80

    #Logical Right Shift        
    elif pipe.select == 0x3:
        pipe.alu_reg = memory.r[pipe.dst_reg] >> 1

def not_op(pipe, memory):
    pipe.alu_reg = ~memory.r[pipe.dst_reg]&0xFF
    

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
