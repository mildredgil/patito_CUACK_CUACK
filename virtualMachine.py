import csv
from quad import Quad
from dataTable import DirFunc, VarTable
from decimal import Decimal as D
from dataStructure import stack
from memoryConstants import MEM_GLOBAL, MEM_LOCAL, MEM_CONST, CONST_CHAR
from vmMemory import *

class CurrentMemory():
    def __init__(self):
        self.memory =  [
            Memory(GLOBAL),
            Memory(LOCAL),
            Memory(CONST),
        ]
        
    def insert(self, memory, val):
        if memory < MEM_LOCAL:
            self.memory[GLOBAL].insert(memory, val)
        elif memory < MEM_CONST:
            self.memory[LOCAL].insert(memory, val)
        else:
            self.memory[CONST].insert(memory, val)
        
    def value(self, memory):
        if memory < MEM_LOCAL:
            return self.memory[GLOBAL].value(memory)
        elif memory < MEM_CONST:
            return self.memory[LOCAL].value(memory)
        else:
            return self.memory[CONST].value(memory)
        
class Memory(): 
    def __init__(self,scope):
        self.memory =  memory_struct[scope]
        self.scope = scope

    def insert(self, memory, val):
        memType = memory // 10000
        memPos = memory % 10000
        if MEM_INFO[memType][TYPE] == INT:
            value = int(val)
        elif MEM_INFO[memType][TYPE] == FLOAT:
            value = float(val)
        
        self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ] = value
 
    def value(self, memory):
        memType = memory // 10000
        memPos = memory % 10000
        return self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ]
        
class VirtualMachine():
    def __init__(self, filename):
        #define variables
        self.filename = filename
        self.quad = Quad()
        self.constants = {}
        self.dirFunc = DirFunc()
        self.currentCounter = 0
        self.pilaMem = stack.Stack()
        self.currentMem = CurrentMemory()

        #run methods
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
                        if int(row['2']) < CONST_CHAR:
                            self.currentMem.insert(int(row['2']),D(row['1']))
                        else:
                            self.currentMem.insert(int(row['2']),row['1'])
                        
        self.quad.print()
        self.dirFunc.print()
        print(self.currentMem.memory[GLOBAL].memory)
        print(self.currentMem.memory[CONST].memory)
        #print currentMem
        
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
                "READ": self.readAction,
                "GOTO": self.gotoAction,
                "GOTOF": self.gotoFAction,
            }
            func = switch.get(instruction[0], "END")
            func(instruction)
            instruction = self.quad.get(self.currentCounter)
            
    def addAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) + self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def susbtractAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) - self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def timesAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) * self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def divideAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) / self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def printAction(self, quad):
        if quad[1] == '\\n':
            print(' ')
        elif quad[1] == ' ':
            print(' ', end="")
        else:
            print(self.currentMem.value(int(quad[1])), end ="")
        self.setCounter(self.currentCounter + 1)

    def readAction(self, quad):
        valor = input("")
        self.currentMem.insert(int(quad[3]), valor)
        self.setCounter(self.currentCounter + 1)

    def asignAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])))
        self.setCounter(self.currentCounter + 1)

    def gotoAction(self, quad):
        self.setCounter(int(quad[3]))

    def gotoFAction(self, quad):
        if self.currentMem.value(quad[1]):
            self.setCounter(self.currentCounter + 1)
        else:
            self.setCounter(int(quad[3]))