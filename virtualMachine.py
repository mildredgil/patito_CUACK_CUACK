import csv
from quad import Quad
from dataTable import DirFunc, VarTable

class Memory():
    def __init__(self):
        self.memory =  {
            0: {},
            1: {}, 
            2: {}, 
            3: {}, 
            4: {}, 
            5: {}, 
            6: {}, 
            7: {}, 
            8: {}, 
            9: {}, 
            10: {}, 
            11: {}, 
            12: {}, 
            13: {}, 
            14: {}, 
            15: {}, 
            16: {}, 
            17: {}
        }

    def insert(self, memory, val):
        memType = memory // 1000
        self.memory[memType][memory] = val

    def value(self, memory):
        memType = memory // 1000
        return self.memory[memType][memory]

class VirtualMachine():
    def __init__(self, filename):
        self.filename = filename
        self.quad = Quad()
        self.constants = {}
        self.dirFunc = DirFunc()
        self.currentCounter = 0
        self.memory = Memory()
        
        self.readFile()
        self.execute()
        
    def setCounter(self, i):
        self.currentCounter = i

    def readFile(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            readingContext = 0
            for row in reader:
                if row['1'] == "#QUAD":
                    readingContext = 1
                elif row['1'] == "#DIRFUNC":
                    readingContext = 2
                elif row['1'] == "#CONST":
                    readingContext = 3
                else:
                    if readingContext == 1:
                        switcher = {
                            '_': None
                        }
                        self.quad.add(row['1'],switcher.get(row['2'],row['2']),switcher.get(row['3'],row['3']),switcher.get(row['4'],row['4']))
                    elif readingContext == 2:
                        self.dirFunc.insert(row['1'],row['2'],row['3'],row['4'],row['5'])
                    else:
                        if int(row['2']) < 16000:
                            self.memory.insert(int(row['2']),int(row['1']))
                        else:
                            self.memory.insert(int(row['2']),row['1'])
                        
        #self.quad.print()
        #self.dirFunc.print()
        
    def execute(self):
        instruction = self.quad.get(self.currentCounter)
        while instruction[0] != "END":
            switch = {
                "+": self.addAction,
                "-": self.susbtractAction,
                "*": self.timesAction,
                "/": self.divideAction,
                "=": self.asignAction,
                "PRINT": self.printAction,
                "GOTO": self.gotoAction,
                "GOTOF": self.gotoFAction,
            }
            func = switch.get(instruction[0], "END")
            func(instruction)
            instruction = self.quad.get(self.currentCounter)
            
    def addAction(self, quad):
        self.memory.insert(int(quad[3]), self.memory.value(int(quad[1])) + self.memory.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def susbtractAction(self, quad):
        self.memory.insert(int(quad[3]), self.memory.value(int(quad[1])) - self.memory.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def timesAction(self, quad):
        self.memory.insert(int(quad[3]), self.memory.value(int(quad[1])) * self.memory.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def divideAction(self, quad):
        self.memory.insert(int(quad[3]), self.memory.value(int(quad[1])) / self.memory.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def printAction(self, quad):
        if quad[1] == '\\n':
            print(' ')
        elif quad[1] == ' ':
            print(' ', end="")
        else:
            print(self.memory.value(int(quad[1])), end ="")
        self.setCounter(self.currentCounter + 1)

    def asignAction(self, quad):
        self.memory.insert(int(quad[3]), self.memory.value(int(quad[1])))
        self.setCounter(self.currentCounter + 1)

    def gotoAction(self, quad):
        self.setCounter(int(quad[3]))

    def gotoFAction(self, quad):
        if self.memory.value(quad[1]):
            self.setCounter(self.currentCounter + 1)
        else:
            self.setCounter(int(quad[3]))