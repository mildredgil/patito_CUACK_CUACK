def notExist(a):
    raise Exception("{} does not exist. Declare it before use it.".format(a))

def multipleDeclaration(a):
    raise Exception("Multiple Declaration. {} already exist.".format(a))

def missMatchType(a, b):
    raise Exception("Excepted a {} type for {} variable".format(a,b))

def missMatchTypeBool():
    raise Exception("Excepted a bool type".format())

def paramCountDif(func, paramsCount):
    raise Exception("Function {} expecting {} parameters".format(func, paramsCount))

def paramMissMatch(func, paramType):
    switcher={
                'i': 'int',
                'f': 'float',
                'c': 'char',
                'b': 'bool'
             }
    raise Exception("Function {} expecting param of type: {}".format(func, switcher.get(paramType,"Invalid type")))

def cantAssign(op1, op2):
    raise Exception("Cant assign {} to {}".format(op1, op2))

def notEnoughMem():
    raise Exception("Program has exceed memory limits")