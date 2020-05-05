'''
===============================================================================
#                                                                             #
#                        pCalc - Scientific Calculator                        #
#                                                                             #
===============================================================================

    Main functions:

        - Natural Order of Opeartions: Calculations can be input in the same
          form as they are written, the priority sequence of the input
          calculation will be evaluated automatically according to the
          operator precedence, eg. 1 + 2 x 3 = 7.
        - Equation Input Control Rules: advanced supervision mechanism
          introduced in order to minimize number of syntax errors.
        - Answer Memory (Ans): the last calculation result obtained is stored
          in Ans (answer) memory. You can scroll back through all the previous
          calculation results' by pressing Ans key.
        - Calculation Precision Setup:  The value you specify (from 1 to 5
          and FULL) controls the number of decimal places for displayed
          calculation results. Calculation results are rounded off to the
          specified digit before being displayed.
        - Engineering notation eg. 1.2 e+3 = 1.2 x 10^3 = 1200.

    Available operators:

        - basic arithmetic opertors:  addition, subtraction, multiplication
          and division
        - floor division operator (integral part of the division),
          eg. 5 // 3 = 1
        - modulus opeartor (remainder of the division), eg. 5 mod 3 = 2
        - exponenet operator (raises the left operand to the power of the
          right), eg. 2 ^ 3 = 8
        - roots: available using exponent operator, as 1/n exponent is equal
          to n-th root of the number, eg. 8 ^ (1/3) = 2
        - use of parenthesis: please note that input of the closing
          parenthesis is required
        - Pi number: being equal to 3.141592653
'''

import tkinter as tk
import tkinter.ttk as ttk         
import tkinter.messagebox


# pCalc Program Version Global Var
version = '1.5'

# Float Number Result Precision Var
floatPrecisionData = ('1', '2', '3', '4', '5', 'Full')
floatPrecision = 'Full'


def main():
    root = tk.Tk()
    pCalc(root)
    CreateMenu(root)
    root.mainloop()


