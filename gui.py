from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from packages.pygui import text
from packages.pygui import box
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
        self.buttonframe = ttk.Frame(self.parent)
        self.assembler   = Assembler.Assembler()

        # Text Editor creation
        self.asmEditor = text.TextEditor(self.asmframe)
        self.mcEditor  = text.TextEditor(self.mcframe)
        self.mcEditor.configure(state=DISABLED)

        # Button Images
        loadImg         = PhotoImage(file='img/load.gif')
        saveImg         = PhotoImage(file='img/save.gif')
        settingsImg     = PhotoImage(file='img/settings.gif')
        undoImg         = PhotoImage(file='img/undo.gif')
        compileImg      = PhotoImage(file='img/compile.gif')
        runImg          = PhotoImage(file='img/run.gif')
        pauseImg        = PhotoImage(file='img/pause.gif')
        stopImg         = PhotoImage(file='img/stop.gif')
        nextImg         = PhotoImage(file='img/next.gif')
        
        
        # Buttons
        self.loadBtn     = ttk.Button(self.buttonframe, image=loadImg,    command=self.loadAsm)
        self.saveBtn     = ttk.Button(self.buttonframe, image=saveImg,    command=self.saveAsm)
        self.settingsBtn = ttk.Button(self.buttonframe, image=settingsImg)
        self.undoBtn     = ttk.Button(self.buttonframe, image=undoImg)
        self.compileBtn  = ttk.Button(self.buttonframe, image=compileImg, command=self.compileAsm)
        self.runBtn      = ttk.Button(self.buttonframe, image=runImg)
        self.pauseBtn    = ttk.Button(self.buttonframe, image=pauseImg)
        self.stopBtn     = ttk.Button(self.buttonframe, image=stopImg)
        self.nextBtn     = ttk.Button(self.buttonframe, image=nextImg)
        self.loadBtn.image     = loadImg
        self.saveBtn.image     = saveImg
        self.settingsBtn.image = settingsImg
        self.undoBtn.image     = undoImg
        self.compileBtn.image  = compileImg
        self.runBtn.image      = runImg
        self.pauseBtn.image    = pauseImg
        self.stopBtn.image     = stopImg
        self.nextBtn.image     = nextImg
        

        # Canvas
        self.canvas = box.CPU_Canvas(self.leftframe, 950, 600, 'white')
        
        # Pack elements
        self.buttonframe.pack(side=TOP, fill=X, anchor=N, pady=2, padx=10)
        ttk.Separator(orient=HORIZONTAL).pack(side=TOP, fill=X, anchor=N, pady=4)
        self.mainframe.pack(expand=YES, fill=BOTH)
        self.mainframe.add(self.leftframe)
        self.mainframe.add(self.rightframe)

        
        self.canvas.pack(fill=BOTH)
        self.editorframe.pack(side=TOP, fill=X)
        self.editorframe.add(self.asmframe, text='Assembly')
        self.editorframe.add(self.mcframe,  text='Machine Code')
        self.loadBtn.pack(side=LEFT, pady=2, anchor=N)
        self.saveBtn.pack(side=LEFT, pady=2, anchor=N)
        self.settingsBtn.pack(side=LEFT, pady=2, anchor=N)
        self.undoBtn.pack(side=LEFT, pady=2, anchor=N)
        ttk.Separator(self.buttonframe, orient=VERTICAL).pack(side=LEFT, fill=Y, anchor=N, pady=2, padx=5)
        self.compileBtn.pack(side=LEFT, pady=2, anchor=N)
        self.runBtn.pack(side=LEFT, pady=2, anchor=N)
        self.pauseBtn.pack(side=LEFT, pady=2, anchor=N)
        self.stopBtn.pack(side=LEFT, pady=2, anchor=N)
        self.nextBtn.pack(side=LEFT, pady=2, anchor=N)
        
        
        

        
    def compileAsm(self):
        data = self.asmEditor.get('0.0', END)
        f = open('asm/tmp.asm', 'w')
        f.write(data)
        f.close()
        self.assembler.compiler('asm/tmp.asm')
        if os.name == 'posix':
            os.system('rm asm/tmp.asm')
        else:
            os.system('del asm/tmp.asm')
        f = open('hex/out.a')
        code = f.readlines()
        f.close()
        lineNum = 1
        self.mcEditor.configure(state=NORMAL)
        self.mcEditor.delete('0.0', END)
        self.mcEditor.configure(foreground='red3', font=('Consolas 12 normal'))
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
        

#if __name__ == "__main__":
#    app = App(None)
#    app.title("CPyU - A Python CPU Simulator")
#    app.mainloop()
