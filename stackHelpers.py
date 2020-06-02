from err import *
from typeMatching import *
from memoryConstants import *

test= False

def pushOperandType(operSt, typeSt, memSt, dimSt, oper, type, mem,d):
    operSt.push(oper)
    typeSt.push(type)
    memSt.push(mem)
    dimSt.push(d)
    
def normalQuad(opSt, operSt, typeSt, memSt, dimSt, quad, temp, dataTable, currentFunc, memoryManager, memScope):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()
    rm = memSt.pop()
    lm = memSt.pop()
    ldim = dimSt.pop()
    rdim = dimSt.pop()

    rType = typeSt.pop()
    lType = typeSt.pop()

    newType = TypeMatching.sem(0, rType, op, lType)
    
    newVar = "t" + str(temp)

    if ldim != rdim:
        raise Exception("Los operadores {} y {} no tienen las mismas dimenciones {} tiene: {} y {} tiene: {}".format(r,l,r,rdim,l,ldim))

    mem = memoryManager.get(MEM[memScope]['TEMP'][newType.upper()],1)

    if test:
        quad.add(op, l, r, mem)
    else:
        quad.add(op, lm, rm, mem)
    
    operSt.push(newVar)
    typeSt.push(newType)
    memSt.push(mem)
    dimSt.push(ldim)

def assignQuad(opSt, operSt, typeSt, memSt, dimSt, dataTable, currentFunc, quad):
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()
    # dimSt.print()
    rm = memSt.pop()
    lm = memSt.pop()
    ldim = dimSt.pop()
    rdim = dimSt.pop()
    
    rType = typeSt.pop()
    lType = typeSt.pop()

            
    if ldim != rdim:
        raise Exception("Los operadores {} y {} no tienen las mismas dimenciones {} tiene: {} y {} tiene: {}".format(r,l,r,rdim,l,ldim))

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

def gotoFQuad(operSt, typeSt, jumpSt, memSt, dimSt, quad):
    boolType = typeSt.pop()


    if boolType != "bool":
        missMatchTypeBool()

    m = memSt.pop()
    dimSt.pop()
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
    quad.update(index, quad.getCount())

    #push goto index
    jumpSt.push(indexGOTO)

def printQuad(toPrint, quad):
    quad.add('PRINT',toPrint,None,None)

def returnQuad(typeSt, operSt, memSt, dimSt, dataTable, func, quad):
    operType = typeSt.pop()
    funcType = dataTable.getType(func)
    dimSt.pop()
    _ = TypeMatching.sem(0,funcType, "=", operType)
    if test:
        quad.add("RETURN", None, None, operSt.pop())
    else:
        operSt.pop()
    if not test:
        quad.add("RETURN", None, None, memSt.pop())

def paramQuad(typeSt, operSt, memSt, dimSt, dataTable, func, quad, paramCounter):
    params = dataTable.getParams(func)
    operType = typeSt.pop()
    dimSt.pop()

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

def expQuads(stopOp, pilaOp, pilaOper,  pilaType, pilaMemoria, pilaDim, quad,  tempVar, dataTable, currentFunc, memoryManager, memScope):
    while pilaOp.top() != stopOp:
        normalQuad(pilaOp, pilaOper,  pilaType, pilaMemoria, pilaDim, quad,  tempVar, dataTable, currentFunc, memoryManager, memScope)
        tempVar = tempVar + 1
    pilaOp.pop()

def verQuad(operSt, typeSt, memSt, lim, quad):
    tp = typeSt.top()
    
    if tp != "int":
        dimNoInt()

    operV = operSt.top()
    m = memSt.top()

    if test:    
        quad.add("VER",operV,lim,None)
    else:
        quad.add("VER",m,lim,None)

def miDimQuad(mi, temp, operSt, typeSt, memSt, dimSt, mem, scope, quad):
    oper = operSt.pop()
    t = typeSt.pop()
    memO = memSt.pop()
    dimSt.pop()
    newVar = "t" + str(temp)
    tempMem = mem.get(MEM[scope]['TEMP'][t.upper()],1)
    
    if test:
        quad.add("*", oper, mi, newVar)
    else:
        quad.add("*", memO, mi, tempMem)

    operSt.push(newVar)
    typeSt.push(t)
    memSt.push(tempMem)
    #this might be wrong
    dimSt.push([])

def miAddQuad(operSt, typeSt, memSt, dimSt, temp, mem, scope, quad):
    typeSt.pop()
    typeSt.pop()

    r = operSt.pop()
    l = operSt.pop()

    mr = memSt.pop()
    ml = memSt.pop()

    dimSt.pop()
    dimSt.pop()

    newVar = "t" + str(temp)

    tempMem = mem.get(MEM[scope]['TEMP']["INT"],1)

    if test:
        quad.add("+", l, r, newVar)
    else:
        quad.add("+", ml, mr, tempMem)

    operSt.push(newVar)
    typeSt.push("int")
    memSt.push(tempMem)
    dimSt.push([])

def dimAddressQuad(address, varType, operSt, typeSt, memSt, dimSt, temp, mem, scope, quad):
    l = operSt.pop()
    ml = memSt.pop()
    t = typeSt.pop()
    dimSt.pop()
    newVar = "t" + str(temp)
    tempMem = mem.get(MEM[scope]['TEMP']['POINTER'][varType.upper()],1)

    if test:
        quad.add("+", l, address, newVar)
    else:
        quad.add("+", ml, address, tempMem)

    operSt.push("(" + newVar + ")")
    typeSt.push(varType)
    memSt.push(tempMem)
    dimSt.push([])