class pCalc:

    def __init__(self, master):
        '''
        Bottom frame creation with all the digits and basic operators.
        '''
        self.master = master
        global version

        self.master.title('pCalc - v.' + version)
        master.resizable(1,0)
        self.extraButtons = [('Pi', 'x^y', '(', ')', '//', 'mod')]

        self.digitButtons = [('7', '8', '9',   'Del', 'AC'),
                             ('4', '5', '6',     '*',  '/'),
                             ('1', '2', '3',     '+',  '-'),
                             ('0', '.', 'EXP', 'Ans',  '=')]

        self.keyDic = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                       '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
                       '.': '.', '+': '+', '-': '-', '*': '*', '/': "<slash>", 
                       'EXP': "e", 'AC': "<Delete>", 'Del': "<BackSpace>",
                       '=': "<Return>", 'Ans': "<Up>"}
        self.Ans = []
        self.AnsCount = 0
        self.equalCount = 0

        self.displayWidget(master)
        self.extraFrameWidget(master)
        self.digitFrameWidget(master)
        self.imageFrameWidget(master)
      

    def displayWidget(self, master):
        
        self.displayVar = tk.StringVar()
        self.display = tk.Entry(master,
                                justify="right",
                                bd=5,
                                relief='sunken',
                                textvariable=self.displayVar,
                                state='readonly',
                                readonlybackground='dark sea green',
                                font=("Consolas 18 bold"))
        self.display.focus()
        self.displayVar.set('0')
        self.display.grid(column=0, row=1, padx=10, pady=10, sticky='nswe')
        master.grid_columnconfigure(0, weight=1)


    def extraFrameWidget(self, master):
        
        extraFrame = tk.Frame(master, padx=4)
        extraFrame.grid(column=0, row=5, padx=2, sticky='nswe')

        c = 0
        r = 0
        button = []
        for row in self.extraButtons:
            for key in row:
                b = tk.Button(extraFrame,
                              text=key,
                              font=("Biome 9 bold"),
                              bd=3,
                              width=1,
                              bg='grey40',
                              fg='white',
                              command=lambda k=key: self.displayFunc("", k))
                b.grid(column=c, row=r, padx=4, pady=4, sticky='nswe')
                c += 1
            c = 0
            r += 1
        master.bind('p', lambda event: self.displayFunc(event, 'Pi'))
        master.bind('P', lambda event: self.displayFunc(event, 'Pi'))
        master.bind('^', lambda event: self.displayFunc(event, 'x^y'))
        master.bind('(', lambda event: self.displayFunc(event, '('))
        master.bind(')', lambda event: self.displayFunc(event, ')'))
        master.bind('m', lambda event: self.displayFunc(event, 'mod'))
        master.bind('M', lambda event: self.displayFunc(event, 'mod'))
        '''
        For convenience extended list of events associated with pressed keys.
        '''
       
        # Even distribution of columns
        extraFrame.grid_columnconfigure(0, weight=1)
        extraFrame.grid_columnconfigure(1, weight=1)
        extraFrame.grid_columnconfigure(2, weight=1)
        extraFrame.grid_columnconfigure(3, weight=1)
        extraFrame.grid_columnconfigure(4, weight=1)
        extraFrame.grid_columnconfigure(5, weight=1)

    def digitFrameWidget(self, master):
        
        digitFrame = tk.Frame(master, padx=3, pady=3)
        digitFrame.grid(column=0, row=10, padx=2, pady=1, sticky='nswe')

        c = 0
        r = 0
        for row in self.digitButtons:
            for key in row:
                b = tk.Button(digitFrame,
                              text=key,
                              font = ("Biome 11 bold"),
                              bd=4, width=1,
                              bg='grey76',
                              command=lambda k=key: self.displayFunc("", k))
                b.grid(column=c, row=r, padx=4, pady=4, sticky='nswe')
                master.bind(self.keyDic[key],
                            lambda event, k=key: self.displayFunc(event, k))
                if key in ('Del', 'AC'):
                    b.config(bg='tomato')
                c += 1
            c = 0
            r += 1
        master.bind('=', lambda event: self.displayFunc(event, '='))
        master.bind('E', lambda event: self.displayFunc(event, 'EXP'))
        master.bind('x', lambda event: self.displayFunc(event, '*'))
        master.bind('X', lambda event: self.displayFunc(event, '*'))
        master.bind('a', lambda event: self.displayFunc(event, '+'))
        master.bind('A', lambda event: self.displayFunc(event, '+'))
        master.bind('s', lambda event: self.displayFunc(event, '-'))
        master.bind('S', lambda event: self.displayFunc(event, '-'))
        master.bind('<Escape>', lambda event: self.displayFunc(event, 'AC'))
        '''
        For convenience extended list of events associated with pressed keys.
        '''
        
        # Even distribution of columns
        digitFrame.grid_columnconfigure(0, weight=1)
        digitFrame.grid_columnconfigure(1, weight=1)
        digitFrame.grid_columnconfigure(2, weight=1)
        digitFrame.grid_columnconfigure(3, weight=1)
        digitFrame.grid_columnconfigure(4, weight=1)

    def imageFrameWidget(self, master):
        imageFrame = tk.Frame(master)
        imageFrame.grid(column=0, row=15, padx=2, pady=1, sticky='nswe')

        # Image 
        self.img_author = tk.PhotoImage(file="img/programoteq.100.png")
        self.img_Label = tk.Label(imageFrame, image=self.img_author)
        self.img_Label.grid(column=0, row=0, sticky='s', padx=2, pady=2)
        imageFrame.grid_columnconfigure(0, weight=1)

        # Sizegrip Widget
        ttk.Sizegrip(imageFrame).grid(column=1, row=0, sticky=('se'))

        
    def displayFunc(self, event, key):
        global floatPrecision
      
        if key != 'Ans':
            self.AnsCount = 0
        if key not in "123456789(" and key != 'Pi':
            self.equalCount = 0           
