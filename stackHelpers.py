from err import *
from typeMatching import *
from memoryConstants import *

test= False


def pushOperandType(operSt, typeSt, memSt, dimSt, oper, type, mem,d):
    """Function that pushes information to difrent stacks"""
    operSt.push(oper)
    typeSt.push(type)
    memSt.push(mem)
    dimSt.push(d)
    

def normalQuad(opSt, operSt, typeSt, memSt, dimSt, quad, temp, dataTable, currentFunc, memoryManager, memScope, constTable):
    """Function that pases info from stacks to quads "normal stands for normal mathematical operation into a temporal value"""
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
        dimMismatch(r, rdim, l, ldim)
    
    dimR=1

    if ldim!=[]:
        dimR = dataTable.getTable(currentFunc).getDimR(r)
        dimQuad(r, rdim, memScope, constTable, memoryManager, quad)

    mem = memoryManager.get(MEM[memScope]['TEMP'][newType.upper()],dimR)

    if test:
        quad.add(op, l, r, mem)
    else:
        quad.add(op, lm, rm, mem)
    
    operSt.push(newVar)
    typeSt.push(newType)
    memSt.push(mem)
    dimSt.push(ldim)


def assignQuad(opSt, operSt, typeSt, memSt, dimSt, dataTable, currentFunc, quad, memoryManager, memScope, constTable):
    """
        Function that pases info from stacks to quads
        This function does it specificaly to assign "="
    """
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
        raise Exception("Los operadores {} y {} no tienen las mismas dimensiones {} tiene: {} y {} tiene: {}".format(r,l,r,rdim,l,ldim))

    _ = TypeMatching.sem(0,rType , op, lType)
    
    if ldim!=[]:
        dimQuad(r, ldim, memScope, constTable, memoryManager, quad)
        
    if test:
        quad.add(op, r, None, l)
    else:
        quad.add(op, rm, None, lm)


def singeOpQuad(opSt, operSt, memSt, quad, temp):
    """
        Function that pases info from stacks to quads
        This function was never used
    """
    op = opSt.pop()
    r = operSt.pop()
    rm = memSt.pop()
    
    quad.add(op, rm, None, temp)


def gotoFQuad(operSt, typeSt, jumpSt, memSt, dimSt, quad):
    """
        Function that pases info from stacks to quads
        This insertes the gotof (goto on false) quad used in loops
    """
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
    """This fills the gotof quads"""
    index = jumpSt.pop()
    quad.update(index, quad.getCount())



def gotoQuad(quad, jumpSt):
    """
        This inserts the GOTO quad 
        used in while, for and while HEY
    """
    #add goto
    indexGOTO = quad.getCount()
    quad.add("GOTO", None, None, None)
    #update gotoF
    index = jumpSt.pop()
    quad.update(index, quad.getCount())

    #push goto index
    jumpSt.push(indexGOTO)

def gotoSimpleQuad(quad, jumpSt):
    """
        This inserts the GOTO quad 
        used in the start of the stack
    """
    jumpSt.push(quad.getCount())
    quad.add("GOTO", None, None, None)


def fillGotoQuad(quad, jumpSt):
    """Fills goto quad"""
    index = jumpSt.pop()
    quad.update(index, jumpSt.pop())


def printQuad(toPrint, quad):
    """Basic printing quad used in all prints"""
    quad.add('PRINT',toPrint,None,None)


def returnQuad(typeSt, operSt, memSt, dimSt, dataTable, func, quad):
    """Inserts the return into quad used only on the return function"""
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
    """ Call function Quad.
        Add a PARAM Quad with the parameter
    """

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
    """
        Inserts the era call into the quad
        used only in era_call
    """
    if dataTable.existFunc(func):
        quad.add("ERA", func, None, None)
    else:
        notExist(func)


def validParamLen(paramCounter, funcParamLen, func):
    """
        Veryfies param length
        used only in llamada
    """
    if paramCounter != funcParamLen:
        paramCountDif(func, funcParamLen)



def callAssignQuad(funcName, funcType, temp, typeSt, operSt, memSt, address, memoryManager, memScope, quad):
    """
        Asigns the return value of a function
        used only in llamada
    """
    newVar = "t" + str(temp)
    mem = memoryManager.get(MEM[memScope]['TEMP'][funcType.upper()],1)
    
    if test:
        quad.add("=", funcName, None, newVar)
    else:
        quad.add("=", address, None, mem)
    typeSt.push(funcType)
    operSt.push(newVar)
    
    memSt.push(mem)

def expQuads(stopOp, pilaOp, pilaOper,  pilaType, pilaMemoria, pilaDim, quad,  tempVar, dataTable, currentFunc, memoryManager, memScope, constTable):
    """ 
        Help EXP Quads. 
        Creates normalQuads until stop operator is at top.
    """

    while pilaOp.top() != stopOp:
        normalQuad(pilaOp, pilaOper,  pilaType, pilaMemoria, pilaDim, quad,  tempVar, dataTable, currentFunc, memoryManager, memScope, constTable)
        tempVar = tempVar + 1
    pilaOp.pop()

# DIMENSIONED VARIABLES QUADS ######################################################################################

def verQuad(operSt, typeSt, memSt, lim, quad):
    """ 
        Add special Quad for dimentioned Variables. \n
        Adds VER quad. Only need to test if index is smaller
        than max Limit.
    """

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
    """ 
        Add special Quad for dimentioned Variables. \n
        Add special Times Quad for carrying R size for
        dimensional variables
    """

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
    """ Add special Quad for dimentioned Variables. \n
        add the index plus the mi variable field."""

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
    """ 
        Add special Quad for dimentioned Variables.
        Add Quad for TEMP POINTER address. This Quad assign 
        and address to the dimensioned variable index.
    """

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
    memSt.push("*" + str(tempMem))
    dimSt.push([])

def dimQuad(id, dim, scope, constTable, memoryManager, quad):
    """
        Adds the special DIM quad that goes before adding or resting matrixes
    """
    dimensions = dim
    
    for i, dim in enumerate(dimensions):
        if constTable.existVar(dim):
                memR = constTable.getAddress(dim)
        else:
            memR = memoryManager.get(MEM['CONST']['INT'],1)
            constTable.insert(dim,'int', memR)
        
        quad.add("DIM",dim,None,"d" + str(i))
    