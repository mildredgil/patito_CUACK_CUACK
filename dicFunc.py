from err import notExist, multipleDeclaration, missMatchType
from varTable import VarTable
import json

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
    
    def funcHasVars(self, funcName):
        if (self.exist(self.table, funcName)):
            return not self.table[funcName]

    def look(self, funcName):
        if(self.exist(self.table, funcName)):
            return self.table[funcName]
        else:
            notExist(funcName)

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

'''
#1- Create DirFunc
funcs = DirFunc()

#2- Create global 
funcs.insert('global', 'void')

#3- create VarTable and add it to current Func
gDic = VarTable()
funcs.insertVarTable('global', gDic)

#4, 5- search for c, if exist in current VarTable, error if not insert var
gDic.insert('c', 'int')

#7,8,9- Insert function to dirFunc
funcs.insert('fun1', 'void')

#10- Create varTable and link it to fun1
fun1Dic = VarTable()
funcs.insertVarTable('fun1', fun1Dic)

#11- search for c, if exist in current VarTable error, if not insert var
fun1Dic.insert('c', 'int')
fun1Dic.insert('c', 'int')
funcs.print()

print(fun1Dic.look('a'))


dic = 
    'global': {
        'type': 'void',
        'varTable': {
            'a': {
                'int': 1,
                'float':3.0
            }
        }
    },
    'func':{
        'type': 'int',
        'varTable': {
            'a': {
                'type': 'int',
                'value': 1
            },
            'b': {
                'type': 'int',
                'value': 1
            },
        }
    }
'''