###
##        print('\nIN: self.displayVar.get(): ', self.displayVar.get())
##        print('<> self.AnsCount: ', self.AnsCount)
##        print(' + :key: ', key)
###
        if key == '=':
            try:
                toDisplayReplace = self.displayVar.get()\
                              .replace('^', '**')\
                              .replace('Pi', '3.141592653')\
                              .replace('mod', '%')
                toDisplayReplaceEval = eval(toDisplayReplace)
###
##                print('\n=: self.displayVar.get(): ', self.displayVar.get())
##                print('=: toDisplayReplace: ', toDisplayReplace)
##                print('=: toDisplayReplaceEval: ', toDisplayReplaceEval)
##                print('= floatPrecision: ', floatPrecision)
###
                if toDisplayReplaceEval == int(toDisplayReplaceEval):
                    self.displayVar.set(int(toDisplayReplaceEval))
                    self.Ans.insert(0, int(toDisplayReplaceEval))
                    self.equalCount += 1
                else:
                    if floatPrecision != 'Full':
                        toDisplayReplaceEval = \
                                f'{toDisplayReplaceEval:.{floatPrecision}f}'
                    self.displayVar.set(toDisplayReplaceEval)
                    self.Ans.insert(0, toDisplayReplaceEval)
                    self.equalCount += 1
###
##                print('=: self.Ans: ', self.Ans)
###
            except:
                temp = self.displayVar.get()
                self.displayVar.set('-ERROR-')
                root.after(600, lambda: self.displayVar.set(temp))
                
        elif key == 'Ans':           
            if self.AnsCount > 0:
                if self.AnsCount < len(self.Ans):
                    self.AnsCount += 1
                    lenPrev = len(str(self.Ans[self.AnsCount - 2]))
                    if len(self.displayVar.get()) \
                    == len(str(self.Ans[self.AnsCount - 2])):
                        self.displayVar.set(str(self.Ans[self.AnsCount - 1]))
                    elif len(self.displayVar.get()) \
                    > len(str(self.Ans[self.AnsCount - 2])):
                        self.displayVar.set(self.displayVar.get()[:-lenPrev]
                                            + str(self.Ans[self.AnsCount - 1]))                
