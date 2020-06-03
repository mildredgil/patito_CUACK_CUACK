from err import notExist, multipleDeclaration, missMatchType
from dataTable import VarTable
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
            self.table[funcName] = {'type': funcType, 'table': VarTable(), 'name': funcName}

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

    def getAddress(self, funcName='global'):
        if self.exist(self.table, funcName):
            return self.table[funcName]["adress"]
        else:
            notExist(funcName)

    def print(self):
        for a in self.table:
            print(a)

