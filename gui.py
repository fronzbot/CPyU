from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from packages.pygui import text
import keyword
from string import ascii_letters, digits, punctuation
import re, os
import Assembler


class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Frame setup
        self.mainframe   = ttk.PanedWindow(self.parent, orient=HORIZONTAL)
        self.leftframe   = ttk.Labelframe(self.parent, text='CPU Visualizer', relief='groove')
        self.rightframe  = ttk.Labelframe(self.parent, text='ASM/Machine Code Editor', relief='sunken')
        self.editorframe = ttk.Notebook(self.rightframe)
        self.asmframe    = ttk.Frame(self.editorframe)
        self.mcframe     = ttk.Frame(self.editorframe)
        self.buttonframe = ttk.Frame(self.rightframe, padding="3 3 12 12")
        self.assembler   = Assembler.Assembler()

        # Text Editor creation
        self.asmEditor = text.TextEditor(self.asmframe)
        self.mcEditor  = text.TextEditor(self.mcframe)
        self.mcEditor.configure(state=DISABLED)

        # Buttons
        self.compileBtn = ttk.Button(self.buttonframe, text="Compile", width=8, command=self.compileAsm)
        self.saveBtn    = ttk.Button(self.buttonframe, text="Save",    width=8, command=self.saveAsm)
        self.loadBtn    = ttk.Button(self.buttonframe, text="Load",    width=8, command=self.loadAsm)

        # Canvas
        self.canvas = Canvas(self.leftframe, width=640, height=480, borderwidth=4, relief='ridge')
        
        # Pack elements
        self.mainframe.pack(expand=YES, fill=BOTH)
        self.mainframe.add(self.leftframe)
        self.mainframe.add(self.rightframe)
        self.canvas.pack(fill=BOTH)
        self.editorframe.pack(side=TOP, fill=X)
        self.editorframe.add(self.asmframe, text='Assembly')
        self.editorframe.add(self.mcframe,  text='Machine Code')
        self.buttonframe.pack(side=BOTTOM, fill=X)
        self.compileBtn.grid(column=0, row=0, padx=5)
        self.saveBtn.grid(column=1, row=0, padx=5)
        self.loadBtn.grid(column=2, row=0, padx=5)

    def compileAsm(self):
        data = self.asmEditor.get('0.0', END)
        f = open('asm/tmp.asm', 'w')
        f.write(data)
        f.close()
        self.assembler.compiler('asm/tmp.asm')
        if os.name == 'posix':
            os.sysem('rm asm/tmp.asm')
        else:
            os.system('del asm/tmp.asm')
        f = open('hex/out.a')
        code = f.readlines()
        f.close()
        lineNum = 1
        self.mcEditor.delete('0.0', END)
        self.mcEditor.configure(foreground='red3', font=('Consolas 12 normal'), state=NORMAL)
        for line in code:
            self.mcEditor.insert(END, line)
            lineNum += 1
        self.mcEditor.configure(state=DISABLED)
    
    def loadAsm(self):
        types = [('Assembly Source', '.asm'),('All Files', '.*')]
        file  = filedialog.askopenfilename(initialdir='asm', filetypes=types)
        if not file:
            pass
        elif file[-4:] != '.asm':
            messagebox.showerror(parent=self, icon='error', default='ok', message='File Type Error',
                                 detail='File cannot be loaded.  Must be .asm!')
        else:
            try:
                f = open(file, 'r')
                data = f.readlines()
                f.close()
                num = 0
                self.asmEditor.delete('0.0', END)
                for line in data:
                    self.asmEditor.insert(END, line)
                    num += 1
                    self.asmEditor.highlight(line, num)

            except IOError:
                messagebox.showerror(parent=self, icon='error', default='ok', message='Read File Error',
                                     detail='File cannot be read.  Check to make sure that the file is not open in another program and try again')    
    
            
    def saveAsm(*args):
        pass
        

if __name__ == "__main__":
    app = App(None)
    app.title("CPyU - A Python CPU Simulator")
    app.mainloop()
