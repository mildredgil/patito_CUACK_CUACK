from err import *
from typeMatching import *

def pushOperandType(operSt, typeSt, oper, type):
    operSt.push(oper)
    typeSt.push(type)

def normalQuad(opSt, operSt, typeSt, quad, temp):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()

    rType = typeSt.pop()
    lType = typeSt.pop()

    newType = TypeMatching.sem(0, rType, op, lType)
    
    newVar = "t" + str(temp)
    
    quad.add(op, l, r, newVar)
    operSt.push(newVar)
    typeSt.push(newType)

def assignQuad(opSt, operSt, typeSt, quad):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()

    rType = typeSt.pop()
    lType = typeSt.pop()

    _ = TypeMatching.sem(0, rType, op, lType)
    
    quad.add(op, r, None, l)

def singeOpQuad(opSt, operSt, quad, temp):
    op = opSt.pop()
    r = operSt.pop()
    
    quad.add(op, r, None, temp)

def gotoFQuad(operSt, typeSt, jumpSt, quad):
    boolType = typeSt.pop()

    if boolType != "bool":
        missMatchTypeBool()

    result = operSt.pop()
    jumpSt.push(quad.getCount())
    quad.add("GOTOF", result, None, None)
    
def fillGotoFQuad(quad, jumpSt):
    index = jumpSt.pop()
    quad.update(index, quad.getCount())

def gotoQuad(quad, jumpSt):
    #add goto
    indexGOTO = quad.getCount()
    quad.add("GOTO", None, None, None)
    #update gotoF
    index = jumpSt.pop()
    quad.update(index, quad.getCount())

    #push goto index
    jumpSt.push(indexGOTO)

def gotoSimpleQuad(quad, jumpSt):
    jumpSt.push(quad.getCount())
    quad.add("GOTO", None, None, None)
    
def fillGotoQuad(quad, jumpSt):
    index = jumpSt.pop()
    quad.update(index, jumpSt.pop())


def gotoQuadFor(quad, jumpSt):
    #add goto
    indexGOTO = quad.getCount()
    quad.add("GOTO", None, None, None)
    #update gotoF
    index = jumpSt.pop()
    quad.update(index, quad.getCount() + 1)

    #push goto index
    jumpSt.push(indexGOTO)

def printQuad(toPrint, quad):
    quad.add('PRINT',toPrint,None,None)

def returnQuad(typeSt, operSt, dataTable, func, quad):
    operType = typeSt.pop()
    funcType = dataTable.getType(func)
    _ = TypeMatching.sem(0,funcType, "=", operType)
    quad.add("RETURN", None, None, operSt.pop())

def paramQuad(typeSt, operSt, dataTable, func, quad, paramCounter):
    params = dataTable.getParams(func)
    operType = typeSt.pop()
    
    if paramCounter > len(params):
        paramCountDif(func, len(params))
    elif params[paramCounter - 1] != operType[0]:
        paramMissMatch(func, params[paramCounter - 1])
        
    quad.add("PARAM", operSt.pop(), None, "p" + str(paramCounter))

def eraQuad(dataTable, func, quad):
    if dataTable.existFunc(func):
        quad.add("ERA", func, None, None)
    else:
        notExist(func)

def validParamLen(paramCounter, funcParamLen, func):
    if paramCounter != funcParamLen:
        paramCountDif(func, funcParamLen)

def callAssignQuad(funcName, funcType, temp, typeSt, operSt, quad):
    newVar = "t" + str(temp)
    quad.add("=", funcName, None, newVar)
    typeSt.push(funcType)
    operSt.push(newVar)

