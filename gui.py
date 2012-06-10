from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import keyword
from string import ascii_letters, digits, punctuation
import re, os
import Assembler

cmds = ['cpy', 'swap', 'ld',  'st',  'in',  'out', 'add', 'sub',
        'and', 'ceq', 'clt', 'not', 'mul', 'div', 'shla', 'shll',
        'shra', 'shrl', 'jmp', 'br', 'call', 'ret', 'reti', 'nop']

class TextEditor(Text):
    tags = {'COMMAND': ('blue',   'Consolas 12 bold'  ),
            'HEXNUM' : ('orange', 'Consolas 12 normal'),
            'COMMENT': ('ForestGreen', 'Consolas 12 normal'),
            'INT'    : ('red', 'Consolas 12 bold')
           }
    
    def __init__(self, parent):
        Text.__init__(self, parent, undo=True)
        self.pack(side=LEFT, expand=YES, fill=BOTH)
        self.yScrollbar = Scrollbar(parent, orient=VERTICAL, command=self.yview)
        self['yscrollcommand'] = self.yScrollbar.set
        self.yScrollbar.pack(side=RIGHT, fill=Y)
        self.configure(font='Consolas 12 normal', width=40, height=25)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation
        self.colorComment = False
        self.commentStart = 0
        self.lastLine = 1
        self.bind('<Any-KeyRelease>', self.key_press)
        self.compiler = Assembler.Assembler()


    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val[0], font=val[1])

    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)


    def key_press(self, key):
        linenum = self.index(INSERT).split('.')[0]
        lastcol = 0
        if self.lastLine != linenum:
            self.colorComment = False
        self.lastLine = linenum
            
        char = self.get('%s.%d'%(linenum, lastcol))
        
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(linenum, lastcol))
        buffer = self.get('%s.%d'%(linenum,0),'%s.%d'%(linenum,lastcol))
        tokenized = buffer.split(' ')
      
        self.remove_tags('%s.%d'%(linenum, 0), '%s.%d'%(linenum, lastcol))

        start, end = 0, 0
        for token in tokenized:
            end = start + len(token)                
            if token in cmds:
                self.tag_add('COMMAND', '%s.%d'%(linenum, start), '%s.%d'%(linenum, end))
            elif len(token) >= 2 and token[0:2] == '0x':
                self.tag_add('HEXNUM', '%s.%d'%(linenum, start), '%s.%d'%(linenum, end))
                
            for letter in token:
                if letter == ';':
                    self.colorComment = True
                    self.commentStart = start + token.index(letter)
                    self.remove_tags('%s.%d'%(linenum, self.commentStart), '%s.%d'%(linenum, end))
                   
            if self.colorComment:
                self.remove_tags('%s.%d'%(linenum, self.commentStart), '%s.%d'%(linenum, end))
                self.tag_add('COMMENT', '%s.%d'%(linenum, self.commentStart), '%s.%d'%(linenum, end))

            start += len(token)+1
        
    def highlight(self, line, linenum):
        start = 0
        colorComment = False
        commentStart = 0
        line = re.sub(r"\n", "", line).split(" ")

        for token in line:
            end = start + len(token)
            if token in cmds:
                self.tag_add('COMMAND', '%s.%d'%(linenum, start), '%s.%d'%(linenum, end))
                
            elif len(token) >= 2 and token[0:2] == '0x':
                self.tag_add('HEXNUM', '%s.%d'%(linenum, start), '%s.%d'%(linenum, end))
                
            for letter in token:
                if letter == ';':
                    colorComment = True
                    commentStart = start + token.index(letter)
                    self.remove_tags('%s.%d'%(linenum, commentStart), '%s.%d'%(linenum, end))
                   
            if colorComment:
                self.remove_tags('%s.%d'%(linenum, commentStart), '%s.%d'%(linenum, end))
                self.tag_add('COMMENT', '%s.%d'%(linenum, commentStart), '%s.%d'%(linenum, end))

            start += len(token)+1
            
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
                self.delete('0.0', END)
                for line in data:
                    self.insert(END, line)
                    num += 1
                    self.highlight(line, num)

            except IOError:
                messagebox.showerror(parent=self, icon='error', default='ok', message='Read File Error',
                                     detail='File cannot be read.  Check to make sure that the file is not open in another program and try again')    
    
            
    def saveAsm(*args):
        pass
        
def compileAsm(*args):
    data = app.asmEditor.get('0.0', END)
    f = open('tmp.asm', 'w')
    f.write(data)
    f.close()
    app.asmEditor.compiler.compiler('tmp.asm')
    if os.name == 'posix':
        os.sysem('rm tmp.asm')
    else:
        os.system('del tmp.asm')
    f = open('out.a')
    code = f.readlines()
    f.close()
    lineNum = 1
    app.mcEditor.delete('0.0', END)
    app.mcEditor.configure(foreground='red3', font=('Consolas 12 normal'), state=NORMAL)
    for line in code:
        app.mcEditor.insert(END, line)
        lineNum += 1
    app.mcEditor.configure(state=DISABLED)



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

        # Text Editor creation
        self.asmEditor = TextEditor(self.asmframe)
        self.mcEditor  = TextEditor(self.mcframe)
        self.mcEditor.configure(state=DISABLED)

        # Buttons
        self.compileBtn = ttk.Button(self.buttonframe, text="Compile", width=8, command=compileAsm)
        self.saveBtn    = ttk.Button(self.buttonframe, text="Save",    width=8, command=self.asmEditor.saveAsm)
        self.loadBtn    = ttk.Button(self.buttonframe, text="Load",    width=8, command=self.asmEditor.loadAsm)

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
        
        

if __name__ == "__main__":
    app = App(None)
    app.title("CPyU - A Python CPU Simulator")
    app.mainloop()