###
##                    print('<> lenPrev: ', lenPrev)
##                    print('<> self.displayVar.get()[:-lenPrev]: ', self.displayVar.get()[:-lenPrev])
##                    print('<> + str(self.Ans[self.AnsCount - 1]): ', str(self.Ans[self.AnsCount - 1]))
###

            elif self.displayVar.get() == '0':
                if self.Ans:
                    self.AnsCount += 1
                    self.displayVar.set(self.Ans[0])
            elif self.displayVar.get()[-1] in '+-*^/d(':
                if self.Ans:
                    self.AnsCount += 1
                    self.displayVar.set(self.displayVar.get()
                                        + str(self.Ans[0]))

        elif key == 'AC':
            self.displayVar.set(0)

        elif key == 'Del':
            if self.displayVar.get()[-1] == 'd':
                self.displayVar.set(self.displayVar.get()[:-3])
            elif self.displayVar.get()[-1] == 'i':
                self.displayVar.set(self.displayVar.get()[:-2])
            else:
                self.displayVar.set(self.displayVar.get()[:-1])
            if not self.displayVar.get():
                self.displayVar.set('0')          

        elif key == 'EXP':
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + 'e+')
            elif self.displayVar.get()[-1] in '.':
                self.displayVar.set(self.displayVar.get()[:-1] + 'e+')

        elif key == '.':
            if self.displayVar.get() == '0':
                self.displayVar.set('0.')
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get() + '0.')
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) == 1:
                    self.displayVar.set(self.displayVar.get() + '0.')
                elif len(self.displayVar.get()) > 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get() + '0.')
            elif self.displayVar.get()[-1] in '*^/mod(':
                self.displayVar.set(self.displayVar.get() + '0.')
            elif self.displayVar.get()[-1] in "1234567890":
                self.displayVar.set(self.displayVar.get() + '.')

        elif key == '-':
            if self.displayVar.get() == '0':
                self.displayVar.set(key)
            elif self.displayVar.get()[-1] not in '.+-*^/mod':
                self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1:
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif len(self.displayVar.get()) == 1:
                    self.displayVar.set('0')
            elif self.displayVar.get()[-1] in '.+*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif self.displayVar.get()[-2] in '/':
                    self.displayVar.set(self.displayVar.get()[:-2] + key)
                elif self.displayVar.get()[-2] in 'mod':
                    self.displayVar.set(self.displayVar.get()[:-3] + key)

        elif key in '+':
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*^/mod':
                self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1:
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif len(self.displayVar.get()) == 1:
                    self.displayVar.set('0')
            elif self.displayVar.get()[-1] in '.+*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif self.displayVar.get()[-2] in '/':
                    self.displayVar.set(self.displayVar.get()[:-2] + key)
                elif self.displayVar.get()[-2] in 'mod':
                    self.displayVar.set(self.displayVar.get()[:-3] + key)

        elif key in '*/':
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] in '.*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif self.displayVar.get()[-2] in '/mod':
                    if self.displayVar.get()[-3] not in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-2] + key)
                    elif self.displayVar.get()[-3] in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-3] + key)

        elif key == '//':
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] in '.*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif self.displayVar.get()[-2] in '/mod':
                    if self.displayVar.get()[-3] not in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-2] + key)
                    elif self.displayVar.get()[-3] in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-3] + key)

        elif key == "mod":
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
            elif self.displayVar.get()[-1] in '.*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + key)
                elif self.displayVar.get()[-2] in '/mod':
                    if self.displayVar.get()[-3] not in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-2] + key)
                    elif self.displayVar.get()[-3] in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-3] + key)

        elif key == 'x^y':
            if self.displayVar.get() == '0' or self.displayVar.get()[-1] \
               not in '.+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + '^')
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + '^')
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) != 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get()[:-1] + '^')
            elif self.displayVar.get()[-1] in '.*^/mod':
                if self.displayVar.get()[-2] not in '/mod':
                    self.displayVar.set(self.displayVar.get()[:-1] + '^')
                elif self.displayVar.get()[-2] in '/mod':
                    if self.displayVar.get()[-3] not in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-2] + '^')
                    elif self.displayVar.get()[-3] in 'mod':
                        self.displayVar.set(self.displayVar.get()[:-3] + '^')
                        
        elif key == 'Pi':
            if self.displayVar.get() == '0':
                self.displayVar.set(key)
            elif self.equalCount != 0:
                self.displayVar.set(key)
                self.equalCount = 0
            elif self.displayVar.get()[-2:] == 'Pi':
                self.displayVar.set(self.displayVar.get()[:-2] + key)
            elif self.displayVar.get()[-1] == '+':
                if self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] == '-':
                if len(self.displayVar.get()) == 1:
                    self.displayVar.set(self.displayVar.get() + key)
                elif len(self.displayVar.get()) > 1 and \
                   self.displayVar.get()[-2] not in 'eE':
                    self.displayVar.set(self.displayVar.get() + key)
            elif self.displayVar.get()[-1] in '*/^mod(':
                self.displayVar.set(self.displayVar.get() + key)

        elif  key == "(":
            if self.displayVar.get() == '0':
                self.displayVar.set(key)
            elif self.equalCount != 0:
                self.displayVar.set(key)
                self.equalCount = 0
            elif self.displayVar.get()[-1] not in ".1234567890Pi":
                self.displayVar.set(self.displayVar.get() + key)

        elif key == ")":
            if self.displayVar.get() != '0' and self.displayVar.get()[-1] \
               not in '+-*/^mod(':
                self.displayVar.set(self.displayVar.get() + key)

        elif key in "1234567890":
            if self.displayVar.get() == '0':
                self.displayVar.set(key)
            elif self.equalCount != 0:
                self.displayVar.set(key)
                self.equalCount = 0
            else:
                self.displayVar.set(self.displayVar.get() + key)

#
        print('OUT: self.displayVar.get(): ', self.displayVar.get())
#


