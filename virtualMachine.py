import csv
from quad import Quad
from dataTable import DirFunc, VarTable
from decimal import Decimal as D
from dataStructure import stack
from memoryConstants import MEM_GLOBAL, MEM_LOCAL, MEM_CONST, CONST_CHAR, LOCAL_INT, LOCAL_FLOAT, LOCAL_CHAR
from vmMemory import *
from err import *

class CurrentMemory():
    def __init__(self):
        self.memory =  [
            Memory(GLOBAL),
            None,
            Memory(CONST),
        ]

    def setLocal(self, local):
        self.memory[LOCAL] = local
        
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
    
    def print(self, scope=None):
        if scope:
            print(scope, self.memory[scope].memory)
        else:
            print("GLOBAL", self.memory[GLOBAL].memory)

            if self.memory[LOCAL]:
                print("LOCAL", self.memory[LOCAL].memory)

            print("CONST", self.memory[CONST].memory)
        
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
        elif MEM_INFO[memType][TYPE] == CHAR:
            value = str(val)
        elif MEM_INFO[memType][TYPE] == STRING:
            value = str(val)
        else:
            value = val
        
        self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ] = value
 
    def value(self, memory):
        memType = memory // 10000
        memPos = memory % 10000
        
        if not memPos in self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ]:
            notDefined("function")
        
        value = self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ]
        return value

    def print(self):
        print(self.memory)
        
class VirtualMachine():
    def __init__(self, filename):
        #define variables
        self.filename = filename
        self.quad = Quad()
        self.constants = {}
        self.dirFunc = DirFunc()
        self.currentCounter = 0
        self.pilaFunc = stack.Stack()
        self.pilaParams = stack.Stack() 
        self.pilaMem = stack.Stack()
        self.currentMem = CurrentMemory()
        self.pilaCounters = stack.Stack()
        
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
                        if row['1'] != 'global':
                            self.dirFunc.insert(row['1'],row['2'],row['5'],row['3'],row['4'],row['6'])
                        else:
                            self.dirFunc.insert(row['1'],row['2'],None,row['3'],row['4'],row['6'])
                    else:
                        if int(row['2']) < CONST_CHAR:
                            self.currentMem.insert(int(row['2']),D(row['1']))
                        else:
                            self.currentMem.insert(int(row['2']),row['1'])
                        
        self.quad.print()
        print("-------------")
        self.dirFunc.print()
        print("-------------")
        print(self.currentMem.memory[GLOBAL].memory)
        print(self.currentMem.memory[CONST].memory)
        #print currentMem
        
    def execute(self):
        quadInstruction = self.quad.get(self.currentCounter)
        while quadInstruction[0] != "END":
            switch = {
                "+":        self.addAction,
                "-":        self.susbtractAction,
                "*":        self.timesAction,
                "/":        self.divideAction,
                "==":       self.equalAction,
                "=":        self.asignAction,
                ">=":       self.gteAction,
                "<=":       self.gteAction,
                ">":        self.gtAction,
                "<":        self.ltAction,
                "!=":       self.diffAction,
                "|":        self.orAction,
                "&":        self.andAction,
                "PRINT":    self.printAction,
                "READ":     self.readAction,
                "GOTO":     self.gotoAction,
                "GOTOF":    self.gotoFAction,
                "ERA":      self.eraAction,
                "PARAM":    self.paramAction,
                "GOSUB":    self.gosubAction,
                "ENDPROC":  self.endPAction,
                "RETURN":   self.returnAction,
                "VER":      self.verAction
            }

            func = switch.get(quadInstruction[0], "END")
            func(quadInstruction)
            quadInstruction = self.quad.get(self.currentCounter)
            
#   IO ACTIONS     ########################################################################

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

#   EXPRESION ACTIONS     ########################################################################
                
    def addAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) + self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def susbtractAction(self, quad):
        if quad[2]:
            self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) - self.currentMem.value(int(quad[2])))
        else:
            self.currentMem.insert(int(quad[3]),  -1 * self.currentMem.value( int( quad[1])) )
        self.setCounter(self.currentCounter + 1)

    def timesAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) * self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def divideAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) / self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def asignAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])))
        self.setCounter(self.currentCounter + 1)

    def equalAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) == self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def lteAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) <= self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)
    
    def gteAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) >= self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def diffAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) != self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def ltAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) < self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)
    
    def gtAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) > self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def andAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) and self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

    def orAction(self, quad):
        self.currentMem.insert(int(quad[3]), self.currentMem.value(int(quad[1])) or self.currentMem.value(int(quad[2])))
        self.setCounter(self.currentCounter + 1)

#   JUMP ACTIONS     ########################################################################

    def gotoAction(self, quad):
        self.setCounter(int(quad[3]))

    def gotoFAction(self, quad):
        #evaluate value
        if self.currentMem.value(int(quad[1])) == "True":
            self.setCounter(self.currentCounter + 1)
        else:
            self.setCounter(int(quad[3]))

#   FUNCTION ACTIONS  ########################################################################
    
    def eraAction(self, quad):
        self.pilaMem.push(Memory(LOCAL))
        self.setCounter(self.currentCounter + 1)

    def paramAction(self, quad):
        self.pilaParams.push(quad[1])
        self.setCounter(self.currentCounter + 1)
        
    def gosubAction(self, quad):
        nameFunc = quad[1]
        #prepare params:
        params = self.dirFunc.getParams(nameFunc)
        
        local = self.pilaMem.pop()

        intCount = LOCAL_INT
        flCount  = LOCAL_FLOAT
        chCount  = LOCAL_CHAR

        aux = stack.Stack()
        for varType in params:
            aux.push(self.pilaParams.pop())

        for varType in params:
            if varType == "i":
                local.insert(intCount, self.currentMem.value(int(aux.pop())))
                intCount += 1
            elif varType == "f":
                local.insert(flCount, self.currentMem.value(int(aux.pop())))
                flCount += 1
            elif varType == "c":
                local.insert(chCount, self.currentMem.value(int(aux.pop())))
                chCount += 1
        
        #set local memory to current Memory
        self.currentMem.setLocal(local)
        
        #set previous counter
        self.pilaCounters.push(self.currentCounter)

        #add current function name
        self.pilaFunc.push(nameFunc)

        #move counter
        counter = int(self.dirFunc.getStartCounter(nameFunc))
        self.setCounter(counter)
        
    def endPAction(self, quad):
        self.setCounter(self.pilaCounters.pop() + 1)

    def returnAction(self, quad):
        nameFunc = self.pilaFunc.pop()
        mem = self.dirFunc.getAdressVar(nameFunc,"global")

        self.currentMem.insert(int(mem), self.currentMem.value(int(quad[3])))
        self.setCounter(self.currentCounter + 1)
    
# DIMENSIONED VARIABLES ######################################################################

    def verAction(self, quad):
        if not self.currentMem.value(int(quad[1])) < self.currentMem.value(int(quad[2])):
            outOfRange()
        
        self.setCounter(self.currentCounter + 1)