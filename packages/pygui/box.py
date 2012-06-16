from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class CPU_Canvas(Canvas):
    def __init__(self, parent, width, height, background):
        Canvas.__init__(self, parent, width=width, height=height, background=background, borderwidth=4, relief='groove')
        self.parent    = parent
        self.pipeOne   = Visual_Pipe(self.parent, self, (75, 25,  125, 75),  "P1")
        self.pipeTwo   = Visual_Pipe(self.parent, self, (75, 115, 125, 165), "P2")
        self.pipeThree = Visual_Pipe(self.parent, self, (75, 205, 125, 255), "P3")
        self.pipeFour  = Visual_Pipe(self.parent, self, (75, 295, 125, 345), "P4")
        self.pipeFive  = Visual_Pipe(self.parent, self, (75, 385, 125, 435), "P5")


        
class Visual_Pipe(object):
    def __init__(self, parent, canvas, pos, tag):
        self.parent  = parent
        self.canvas  = canvas
        self.pos     = pos
        self.width   = pos[2]-pos[0]
        self.height  = pos[3]-pos[1]

        x = self.width  + 40

        # Boxes
        self.IF_box  = self.canvas.create_rectangle(pos[0],     pos[1], pos[2],     pos[3], width=2, tag=(tag, "IF"))
        self.RF_box  = self.canvas.create_rectangle(pos[0]+x,   pos[1], pos[2]+x,   pos[3], width=2, tag=(tag, "RF"))
        self.ALU_box = self.canvas.create_rectangle(pos[0]+x*2, pos[1], pos[2]+x*2, pos[3], width=2, tag=(tag, "ALU"))
        self.MA_box  = self.canvas.create_rectangle(pos[0]+x*3, pos[1], pos[2]+x*3, pos[3], width=2, tag=(tag, "MA"))
        self.WB_box  = self.canvas.create_rectangle(pos[0]+x*4, pos[1], pos[2]+x*4, pos[3], width=2, tag=(tag, "WB"))

        # Text
        self.canvas.create_text(30, pos[1]+self.height/2, text=tag+": ", fill='navy', font=('Helvetica 14 bold'))
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





















        

        
