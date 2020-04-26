import json

def notExist(a):
    print("%s does not exist. Declare it before use it." % a)

def multipleDeclaration(a):
    print("Multiple Declaration. %s already exist." % a)

def missMatchType(a, b):
    print("Excepted a %s type for %s variable" % (a, b))

class VarTable():
    def __init__(self, table=None):
        if table is None:
            self.table = {}
        else:
            self.table = table

    def exist(self, a, b):
        return b in a

    def typeMatch(self, var, value):
        return type(value).__name__ == var['type']
    
    def insert(self, varName, varType):
        if(self.exist(self.table, varName)):
            multipleDeclaration(varName)
        else:
            self.table[varName] = {'type': varType, 'value': None}

    def getTypeVar(self, varName):
        if(self.exist(self.table, varName)):
            return self.table[varName]['type']
        else:
            notExist(varName)
            
    def look(self, varName):
        if(self.exist(self.table, varName)):
            return self.table[varName]['value']
        else:
            notExist(varName)

    def update(self, varName, value):
        if(self.exist(self.table, varName)):
            if(self.typeMatch(self.table[varName], value)):
                self.table[varName]['value'] = value
            else:
                missMatchType(self.table[varName]['type'], varName)
        else:
            notExist(varName)
            
    def print(self):
        print(json.dumps(self.table, indent=2))

class DirFunc():
    def __init__(self):
        self.table = {}

    def exist(self, a, b):
        return b in a

    def insert(self, funcName, funcType):
        if(self.exist(self.table, funcName)):
            multipleDeclaration(funcName)
        else:
            self.table[funcName] = {'type': funcType, 'variables': {}}

    def look(self, funcName):
        if(self.exist(self.table, funcName)):
            return self.table[funcName]
        else:
            notExist(funcName)

    def funcHasVars(self, funcName):
        if (self.exist(self.table, funcName)):
            return not self.table[funcName]

    def insertVarTable(self, funcName, varTable):
        self.table[funcName]['variables'] = varTable.table

    def getVariables(self, funcName):
        return self.table[funcName]['variables']

    def getTypeFunc(self, funcName='global'):
        if self.exist(self.table, funcName):
            return self.table[funcName]["type"]
        else:
            notExist(funcName)

    def print(self):
        print(json.dumps(self.table, indent=2))
