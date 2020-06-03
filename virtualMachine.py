import csv
import numpy as np
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

    def getLocal(self):
        return self.memory[LOCAL]
    
    def insertPointer(self, memory, val):
        if memory < MEM_LOCAL:
            self.memory[GLOBAL].insertP(memory, val)
        elif memory < MEM_CONST:
            self.memory[LOCAL].insertP(memory, val)
            
    def insertNormal(self, memory, val):
        if memory < MEM_LOCAL:
            self.memory[GLOBAL].insert(memory, val)
        elif memory < MEM_CONST:
            self.memory[LOCAL].insert(memory, val)
        else:
            self.memory[CONST].insert(memory, val)

    def insert(self, memory, val):
        if memory[0] == "*":
            self.insertPointer(int(memory[1:]), val)
        else:
            self.insertNormal(int(memory), val)
    
    def value(self, memory):
        if memory[0] == "*":
            return self.valuePointer(int(memory[1:]))
        else:
            return self.valueNormal(int(memory))

    def valueNormal(self, memory):
        if memory < MEM_LOCAL:
            return self.memory[GLOBAL].value(memory)
        elif memory < MEM_CONST:
            return self.memory[LOCAL].value(memory)
        else:
            return self.memory[CONST].value(memory)

    def valuePointer(self, memory):
        if memory < MEM_LOCAL:
            return self.memory[GLOBAL].valueP(memory)
        elif memory < MEM_CONST:
            return self.memory[LOCAL].valueP(memory)

    def print(self, scope=None):
        if scope != None: 
            print(scope, self.memory[scope].memory,'\n')
        else:
            print("GLOBAL", self.memory[GLOBAL].memory)

            if self.memory[LOCAL]:
                print("LOCAL", self.memory[LOCAL].memory)

            print("CONST", self.memory[CONST].memory, '\n')
        
class Memory(): 
    def __init__(self,scope):
        if scope == GLOBAL:
            self.memory =  MemoryStruct.globalStruct()
        elif scope == LOCAL:
            self.memory =  MemoryStruct.localStruct()
        elif scope == CONST:
            self.memory =  MemoryStruct.constStruct()
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

    def insertP(self, memory, val):
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

        self.insert(self.value(memory), value)

    def value(self, memory):
        memory = int(memory)
        memType = memory // 10000
        memPos = memory % 10000
        
        if not memPos in self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ]:
            notDefined("function")
        return self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ]

    def valueP(self, memory):
        memory = int(memory)
        memType = memory // 10000
        memPos = memory % 10000
        
        if not memPos in self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ]:
            notDefined("function")
        
        value = self.memory[ MEM_INFO[memType][ISTEMP] ][ MEM_INFO[memType][ISPOINTER] ][ MEM_INFO[memType][TYPE] ][ memPos ]
        return self.value(value)
            

    def print(self):
        print(self.memory)

class MemoryStruct():
    @classmethod
    def constStruct(self):
        const_struct = [
            [
                [{},{},{},{}],      #CONST_NO_TEMP_NO_POINTER
            ],
        ]
        return const_struct

    @classmethod
    def localStruct(self):
        local_struct = [
            [
                [{},{},{}]          #LOCAL_NO_TEMP_NO_POINTER
            ],
            [
                [{},{},{},{}],      #LOCAL_TEMP_NO_POINTER
                [{},{},{}]          #LOCAL_TEMP_POINTER
            ],
        ]
        return local_struct

    @classmethod
    def globalStruct(self):
        global_struct = [
            [
                [{},{},{}]          #GLOBAL_NO_TEMP_NO_POINTER
            ],
            [
                [{},{},{},{}],      #GLOBAL_TEMP_NO_POINTER
                [{},{},{}]          #GLOBAL_TEMP_POINTER
            ],
        ]
        return global_struct
        
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
        self.dimList = []
        
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
                            self.currentMem.insert(row['2'],D(row['1']))
                        else:
                            self.currentMem.insert(row['2'],row['1'])
        
        self.currentMem.print()
        self.dirFunc.print()

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
                "?":        self.determinantAction,
                "!":        self.transposeAction,
                "?":        self.determinantAction,
                "PRINT":    self.printAction,
                "READ":     self.readAction,
                "GOTO":     self.gotoAction,
                "GOTOF":    self.gotoFAction,
                "ERA":      self.eraAction,
                "PARAM":    self.paramAction,
                "GOSUB":    self.gosubAction,
                "ENDPROC":  self.endPAction,
                "RETURN":   self.returnAction,
                "VER":      self.verAction,
                "DIM":      self.dimAction
            }

            #print("#", self.currentCounter, "   ", quadInstruction)
            #self.currentMem.print()
            func = switch.get(quadInstruction[0], "END")
            func(quadInstruction)
            quadInstruction = self.quad.get(int(self.currentCounter))
        self.currentMem.print()
