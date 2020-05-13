import json

def notExist(a):
    raise Exception("{} does not exist. Declare it before use it.".format(a))

def multipleDeclaration(a):
    raise Exception("Multiple Declaration. {} already exist.".format(a))

def missMatchType(a, b):
    raise Exception("Excepted a {} type for {} variable".format(a,b))

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

    def getType(self, varName):
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
            
    def print(self, name):
        print("printing data from %s:" % name)
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
            self.table[funcName] = {'type': funcType, 'table': VarTable()}
    
    def insertVarTable(self, funcName, varTable):
        self.table[funcName]['variables'] = varTable.table

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
    
    def getValueVar(self, varName, funcName):
        try:
            return self.table.getTable(funcName).look(varName)
        except:
            try: 
                return self.table.getTable("global").look(varName)
            except:
                notExist(funcName)

    def getTypeVar(self, varName, funcName):
        try:
            return self.getTable(funcName).getType(varName)
        except:
            try: 
                return self.getTable("global").getType(varName)
            except:
                notExist(varName)

    def existVar(self, varName, funcName):
        if self.getTable(funcName).exist(self.getTable(funcName).table, varName) or self.getTable("global").exist(self.getTable("global").table, varName):
            return True
        else:
            notExist(varName)

    def print(self):
        for a in self.table:
            print(a)
            self.getTable(a).print(a)

'''
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
        print("printing data from DirFunc:")
        print(json.dumps(self.table, indent=2))
        
'''