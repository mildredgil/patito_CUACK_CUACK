from err import *
from typeMatching import *
from memoryConstants import *

test= False

def pushOperandType(operSt, typeSt, memSt, oper, type, mem):
    operSt.push(oper)
    typeSt.push(type)
    memSt.push(mem)

def normalQuad(opSt, operSt, typeSt, memSt, quad, temp, dataTable, currentFunc, memoryManager, memScope):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()
    rm = memSt.pop()
    lm = memSt.pop()

    rType = typeSt.pop()
    lType = typeSt.pop()

    newType = TypeMatching.sem(0, rType, op, lType)
    
    newVar = "t" + str(temp)
    
    mem = memoryManager.get(MEM[memScope]['TEMP'][newType.upper()],1)
    if test:
        quad.add(op, l, r, mem)
    else:
        quad.add(op, lm, rm, mem)
    
    operSt.push(newVar)
    typeSt.push(newType)
    memSt.push(mem)

def assignQuad(opSt, operSt, typeSt, memSt, quad):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()
    
    rm = memSt.pop()
    lm = memSt.pop()

    # print("R es:" + str(r) + " y L es:"+str(l))
    # if not r or not l:
    #     cantAssign(r, l)

    rType = typeSt.pop()
    lType = typeSt.pop()

    _ = TypeMatching.sem(0,rType , op, lType)
    
    if test:
        quad.add(op, r, None, l)
    else:
        quad.add(op, rm, None, lm)


def singeOpQuad(opSt, operSt, memSt, quad, temp):
    op = opSt.pop()
    r = operSt.pop()
    rm = memSt.pop()
    
    quad.add(op, rm, None, temp)

def gotoFQuad(operSt, typeSt, jumpSt, memSt, quad):
    boolType = typeSt.pop()

    print("estamos en ", boolType)

    if boolType != "bool":
        missMatchTypeBool()

    m = memSt.pop()
    result = operSt.pop()
    jumpSt.push(quad.getCount())

    if test:
        quad.add("GOTOF", result, None, None)
    else:
        quad.add("GOTOF", m, None, None)
    
    
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

def returnQuad(typeSt, operSt, memSt, dataTable, func, quad):
    operType = typeSt.pop()
    funcType = dataTable.getType(func)
    _ = TypeMatching.sem(0,funcType, "=", operType)
    if test:
        quad.add("RETURN", None, None, operSt.pop())
    else:
        operSt.pop()
    if not test:
        quad.add("RETURN", None, None, memSt.pop())

def paramQuad(typeSt, operSt, memSt, dataTable, func, quad, paramCounter):
    params = dataTable.getParams(func)
    operType = typeSt.pop()

    print(func, params, operType, paramCounter)
    if paramCounter > len(params):
        paramCountDif(func, len(params))
    elif params[paramCounter - 1] != operType[0]:
        paramMissMatch(func, params[paramCounter - 1])
    operSt.pop()
    quad.add("PARAM", memSt.pop(), None, "p" + str(paramCounter))

def eraQuad(dataTable, func, quad):
    if dataTable.existFunc(func):
        quad.add("ERA", func, None, None)
    else:
        notExist(func)

def validParamLen(paramCounter, funcParamLen, func):
    if paramCounter != funcParamLen:
        paramCountDif(func, funcParamLen)

def callAssignQuad(funcName, funcType, temp, typeSt, operSt, memSt, address, memoryManager, memScope, quad):
    newVar = "t" + str(temp)
    mem = memoryManager.get(MEM[memScope]['TEMP'][funcType.upper()],1)
    
    if test:
        quad.add("=", funcName, None, newVar)
    else:
        quad.add("=", address, None, mem)
    typeSt.push(funcType)
    operSt.push(newVar)
    
    memSt.push(mem)