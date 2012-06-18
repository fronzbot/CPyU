from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

instructions = {0x0:"cpy", 0x1:"swp", 0x20:"ld", 0x22:"ld.i", 0x23:"st", 0x31:"in", 0x30:"out",
                0x4:"add", 0x5:"sub", 0x6:"and", 0xB:"ceq", 0x8:"clt", 0xA:"not", 0xD:"mul",
                0xE:"div", 0x90:"shla", 0x91:"shll", 0x92:"shra", 0x93:"shrl", 0xC0:"jmp",
                0xC1:"br", 0xCF:"call", 0x70:"ret", 0x71:"reti"}

class CPU_Canvas(Canvas):
    def __init__(self, parent, width, height, background):
        Canvas.__init__(self, parent, width=width, height=height, background=background, borderwidth=4, relief='groove')
        self.parent     = parent
        self.background = background
        self.pipeOne    = Visual_Pipe(self.parent, self, (75, 25,  125, 75),  "P1", 'DeepSkyBlue3')
        self.pipeTwo    = Visual_Pipe(self.parent, self, (75, 115, 125, 165), "P2", 'DarkOliveGreen4')
        self.pipeThree  = Visual_Pipe(self.parent, self, (75, 205, 125, 255), "P3", 'DarkGoldenRod4')
        self.pipeFour   = Visual_Pipe(self.parent, self, (75, 295, 125, 345), "P4", 'DarkOrange3')
        self.pipeFive   = Visual_Pipe(self.parent, self, (75, 385, 125, 435), "P5", 'dark magenta')
        self.create_line(545, 0, 545, height)
        self.progMem    = Visual_Memory(self.parent, self, 256, 585, "PM")
        self.dataMem    = Visual_Memory(self.parent, self, 256, 800, "DM")

        # Pipe Current Instructions
        self.create_text(60, 480, text="P1 Instr:", fill='DeepSkyBlue3', font=('Helvetica 14 bold'))
        self.create_text(60, 505, text="P2 Instr:", fill='DarkOliveGreen4', font=('Helvetica 14 bold'))
        self.create_text(60, 530, text="P3 Instr:", fill='DarkGoldenRod4', font=('Helvetica 14 bold'))
        self.create_text(60, 555, text="P4 Instr:", fill='DarkOrange3', font=('Helvetica 14 bold'))
        self.create_text(60, 580, text="P5 Instr:", fill='dark magenta', font=('Helvetica 14 bold'))

        self.p1_instr = self.create_text(120, 480, text="-", fill='blue', font=('Helvetica 14 bold'), anchor=W)
        self.p2_instr = self.create_text(120, 505, text="-", fill='blue', font=('Helvetica 14 bold'), anchor=W)
        self.p3_instr = self.create_text(120, 530, text="-", fill='blue', font=('Helvetica 14 bold'), anchor=W)
        self.p4_instr = self.create_text(120, 555, text="-", fill='blue', font=('Helvetica 14 bold'), anchor=W)
        self.p5_instr = self.create_text(120, 580, text="-", fill='blue', font=('Helvetica 14 bold'), anchor=W)
        
        # Registers
        self.create_text(585, 545, text="R0:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(585, 575, text="R1:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(670, 545, text="R2:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(670, 575, text="R3:", fill='black', font=('Helvetica 14 bold'))
        self.r0 = Register(self, 615, 545)
        self.r1 = Register(self, 615, 575)
        self.r2 = Register(self, 700, 545)
        self.r3 = Register(self, 700, 575)
        
        # Flags
        self.create_text(800, 545, text="C:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(800, 575, text="N:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(860, 545, text="V:", fill='black', font=('Helvetica 14 bold'))
        self.create_text(860, 575, text="Z:", fill='black', font=('Helvetica 14 bold'))
        self.C_flag = Flag(self, 820, 545)
        self.N_flag = Flag(self, 820, 575)
        self.V_flag = Flag(self, 880, 545)
        self.Z_flag = Flag(self, 880, 575)

    def get_instr_name(self, pipe, instr):
        if instr == 0x0:
            self.itemconfig(pipe, text="-")
            return
        
        MSB = (instr >> 4)
        LSB = (instr & 0xF)
        if MSB in (0x2, 0x3, 0x7, 0x9, 0xC):
            if MSB == 0xC:
                if LSB not in (0x0, 0xF):
                    select = 0x1
                else:
                    select = LSB & 0x3
            elif MSB == 0x7:
                select = LSB >> 3
            else:
                select = LSB & 0x3
                
            MSB = (MSB<<4) | select
            
        self.itemconfig(pipe, text=instructions[MSB])


class Register(object):
    '''Class for Register output'''
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x      = x
        self.y      = y
        self.val    = self.canvas.create_text(x, y, text="00", fill='ForestGreen', font=('Helvetica 14 bold'))

    def update(self, new_val):
        try:
            new_val = new_val[0].capitalize()+new_val[1].capitalize()
        except IndexError:
            new_val = '0'+new_val[0].capitalize()
        self.canvas.itemconfig(self.val, text=new_val)



class Flag(object):
    '''Class for Flag output'''
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x      = x
        self.y      = y
        self.val    = self.canvas.create_text(x, y, text="0", fill='maroon4', font=('Helvetica 14 bold'))

    def update(self, new_val):
        self.canvas.itemconfig(self.val, text=new_val)


        
class Visual_Pipe(object):
    '''Class for visual pipeline'''
    def __init__(self, parent, canvas, pos, tag, color):
        self.parent     = parent
        self.canvas     = canvas
        self.pos        = pos
        self.width      = pos[2]-pos[0]
        self.height     = pos[3]-pos[1]
        self.color      = color
        self.tag        = tag
        self.currStage  = 0

        x = self.width  + 40

        # Boxes
        self.IF_box  = self.canvas.create_rectangle(pos[0],     pos[1], pos[2],     pos[3], width=2, tag=(tag, "IF"))
        self.RF_box  = self.canvas.create_rectangle(pos[0]+x,   pos[1], pos[2]+x,   pos[3], width=2, tag=(tag, "RF"))
        self.ALU_box = self.canvas.create_rectangle(pos[0]+x*2, pos[1], pos[2]+x*2, pos[3], width=2, tag=(tag, "ALU"))
        self.MA_box  = self.canvas.create_rectangle(pos[0]+x*3, pos[1], pos[2]+x*3, pos[3], width=2, tag=(tag, "MA"))
        self.WB_box  = self.canvas.create_rectangle(pos[0]+x*4, pos[1], pos[2]+x*4, pos[3], width=2, tag=(tag, "WB"))

        self.boxes = {"IF": self.IF_box, "RF": self.RF_box, "ALU": self.ALU_box,
                      "MA": self.MA_box, "WB": self.WB_box}

        # Text
        self.canvas.create_text(30, pos[1]+self.height/2, text=tag+": ", fill=color, font=('Helvetica 14 bold'))
        self.canvas.create_text(pos[0]+25,     pos[1]+self.height/2, text="IF",  font=('Helvetica 10 bold'))
        self.canvas.create_text(pos[0]+25+x,   pos[1]+self.height/2, text="RF",  font=('Helvetica 10 bold'))
        self.canvas.create_text(pos[0]+25+x*2, pos[1]+self.height/2, text="ALU", font=('Helvetica 10 bold'))
        self.canvas.create_text(pos[0]+25+x*3, pos[1]+self.height/2, text="MA",  font=('Helvetica 10 bold'))
        self.canvas.create_text(pos[0]+25+x*4, pos[1]+self.height/2, text="WB",  font=('Helvetica 10 bold'))
        
        # Wires
        center = pos[1]+self.height/2
        self.canvas.create_line(50,         center, pos[0],     center)
        self.canvas.create_line(pos[2],     center, pos[0]+x,   center)
        self.canvas.create_line(pos[2]+x,   center, pos[0]+x*2, center)
        self.canvas.create_line(pos[2]+x*2, center, pos[0]+x*3, center)
        self.canvas.create_line(pos[2]+x*3, center, pos[0]+x*4, center)
        self.canvas.create_line(pos[2]+x*4, center, pos[0]+x*5, center)

        # RF Feed Forward to MA
        self.canvas.create_line((pos[2]+x+pos[0]+x*2)/2,   center,    (pos[2]+x+pos[0]+x*2)/2,     center-32)    # RF  | ALU
        self.canvas.create_line((pos[0]+x*3+20),           pos[1],    (pos[0]+x*3+20),             center-32)    # >MA
        self.canvas.create_line((pos[2]+x+pos[0]+x*2)/2,   center-32, (pos[0]+x*3+20)+1,           center-32)    # Bridge

        # ALU Feed Forward to WB
        self.canvas.create_line((pos[2]+x*2+pos[0]+x*3)/2, center,    (pos[2]+x*2+pos[0]+x*3)/2,   center-40)    # ALU | MA
        self.canvas.create_line((pos[0]+x*4+20),           pos[1],    (pos[0]+x*4+20),             center-40)    # >WB
        self.canvas.create_line((pos[2]+x*2+pos[0]+x*3)/2, center-40, (pos[0]+x*4+20)+1,           center-40)    # Bridge

        # ALU Feed Back to IF
        self.canvas.create_line((50+pos[0])/2,             center,    (50+pos[0])/2,               center+35)    #  -- | IF
        self.canvas.create_line((pos[2]+x*2+pos[0]+x*3)/2, center,    (pos[2]+x*2+pos[0]+x*3)/2,   center+35)    # ALU | MA
        self.canvas.create_line((50+pos[0])/2,             center+35, (pos[2]+x*2+pos[0]+x*3)/2+1, center+35)    # Bridge

        # MA Feed Back to IF
        self.canvas.create_line((pos[2]+x*3+pos[0]+x*4)/2, center,    (pos[2]+x*3+pos[0]+x*4)/2,   center+35)    # MA | WB
        self.canvas.create_line((pos[2]+x*2+pos[0]+x*3)/2, center+35, (pos[2]+x*3+pos[0]+x*4)/2+1, center+35)    # Bridge

        # WB Feed Back to IF
        self.canvas.create_line((pos[2]+x*4+pos[0]+x*5)/2, center,    (pos[2]+x*4+pos[0]+x*5)/2,   center+35)    # MA | WB
        self.canvas.create_line((pos[2]+x*3+pos[0]+x*4)/2, center+35, (pos[2]+x*4+pos[0]+x*5)/2+1, center+35)    # Bridge

        # Directional Arrows on wires
        self.canvas.create_polygon(pos[0]-5,     center-5, pos[0],     center, pos[0]-5,     center+5)
        self.canvas.create_polygon(pos[0]+x-5,   center-5, pos[0]+x,   center, pos[0]+x-5,   center+5)
        self.canvas.create_polygon(pos[0]+x*2-5, center-5, pos[0]+x*2, center, pos[0]+x*2-5, center+5)
        self.canvas.create_polygon(pos[0]+x*3-5, center-5, pos[0]+x*3, center, pos[0]+x*3-5, center+5)
        self.canvas.create_polygon(pos[0]+x*4-5, center-5, pos[0]+x*4, center, pos[0]+x*4-5, center+5)

        # Directional Arrows on feedthrough
        self.canvas.create_polygon((pos[2]+x+pos[0]+x*2)/2-5,   center-11, (pos[2]+x+pos[0]+x*2)/2,         # RF ->  MA
                                   center-17, (pos[2]+x+pos[0]+x*2)/2+5, center-12)
        self.canvas.create_polygon((pos[2]+x*2+pos[0]+x*3)/2-5, center-11, (pos[2]+x*2+pos[0]+x*3)/2,       # ALU -> WB
                                   center-17, (pos[2]+x*2+pos[0]+x*3)/2+5, center-12)
        self.canvas.create_polygon(pos[0]+x*3+16, pos[1]-4, pos[0]+x*3+24, pos[1]-4, pos[0]+x*3+20, pos[1]) # -> MA
        self.canvas.create_polygon(pos[0]+x*4+16, pos[1]-4, pos[0]+x*4+24, pos[1]-4, pos[0]+x*4+20, pos[1]) # -> WB

        self.canvas.create_polygon((50+pos[0])/2, center+11, (50+pos[0])/2+5, center+17, (50+pos[0])/2-5, center+17)  # IF <-
        self.canvas.create_polygon((pos[2]+x*2+pos[0]+x*3)/2-5, center+11, (pos[2]+x*2+pos[0]+x*3)/2,       # IF <- ALU
                                   center+17, (pos[2]+x*2+pos[0]+x*3)/2+5, center+12)
        self.canvas.create_polygon((pos[2]+x*3+pos[0]+x*4)/2-5, center+11, (pos[2]+x*3+pos[0]+x*4)/2,       # IF <- MA
                                   center+17, (pos[2]+x*3+pos[0]+x*4)/2+5, center+12)
        self.canvas.create_polygon((pos[2]+x*4+pos[0]+x*5)/2-5, center+11, (pos[2]+x*4+pos[0]+x*5)/2,       # IF <- WB
                                   center+17, (pos[2]+x*4+pos[0]+x*5)/2+5, center+12)
        
        # Nodes
        self.canvas.create_oval((50+pos[0])/2-2, center-2, (50+pos[0])/2+2, center+2, fill='black') # o->IF
        self.canvas.create_oval((pos[2]+x+pos[0]+x*2)/2-2, center-2, (pos[2]+x+pos[0]+x*2)/2+2, center+2, fill='black') # RF-o-ALU
        self.canvas.create_oval((pos[2]+x*2+pos[0]+x*3)/2-2, center-2, (pos[2]+x*2+pos[0]+x*3)/2+2, center+2, fill='black') # ALU-o-MA
        self.canvas.create_oval((pos[2]+x*3+pos[0]+x*4)/2-2, center-2, (pos[2]+x*3+pos[0]+x*4)/2+2, center+2, fill='black') # MA-o-WB
        self.canvas.create_oval((pos[2]+x*4+pos[0]+x*5)/2-2, center-2, (pos[2]+x*4+pos[0]+x*5)/2+2, center+2, fill='black') # WB-o-

    def update(self, new_stage):
        if self.currStage:
            self.canvas.itemconfig(self.currStage, fill=self.canvas.background)

        if new_stage != "DONE":
            self.currStage = self.boxes[new_stage]
            self.canvas.itemconfig(self.currStage, fill=self.color)

class Visual_Memory(object):
    def __init__(self, parent, canvas, mem_size, x_start, name):
        self.parent   = parent
        self.canvas   = canvas
        self.mem_size = mem_size
        self.x_start  = x_start
        self.name     = name
        self.array = []
        self.canvas.create_text(self.x_start+75, 25, text=name, font=('Helvetica 10 bold'))
        y = 50
        x = self.x_start
        for i in range(0, mem_size):
            val = hex(i)[2:]
            if len(val) < 2:
                val = "0"+val[0]
            val = val[0].capitalize()+val[1].capitalize()
            if x == self.x_start:
                self.canvas.create_text(x-20, y, text=val+"|", font=('Helvetica 8 underline bold'), fill='grey45')
            self.array.append(self.canvas.create_text(x, y, tag=(name, str(i)), text="00", font=('Helvetica 8 normal'), fill='SkyBlue4'))
            x += 20

            if (i+1) % 8 == 0:
                y += 15
                x -= 160
 
    def update(self, new_val, mem_loc):
        self.canvas.itemconfig(self.array[mem_loc], text=new_val)
        


    












        

        