#   IO ACTIONS     ########################################################################

    def printAction(self, quad):
        if quad[1] == '\\n':
            print(' ')
        elif quad[1] == ' ':
            print(' ', end="")
        else:
            print(self.currentMem.value(quad[1]), end ="")
        self.setCounter(self.currentCounter + 1)

    def readAction(self, quad):
        valor = input("")
        self.currentMem.insert(quad[3], valor)
        self.setCounter(self.currentCounter + 1)

#   EXPRESION ACTIONS     ########################################################################
                
    def addAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) + self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def susbtractAction(self, quad):
        if quad[2]:
            self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) - self.currentMem.value(quad[2]))
        else:
            self.currentMem.insert(quad[3],  -1 * self.currentMem.value( quad[1]) )
        self.setCounter(self.currentCounter + 1)

    def timesAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) * self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def divideAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) / self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def asignAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]))
        self.setCounter(self.currentCounter + 1)

    def equalAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) == self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def lteAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) <= self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)
    
    def gteAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) >= self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def diffAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) != self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def ltAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) < self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)
    
    def gtAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) > self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def andAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) and self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

    def orAction(self, quad):
        self.currentMem.insert(quad[3], self.currentMem.value(quad[1]) or self.currentMem.value(quad[2]))
        self.setCounter(self.currentCounter + 1)

#   JUMP ACTIONS     ########################################################################

    def gotoAction(self, quad):
        self.setCounter(int(quad[3]))

    def gotoFAction(self, quad):
        #evaluate value
        if self.currentMem.value(quad[1]) == "True":
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
                local.insert(intCount, self.currentMem.value(aux.pop()))
                intCount += 1
            elif varType == "f":
                local.insert(flCount, self.currentMem.value(aux.pop()))
                flCount += 1
            elif varType == "c":
                local.insert(chCount, self.currentMem.value(aux.pop()))
                chCount += 1
        
        #push current Local Memory to stack
        self.pilaMem.push( self.currentMem.getLocal() )
        
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
        
        #pop local and set to current Memmory
        self.currentMem.setLocal(self.pilaMem.pop( ) )

    def returnAction(self, quad):
        nameFunc = self.pilaFunc.pop()
        mem = self.dirFunc.getAddressVar(nameFunc,"global")

        self.currentMem.insert(mem, self.currentMem.value(quad[3]))
        self.setCounter(self.currentCounter + 1)
    
# DIMENSIONED VARIABLES ######################################################################

    def verAction(self, quad):
        if not self.currentMem.value(quad[1]) < self.currentMem.value(quad[2]):
            outOfRange()
        self.setCounter(self.currentCounter + 1)
    
    def dimAction(self, quad):
        self.dimList.append(quad[1])
        self.setCounter(self.currentCounter + 1)

    def determinantAction(self, quad):
        startAddress = int(quad[1])
        mat = []
        
        size = 1
        dimension = []
        for dim in self.dimList:
            size = int(dim) * size
            dimension.append(int(dim))

        for el in range(startAddress, size + 2):
            mat.append( self.currentMem.value( str(el) ) )
        
        deter = np.linalg.det( np.reshape(mat, tuple(dimension)) )

        self.currentMem.insert(quad[3], deter)
        self.setCounter(self.currentCounter + 1)
        self.dimList = []

    def transposeAction(self, quad):
        startAddress = int(quad[1])
        mat = []
        
        size = 1
        dimension = []
        for dim in self.dimList:
            size = int(dim) * size
            dimension.append(int(dim))

        for el in range(startAddress, size + 2):
            mat.append( self.currentMem.value( str(el) ) )
        
        print("transpose",np.reshape(mat, tuple(dimension)))
        mat = np.transpose( np.reshape(mat, tuple(dimension)) )
        print("transpose",mat)
        mat = np.reshape(mat, size)

        self.currentMem.print()
        newStartAddress = int(quad[3])

        for index, pos in enumerate(mat):
            print(newStartAddress + index, mat[index], pos)
            self.currentMem.insert( str(newStartAddress + index), str(pos) )

        self.currentMem.print()
        self.setCounter(self.currentCounter + 1)
        self.dimList = []