class CreateMenu:

    def __init__(self, master):
        self.master = master
        
        # Create Menubar 
        menubar = tk.Menu(master)

        # Options Menu
        optionsMenu = tk.Menu(menubar, tearoff=0)
        optionsMenu.add_command(label="About...", command=self.AboutMsg)
        optionsMenu.add_command(label="Precison Setup",
                                command=self.PrecisionFunc)
        optionsMenu.add_command(label="Shorcuts",
                                command=lambda: self.ManualMsg(""),
                                accelerator="F1")
        optionsMenu.add_separator()
        optionsMenu.add_command(label="Exit",
                                command=lambda: self.ExitMsg(""),
                                accelerator="Ctrl+Q")

        menubar.add_cascade(label="Ξ Options",  menu=optionsMenu)

        # Display Menubar
        master.config(menu=menubar)

        # Whole application shortcuts
        master.bind_all("<F1>", self.ManualMsg)
        master.bind_all("<Control-q>", self.ExitMsg)

        # Delete window protocol handler
        master.protocol("WM_DELETE_WINDOW", lambda: self.ExitMsg(""))
           
    def AboutMsg(self):
        global version
        self.aTop = tk.Toplevel()
        self.aTop.resizable(0,0)

        noteb = ttk.Notebook(self.aTop, padding=(5,1,5,5))
        notebF1 = ttk.Frame(noteb)   # first page, which would get widgets gridded into it
        notebF2 = ttk.Frame(noteb)   # second page
        noteb.add(notebF1, text='About')
        noteb.add(notebF2, text='Description')
        noteb.pack(fill='both')

        # ABOUT tab 
        aLabel = tk.Label(notebF1,
                          pady=10,
                          text=f"\n\npCalc",
                          font=("Biome 20 bold"))
        aLabel.pack(fill='both')

        aLabel = tk.Label(notebF1,
                          pady=10,
                          text=f"version: {version}\n",
                          font=("Biome 16"))
        aLabel.pack(fill='both')

        aBut = ttk.Button(notebF1,
                          text="Close",
                          command=self.aTop.destroy)
        aBut.pack(side='bottom', pady=10)

        self.img_author = tk.PhotoImage(file="img/programoteq.100.png")
        self.img_Label = tk.Label(notebF1, image=self.img_author)
        self.img_Label.pack(side='bottom', padx=2, pady=20)

        # DESCRIPTION tab 
        textbox = tk.Text(notebF2,
                          width=70,
                          height=28,
                          font=("Biome 10"),
                          wrap='word',
                          bg='grey95',
                          padx=5,
                          pady=5)
        textbox.pack()

        # Section 1
        textbox.insert(tk.END, "\nMain functions: ", ("h1"))
        textbox.insert(tk.END, "\n\n - Natural Order of Opeartions:", ("h2"))
        textbox.insert(tk.END, 
''' Calculations can be input in the same form as 
   they are written, the priority sequence of the input calculation will be \
evaluated
   automatically according to the operator precedence, eg. 1 + 2 x 3 = 7.
'''
                       )
        textbox.insert(tk.END, " - Equation Input Control Rules:", ("h2"))
        textbox.insert(tk.END, 
''' advanced supervision mechanism introduced in
   order to minimize number of syntax errors.
'''
                       )
        textbox.insert(tk.END, " - Answer Memory (Ans):", ("h2"))
        textbox.insert(tk.END, 
''' the last calculation result obtained is stored in Ans
   (answer) memory. You can scroll back through all the previous calculation \
results'
   by pressing Ans key.
'''
                       )
        textbox.insert(tk.END, " - Calculation Precision Setup:", ("h2"))
        textbox.insert(tk.END, 
''' The value you specify (from 1 to 5 and FULL)
   controls the number of decimal places for displayed calculation results.
   Calculation results are rounded off to the specified digit before being \
   displayed.
'''
                       )
        textbox.insert(tk.END, " - Engineering notation", ("h2"))
        textbox.insert(tk.END, 
''', eg. 1.2 e+3 = 1.2 x 10^3 = 1200.

'''
                       )

        # Section 2
        textbox.insert(tk.END, "Available operators: ", ("h1"))
        textbox.insert(tk.END, "\n\n - basic arithmetic opertors:", ("h2"))
        textbox.insert(tk.END, 
''' addition, subtraction, multiplication and division
'''
                       )
        textbox.insert(tk.END, " - floor division operator", ("h2"))
        textbox.insert(tk.END, 
''' (integral part of the division), eg. 5 // 3 = 1
'''
                       )
        textbox.insert(tk.END, " - modulus opeartor", ("h2"))
        textbox.insert(tk.END, 
''' (remainder of the division), eg. 5 mod 3 = 2
'''
                       )
        textbox.insert(tk.END, " - exponenet operator", ("h2"))
        textbox.insert(tk.END, 
''' (raises the left operand to the power of the right),
   eg. 2 ^ 3 = 8
'''
                       )
        textbox.insert(tk.END, " - roots:", ("h2"))
        textbox.insert(tk.END, 
''' available using exponent operator, as 1/n exponent is equal to
   n-th root of the number, eg. 8 ^ (1/3) = 2
'''
                       )
        textbox.insert(tk.END, " - use of parenthesis:", ("h2"))
        textbox.insert(tk.END, 
''' please note that input of the closing parenthesis is required
'''
                       )
        textbox.insert(tk.END, " - Pi number:", ("h2"))
        textbox.insert(tk.END, 
''' being equal to 3.141592653

'''
                       )

        textbox.tag_config("h1", font=("Biome 13 bold"))
        textbox.tag_config("h2", font=("Tahoma 10 bold"))
        textbox.config(state='disabled')

        aBut = ttk.Button(notebF2,
                          text="Close",
                          command=self.aTop.destroy)
        aBut.pack(side='bottom', pady=10)


    def PrecisionFunc(self):
        global floatPrecision
        global floatPrecisionData

        # Toplevel window
        self.pTop = tk.Toplevel()
        self.pTop.resizable(0,0)

        pLabel = tk.Label(self.pTop,
                          padx=12,
                          pady=12,
                          text="Calculation \nPrecision Setup",
                          font=("Biome 14"))
        pLabel.pack(fill='x')

        pMsg = tk.Message(self.pTop, font=("Biome 10"), text=
'''The value you specify (from 1 to 5 and FULL) controls the number of decimal \
places for displayed calculation results. Calculation results are rounded off \
to the specified digit before being displayed.

The default precision is set to: 'Full'.

Currently precision is set to:'''
                            )
        pMsg.pack(fill='x')

        self.pCombo = ttk.Combobox(self.pTop,
                               width=15,
                               font=("Biome 10"),
                               state='readonly',
                               values=floatPrecisionData)
        self.pCombo.current(floatPrecisionData.index(floatPrecision))
        self.pCombo.focus()
        self.pCombo.pack(pady=10)

        self.pComboB = ttk.Button(self.pTop,
                                 text="Set Precision",
                                 command=self.pCombFunc)
        self.pComboB.pack(pady=15)

    def pCombFunc(self):
        global floatPrecision
###
##        print('floatPrecision in: ', floatPrecision, type(floatPrecision))
###
        floatPrecision = self.pCombo.get()
###
##        print('floatPrecision out:', floatPrecision, type(floatPrecision))
###
        self.pTop.destroy()


    def ManualMsg(self, event):
        global version
        tkinter.messagebox.showinfo(f"\npCalc v.{version}", 
"""
Keyboard shortcuts:                     

0 - 9                                     digits

.                                           period

+, a, A                                 addition operator

-, s, S                                   subtraction operator

*, x, X                                   multiplication operator

/, d, D                                   division operators

=, <Enter>                          =

<Delete>, <Escape>          AC

<BackSpace>                      Del


e, E                                       EXP

p, P                                       Pi

m, M                                     mod

^                                          exponentiation

( )                                          parenthesis

<Up Arrow>                        Ans

""")

    def ExitMsg(self, event):
        global version
        if tkinter.messagebox.askokcancel(f"\npCalc v.{version}",
                                          "Do you really want to Exit?",
                                          default='cancel'):
            self.master.destroy()

            
if __name__ == "__main__":
    main()
    
