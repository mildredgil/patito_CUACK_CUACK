import json
from err import *

class VarTable():
    def __init__(self):
        self.table = {}

    def exist(self, a, b):
        return b in a

    def existVar(self, var):
        return var in self.table

    def insert(self, varName, varType, address=None):
        if(self.exist(self.table, varName)):
            multipleDeclaration(varName)
        else:
            self.table[varName] = {'type': varType, 'address': address, 'dim': []}
        
    def dimStoreDimR(self, varName, dimR):
        self.table[varName]["dimR"]=dimR
        
    def getDimR(self, varName):
        return self.table[varName]["dimR"]
    
    def dimStoreLim(self, varName, dim, lim):
        if lim > 0:
            self.table[varName]["dim"].append({'lim': lim, 'mi': None})
        else:
            dimLimError(lim)

    def dimStoreMi(self, varName, dim, r):
        if dim < len(self.table[varName]["dim"]):
            mi = r/(self.table[varName]["dim"][dim ]['lim'] + 1)
            self.table[varName]["dim"][dim ]['mi'] = mi
            return mi
        else:
            outOfRange()

    def dimGetMi(self, varName, dim):
        if dim < len(self.table[varName]["dim"]):
            return self.table[varName]["dim"][dim - 1]['mi']
        else:
            outOfRange()

    def dimGetLim(self, varName, dim):
        if dim > 0 and dim <= len(self.table[varName]["dim"]):
            return self.table[varName]["dim"][dim - 1]["lim"]
        else:
            dimLimError(dim)
    
    def getDimentions(self, varName):
        return len(self.table[varName]["dim"])


    def getCompleteDimentions(self, varName):
        x = []
        for d in self.table[varName]["dim"]:
            x.append(d["lim"])
        return x

    def hasDim(self, varName):
        if len(self.table[varName]["dim"]) == 0:
            varNoDim(varName)
        
    def hasDimNoErr(self, varName):
        return len(self.table[varName]["dim"]) > 0

    def isNextDim(self, varName, currDim):
        return len(self.table[varName]["dim"]) > currDim

    def getType(self, varName):
        if(self.exist(self.table, varName)):
            return self.table[varName]['type']
        else:
            notExist(varName)

    def getAddress(self, varName):
        if(self.exist(self.table, varName)):
            return self.table[varName]['address']
        else:
            notExist(varName)

    def delete(self):
        self.table = None
            
    def print(self, name):
        print("printing varTable from %s:" % name)
        print(json.dumps(self.table, indent=2))

class DirFunc():
    def __init__(self):
        self.table = {}
        
    def existFunc(self, func):
        return func in self.table

    def exist(self, a, b):
        return b in a

    def insert(self, funcName, funcType, funcAddress=None, params='', startCounter=-1, numLocals=0):
        if(self.exist(self.table, funcName)):
            multipleDeclaration(funcName)
        else:
            if funcAddress:
                self.getTable("global").insert(funcName, funcType, funcAddress)

            self.table[funcName] = {'type': funcType, 'table': VarTable(), 'params': params, 'startCounter': startCounter, 'numLocals': numLocals}

    def getCompleteDimentions(self, funcName, varName):
        try:
            return self.getTable(funcName).getCompleteDimentions(varName)
        except:
            try: 
                return self.getTable("global").getCompleteDimentions(varName)
            except:
                notExist(varName)

    def insertParam(self, funcName, param):
        self.table[funcName]['params'] += param

    def getParams(self, funcName):
        return self.table[funcName]['params']
        
    def insertStartCounter(self, funcName, counter):
        self.table[funcName]['startCounter'] = counter

    def getStartCounter(self, funcName):
        return self.table[funcName]['startCounter']

    def addNumLocals(self, funcName):
        self.table[funcName]['numLocals'] += 1
    
    def getTable(self, funcName):
        if(self.exist(self.table, funcName)):
            return self.table[funcName]['table']
        else:
            notExist(funcName)

    def getType(self, funcName='global'):
        if self.exist(self.table, funcName):
            return self.table[funcName]["type"]
        else:
            notExist(funcName)
    
    def getTypeVar(self, varName, funcName):
        try:
            return self.getTable(funcName).getType(varName)
        except:
            try: 
                return self.getTable("global").getType(varName)
            except:
                notExist(varName)

    def getAddressVar(self, varName, funcName):
        try:
            return self.getTable(funcName).getAddress(varName)
        except:
            try: 
                return self.getTable("global").getAddress(varName)
            except:
                notExist(varName)

    def existVar(self, varName, funcName):
        if self.getTable(funcName).exist(self.getTable(funcName).table, varName) or self.getTable("global").exist(self.getTable("global").table, varName):
            return True
        else:
            notExist(varName)


    def existVarNoErr(self, varName, funcName):
        return self.getTable(funcName).exist(self.getTable(funcName).table, varName) or self.getTable("global").exist(self.getTable("global").table, varName)
            

    def deleteTable(self, funcName): 
        if self.existFunc(funcName):
            self.getTable(funcName).delete
            self.table[funcName]["table"] = None
        else:
            notExist(funcName)

    def print(self):
        for a in self.table:
            print("function: ", a," type: ", self.table[a]["type"], "   params: ", self.table[a]["params"], ' startCounter: ', self.table[a]["startCounter"], ' numLocals: ', self.table[a]["numLocals"])
            if self.table[a]["table"]:
                self.getTable(a).print(a)