#!/usr/bin/python                                    
import queue

# Each position stores 2 Bytes, therefore
# This works out to 256 Bytes
prog_mem = queue.Queue(128)
data_mem = queue.LifoQueue(128)

r0 = 0
r1 = 0
r2 = 0
r3 = 0

hexLookup = {'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}


def mov(val, loc):
        new_val = parse_value([val])[0]
        store(new_val, loc)   

def add(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1+new_val2, loc)

def sub(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1-new_val2, loc)

def land(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1&new_val2, loc)

def lor(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1|new_val2, loc)

def lnot(val, loc):
        new_val = parse_value([val])[0]
        store(~new_val, loc)    

def xor(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1^new_val2, loc)

def shl(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1<<new_val2, loc)

def shr(val1, val2, loc):
        [new_val1, new_val2] = parse_value([val1, val2])
        store(new_val1>>new_val2, loc)

        
instructions = {'01':mov, '02':add, '03':sub, '04':land,
                '05':lor, '06':lnot, '07':xor, '08':shl,
                '09':shr}


def store(val, loc):
        
        if loc == "E0":
                r0 = val
        elif loc == "E8":
                r1 = val
        elif loc == "F0":
                r2 = val
        elif loc == "F8":
                r3 = val
        else:
                print ("Invalid location "+str(loc))
                
def parse_value(valList):
        multiplier = [16, 1]
        bitVal = [[0,0],[0,0]]
        
        for i in range(0, len(valList)):
                temp = list(valList[i])
                
                try:
                        bitVal[i][0] = int(hexLookup[temp[0]])*16
                except KeyError:
                        bitVal[i][0] = int(temp[0])*16
                try:
                        bitVal[i][1] = int(hexLookup[temp[1]])
                except KeyError:
                        bitVal[i][1] = int(temp[1])

        val1 = bitVal[0][0] + bitVal[0][1]
        val2 = bitVal[1][0] + bitVal[1][1]
        return [val1, val2]
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
                        prog_mem.put(instr)
        mc.close()
		

'''
Main code
'''
get_machine_code('machine.a')

while not prog_mem.empty():
        todo = prog_mem.get()
        
        if todo == '01' or todo == '06':
                try:
                        val = prog_mem.get()
                        loc = prog_mem.get()
                        instructions[todo](val, loc)
                except KeyError:
                        print("Instruction "+str(todo)+"not found!")
        else:
                try:
                        val1 = prog_mem.get()
                        val2 = prog_mem.get()
                        loc = prog_mem.get()
                        instructions[todo](val1, val2, loc)
                except KeyError:
                        print("Instruction "+str(todo)+"not found!")

                        
