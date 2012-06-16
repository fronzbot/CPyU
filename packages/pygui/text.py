from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import keyword
from string import ascii_letters, digits, punctuation
import re, os

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
        self.configure(font='Consolas 12 normal', width=30, height=2)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation
        self.colorComment = False
        self.commentStart = 0
        self.lastLine = 1
        self.bind('<Any-KeyRelease>', self.key_press)


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
                elif letter == ',':
                    commaLoc = start + token.index(letter)
                    self.remove_tags('%s.%d'%(linenum, commaLoc), '%s.%d'%(linenum, commaLoc+1))
                   
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
            
    
        
