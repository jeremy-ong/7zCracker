"""
7z Password Cracker for Linux
Author: Jeremy Ong
Last updated: 2016-05-23
Must have p7zip-full installed to work
Tested on Python 3.4 and 2.7
"""

#get the modules. module names changed in Python 3
try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
import subprocess
import threading

#set ttk theme
s=Style()
s.theme_use('alt')

#call the permutate() function until password length > 8, set widget states to normal when done
def doTheThing():
    for baseWidth in range(1, 9):
        permutate(baseWidth, 0, '')
    main.statusVar.set('Ready')
    main.txtFile['state'] = 'normal'
    main.btnGetFile['state'] = 'normal'
    main.txtFile['state'] = 'normal'
    main.rdoSelect['state'] = 'normal'
    main.rdoCustom['state'] = 'normal'
    main.txtChars['state'] = 'normal'
    if main.charsetVar.get() == 1:
        main.cboNumeric['state'] = 'normal'
        main.cboUpper['state'] = 'normal'
        main.cboLower['state'] = 'normal'
        main.cboSpecial['state'] = 'normal'

#call 7z command to check password without extracting, check stdout and set output message accordingly
def check(password):
    p = subprocess.Popen(['7z', 'x', '-p'+password, '-aos', main.txtFile.get()], stdout=subprocess.PIPE)
    output = str(p.stdout.read())
    if not re.search('Wrong password', output):
        main.stopThis = True
        main.btnStart['state'] = 'normal'

    if re.search('Wrong password', output):
        main.statusVar.set('Checking:')
        main.outputVar.set(password)
    elif re.search('Everything is Ok', output):
        main.outputVar.set('Password found: ' + password)
    elif re.search('Can not open file as archive', output):
        main.outputVar.set('Invalid file type')
    elif re.search('there is no such archive', output):
        main.outputVar.set('File does not exist')
    else:
        main.outputVar.set('Unknown error')
        print(output)

#iterate through each character permutation, unless stopThis variable is True
def permutate(length, position, base):
    for character in main.characters:
        if main.stopThis == True:
            return
        if (position < length - 1):
            permutate(length, position + 1, base + character)
        if len(base) + 1 == length:
            check(base + character)


