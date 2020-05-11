from typeMatching import *

def pushOperandType(operSt, typeSt, oper, type):
    operSt.push(oper)
    typeSt.push(type)

def normalQuad(opSt, operSt, typeSt, quad, temp):
    operSt.print()
    opSt.print()
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
    operSt.print()
    opSt.print()
    op = opSt.pop()
    r = operSt.pop()
    l = operSt.pop()

    rType = typeSt.pop()
    lType = typeSt.pop()

    _ = TypeMatching.sem(0, rType, op, lType)
    
    quad.add(op, r, None, l)

def gotoFQuad(operSt, typeSt, jumpSt, quad):
    quad.print()
    boolType = typeSt.pop()

    if boolType != "bool":
        raise Exception("Type mismatch. if was expecting a bool type")

    result = operSt.pop()
    jumpSt.push(quad.getCount())
    quad.add("GOTOF", result, None, None)
    jumpSt.print()

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

def fillGotoQuad(quad, jumpSt):
    index = jumpSt.pop()
    quad.update(index, jumpSt.pop())
    