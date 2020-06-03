#Semantic Errors
#All of these functions raise difrent kind of errors
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

def outOfRange():
    raise Exception("array index out of range")

def dimLimError(lim):
    raise Exception("array dimension must be greated than 0. {} received.".format(lim))

#voy en esta
def invalidMemType(m):
    raise Exception("{} is an invalid memory type".format(m))

def varNoDim(varName):
    raise Exception("{} does not has dimensions set.".format(varName))

def dimNoInt():
    raise Exception("Array dimension must be of type ENT")

def idWithoutDim(var):
    raise Exception("{} is a dimensional variable. No dimension found.".format(var))

def dimErr(var):
    raise Exception("{} is missing array dimensions".format(var))

def dimMismatch(r,rdim,l,ldim):
    raise Exception("Los operadores {} y {} no tienen las mismas dimensiones {} tiene: {} y {} tiene: {}".format(r,l,r,rdim,l,ldim))

def varNotArray(id):
    raise Exception("Variable {} is not an array.".format(id))

#Runtime Errors
def notDefined(scope):
    raise Exception("RUNTIME ERROR: A variable wasn't initialized in {}.".format(scope))