class Main(Frame):
    def run(self):
        characterInput = self.txtChars.get()
        self.characters = sorted(list(set(characterInput)))
        if self.filename == '':
            self.outputVar.set('Select a file')
            return
        self.btnStart['state'] = 'disabled'
        self.btnGetFile['state'] = 'disabled'
        self.txtFile['state'] = 'readonly'
        self.rdoSelect['state'] = 'disabled'
        self.rdoCustom['state'] = 'disabled'
        self.txtChars['state'] = 'readonly'
        self.cboNumeric['state'] = 'disabled'
        self.cboUpper['state'] = 'disabled'
        self.cboLower['state'] = 'disabled'
        self.cboSpecial['state'] = 'disabled'
        self.stopThis = False
        thread = threading.Thread(target=doTheThing)
        thread.start()

    def stop(self):
        self.stopThis = True
        self.btnStart['state'] = 'normal'
        self.statusVar.set('Ready')

    def getFileName(self):
        self.filename = filedialog.askopenfilename()
        self.txtFile.delete(0, END)
        self.txtFile.insert(END, self.filename)
        self.outputVar.set('')

    def selectionChange(self):
        if self.charsetVar.get() == 1:
            self.txtChars.delete(0, END)
            if self.checkVarNumeric.get():
                self.txtChars.insert(END, '0123456789')
            if self.checkVarUpper.get():
                self.txtChars.insert(END, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if self.checkVarLower.get():
                self.txtChars.insert(END, 'abcdefghijklmnopqrstuvqxyz')
            if self.checkVarSpecial.get():
                self.txtChars.insert(END, '`~!@#$%^&*()-_=+[{]}\|;:\'", <.>/?')
            self.cboNumeric['state'] = 'normal'
            self.cboUpper['state'] = 'normal'
            self.cboLower['state'] = 'normal'
            self.cboSpecial['state'] = 'normal'
            self.charsetVar.set(1)
        elif self.charsetVar.get() == 2:
            self.cboNumeric['state'] = 'disabled'
            self.cboUpper['state'] = 'disabled'
            self.cboLower['state'] = 'disabled'
            self.cboSpecial['state'] = 'disabled'

    def customBox(self):
        self.charsetVar.set(2)
        self.selectionChange()
        return True

    def createWidgets(self):
        lblFile = Label(self, text='Select a file:')
        lblFile.grid(row=0, column=0, columnspan=2, sticky=W)

        self.txtFile = Entry(self, width=60)
        self.txtFile.grid(row=1, column=1, columnspan=3)

        self.btnGetFile = Button(self, text='Browse...', command=self.getFileName)
        self.btnGetFile.grid(row=1, column=4)

        self.charsetVar = IntVar()

        self.rdoSelect = Radiobutton(self, text='Select from:', variable=self.charsetVar, value=1, command=self.selectionChange)
        self.rdoSelect.grid(row=2, column=1, sticky=W)


        checkbuttonFrame = Frame(self)
        checkbuttonFrame.grid(row=3, column=0, columnspan=5)

        self.checkVarNumeric = IntVar()
        self.cboNumeric = Checkbutton(checkbuttonFrame, text='Numeric [0-9]', variable=self.checkVarNumeric, command=self.selectionChange)
        self.cboNumeric.grid(row=0, column=0)

        self.checkVarUpper = IntVar()
        self.cboUpper = Checkbutton(checkbuttonFrame, text='Upper [A-Z]', variable=self.checkVarUpper, command=self.selectionChange)
        self.cboUpper.grid(row=0, column=1)

        self.checkVarLower = IntVar()
        self.cboLower = Checkbutton(checkbuttonFrame, text='Lower [a-z]', variable=self.checkVarLower, command=self.selectionChange)
        self.cboLower.grid(row=0, column=2)

        self.checkVarSpecial = IntVar()
        self.cboSpecial = Checkbutton(checkbuttonFrame, text='Special', variable=self.checkVarSpecial, command=self.selectionChange)
        self.cboSpecial.grid(row=0, column=3)


        self.rdoCustom = Radiobutton(self, text='Custom:', variable=self.charsetVar, value=2, command=self.selectionChange)
        self.rdoCustom.grid(row=4, column=1, sticky=W)

        self.txtChars = Entry(self, width=60, validate='key', validatecommand=self.customBox)
        self.txtChars.grid(row=5, column=1, columnspan=3, sticky=E)

        scrollbar = Scrollbar(self, command=self.txtChars.xview, orient='horizontal')
        scrollbar.grid(row=5, column=4, sticky=W)
        self.txtChars['xscrollcommand'] = scrollbar.set


        buttonFrame = Frame(self)
        buttonFrame.grid(row=9, column=0, columnspan=5)

        self.btnStart = Button(buttonFrame, text='Start', command=self.run)
        self.btnStart.grid(row=0, column=0)

        self.btnStop = Button(buttonFrame, text='Stop', command=self.stop)
        self.btnStop.grid(row=0, column=1)


        outputFrame = Frame(self, relief='sunken', borderwidth=2)
        outputFrame.grid(row=10, column=0, columnspan=5)

        self.statusVar = StringVar()
        self.statusVar.set('Ready')
        lblStatus = Label(outputFrame, width=9, textvariable=self.statusVar, anchor='center')
        lblStatus.grid(row=0, column=0)

        self.outputVar = StringVar()
        lblOutput = Label(outputFrame, width=30, textvariable=self.outputVar, anchor='center')
        lblOutput.grid(row=1, column=0)


    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.createWidgets()
        self.filename = ''
        self.charsetVar.set(1)
        self.checkVarLower.set(1)
        self.selectionChange()
        self.master.title('7z Password Cracker')
        self.master.resizable(0,0)


main = Main()
main.mainloop() 
