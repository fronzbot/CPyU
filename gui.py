from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import keyword
from string import ascii_letters, digits, punctuation
cmds = ['cpy', 'swp', 'ld',  'st',  'in',  'out', 'add', 'sub',
        'and', 'ceq', 'clt', 'not', 'mul', 'div', 'shla', 'shll',
        'shra', 'shrl', 'jmp', 'br', 'call', 'ret', 'reti', 'nop']

class TextEditor(Text):
    tags = {'kw':  ('blue', 'Consolas 12 bold'),
            'hex': ('orange', 'Consolas 12 normal'),
            'int': ('purple', 'Consolas 12 normal')
            }
    
    def __init__(self, root):
        Text.__init__(self, root)
        self.grid(column=0, row=0)
        self.yScrollbar = Scrollbar(root, orient=VERTICAL, command=self.yview)
        self['yscrollcommand'] = self.yScrollbar.set
        self.yScrollbar.grid(column=1, row=0, stick=(N,S))
        self.configure(font='Consolas 12 normal', width=40, height=25)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation
        self.checkHex = False
        self.bind('<Key>', self.key_press)

    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val[0], font=val[1])

    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)

    def key_press(self, key):
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(cline, lastcol))

        buffer = self.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = buffer.split(' ')

        self.remove_tags('%s.%d'%(cline, 0), '%s.%d'%(cline, lastcol))

        start, end = 0, 0
        for token in tokenized:
            end = start + len(token)                
            if token in cmds:
                self.tag_add('kw', '%s.%d'%(cline, start), '%s.%d'%(cline, end))
            else:
                for index in range(len(token)):
                    try:
                        if token[index] == "x":
                            self.checkHex = True
                        if token[index-1] == "0" and self.checkHex:
                            self.tag_add('hex', '%s.%d'%(cline, start-2), '%s.%d'%(cline, end))
                        else:
                            self.checkHex = False
                            try:
                                hex(int(token[index],16))
                            except ValueError:
                                pass
                            else:
                               self.tag_add('int', '%s.%d'%(cline, start+index)) 
                    except ValueError:
                        pass
                        

            
  
            start += len(token)+1
          
def compileAsm(*args):
    print('Compiling')

def saveAsm(*args):
    print("Saving")

def loadAsm(*args):
    print("Loading")

        
root = Tk()
root.wm_title("CPyU - A Python CPU Simulator")
root.columnconfigure(0, weight=1)

# Frame Setup
mainframe   = ttk.Frame(root, padding="3 3 12 12")
mainframe.pack()

rightframe  = ttk.Frame(mainframe, padding="3 3 12 12", relief='sunken')
leftframe   = ttk.Frame(mainframe, padding="3 3 12 12", relief='groove')
textframe   = ttk.Notebook(rightframe)
asmframe    = ttk.Frame(textframe)
mcframe     = ttk.Frame(textframe)
textframe.add(asmframe, text="Assembly")
textframe.add(mcframe,  text="Machine Code")
buttonframe = ttk.Frame(rightframe, padding="3 3 12 12")
visualframe = Canvas(leftframe, width=640, height=480, bg='white')


rightframe.grid(row=0, column=1)
leftframe.grid(row=0, column=0)
visualframe.grid(row=0, column=0)
textframe.grid(row=0, column=0)
buttonframe.grid(row=1, column=0)

# Text Editor
asmEditor = TextEditor(asmframe)
mcEditor  = TextEditor(mcframe)



# Buttons
compileBtn = ttk.Button(buttonframe, text="Compile", width=8, command=compileAsm)
saveBtn    = ttk.Button(buttonframe, text="Save",    width=8, command=saveAsm)
loadBtn    = ttk.Button(buttonframe, text="Load",    width=8, command=loadAsm)

compileBtn.grid(row=0, column=0)
saveBtn.grid(row=0, column=1)
loadBtn.grid(row=0, column=2)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
