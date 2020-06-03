# -----------------------------------------------------------------------------
# proyecto patito_CUACKCUACK
# AUTHORS: Mildred Gil Melchor, RAUL FLORES
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
from dataTable import *
from dataStructure import stack
from typeMatching import *
from quad import *
from stackHelpers import *
from memoryManager import *
from memoryConstants import *

test = False

#This class is part of SLY here we declare all of our token, literals, error handling on the lexer side. 
#This is only used on main to run the lexer.
class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { 
        STRING, INTNUMBER, FLOATNUMBER, CHARACTER, 
        ID, VAR, PROGRAM, PRINCIPAL,
        IF, ELSE, WHILE,
        PRINT, READ,
        DO, FROM, TO, DO2,
        FUNCTION, RETURN, INT, FLOAT, CHAR, VOID,
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
        EQ, LT, GT, NE, ELT, EGT, AND, OR, TRANSPOSE, INVERSE, DETERMINANT }

    #Literals are accepted as is by the lexer
    literals = { '[', ']','(', ')', '{', '}', ';', ':', ',', '.'}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS        = r'\+'
    MINUS       = r'-'
    TIMES       = r'\*'
    DIVIDE      = r'/'
    EQ          = r'=='
    ASSIGN      = r'='
    ELT         = r'<='
    EGT         = r'>='
    NE          = r'!='
    LT          = r'<'
    GT          = r'>'
    AND         = r'&'
    OR          = r'\|'
    TRANSPOSE   = r'\!'
    INVERSE     = r'\$'
    DETERMINANT = r'\?'
    
    #regex to represent spesific things

    @_(r'[0-9]+\.[0-9]+')
    def FLOATNUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['var'] = VAR
    ID['si'] = IF
    ID['sino'] = ELSE
    ID['escribe'] = PRINT
    ID['lee'] = READ
    ID['mientras'] = WHILE
    ID['haz'] = DO
    ID['hacer'] = DO2
    ID['desde'] = FROM
    ID['hasta'] = TO
    ID['funcion'] = FUNCTION
    ID['regresa'] = RETURN
    ID['programa'] = PROGRAM
    ID['ent'] = INT
    ID['deci'] = FLOAT
    ID['letra'] = CHAR
    ID['nada'] = VOID
    ID['principal'] = PRINCIPAL

    ignore_comment = r'\#.*'

    @_(r'\"(.*?)\"')
    def STRING(self, t):
        t.value = str(t.value[1: len(t.value) - 1])
        return t

    @_(r'\'(.?)\'')
    def CHARACTER(self, t):
        t.value = str(t.value[1: len(t.value) - 1])
        return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    #lexer errors.
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
    
    def printTokens(self,data):
        for tok in self.tokenize(data):
            print(tok)

#This class is also part of SLY this runs the configuration of the parser. 
#We declare all of the structures, neural points of the parser and also error handling of the parser here. 
#This is only used on main to run de parser.
class CalcParser(Parser):
    #debug file for testing purposes
    debugfile = 'parser.out'
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens
    
    def printTokens(self):
        for x in self.dataTable.table:
            self.dataTable.getTable(x).print()

    precedence = (
        ('left', PLUS, MINUS),
    )

    #initializes all of the global memories
    def __init__(self):
        self.dataTable = DirFunc()
        self.constTable = VarTable()
        self.pilaOp = stack.Stack()
        self.pilaOper = stack.Stack()
        self.pilaType = stack.Stack()
        self.pilaMemoria = stack.Stack()
        self.pilaDimGlob = stack.Stack()
        self.pilaJump = stack.Stack()
        self.pilaForOp = stack.Stack()
        
        self.pilaCallId = stack.Stack()
        self.pilaparamCount = stack.Stack()
        
        self.pilaDim = stack.Stack()
        self.pilaDimCount = stack.Stack()
        self.pilaIsArray = stack.Stack()

        self.quad = Quad()
        self.tempVar = 0
        self.badAid = '0'
        self.isConst = False

        self.currentId = None
        self.currentType = None
        self.currentMem = None
        self.currentFunc = None
        self.currentDim = None
        self.globalFunc = None

        self.memScope = "GLOBAL"
        self.memoryManager = MemoryManager()

        self.dim = 0
        self.dimR = 1
        self.isArray = False
        


    #The descriptors on ALL of the following methods are used to tell the parser what to expect
    #Tells the parser the structure of the program, also inserts the last quad.
    #PROGRAMA
    @_('PROGRAM ID set_global ";" programa2 programa3 PRINCIPAL set_principal_quad "(" ")" bloque')
    def programa(self, p):
        self.quad.add("END",None,None, None)
        
    # Inserts global var table
    @_('')
    def set_global(self, p):
        self.dataTable.insert("global", "void")
        self.globalFunc = "global"
        self.currentFunc = "global"
        gotoSimpleQuad(self.quad, self.pilaJump)


    @_('')
    def set_principal_quad(self, p):
        self.memScope = "GLOBAL"
        self.currentFunc = self.globalFunc
        fillGotoFQuad(self.quad, self.pilaJump)

    @_('vars')
    def programa2(self, p):
        pass

    @_('empty')
    def programa2(self, p):
        pass

    @_('funcion programa3')
    def programa3(self, p):
        pass

    @_('empty')
    def programa3(self, p):
        pass

    # VARS
    @_('VAR var1')
    def vars(self, p):
        pass

    @_('tipo ids ";" var2')
    def var1(self, p):
        pass
        
    @_('var1')
    def var2(self, p):
        pass
        
    @_('empty')
    def var2(self, p):
        pass

    @_('identificadoresDec ids2')
    def ids(self, p):
        pass
        
    @_('"," ids')
    def ids2(self, p):
        pass

    @_('empty')
    def ids2(self, p):
        pass

    # FUNCION
    #Detects the function at the end inserts the final quad of the funcitons
    @_('FUNCTION funcion2 ID save_id parametros funcion2 bloque')
    def funcion(self, p):
        self.quad.add("ENDPROC", None, None, None)
        self.dataTable.deleteTable(self.currentFunc)
        self.memoryManager.resetTemp()

    @_('vars')
    def funcion2(self, p):
        pass

    @_('empty')
    def funcion2(self, p):
        pass
        
    #embedded action sav6
    @_('')
    def save_id(self, p):
        mem = None
        if self.currentType != "void":
            mem = self.memoryManager.get(MEM["GLOBAL"][self.currentType.upper()],1)
        self.dataTable.insert(p[-1], self.currentType, mem)
        self.dataTable.insertStartCounter(p[-1], self.quad.getCount())
        self.currentFunc = p[-1]
        self.memScope = "LOCAL"

    @_('tipo')
    def funcion2(self, p):
        pass

    @_('VOID')
    def funcion2(self, p):
        self.currentType = 'void'

    # PARAMETROS
    @_('"(" parametros2 ")"')
    def parametros(self, p):
        pass
        
    @_('tipo ID param parametros3')
    def parametros2(self, p):
        pass

    @_('')
    def param(self, p):
        self.currentId = p[-1]
        mem = self.memoryManager.get(MEM[self.memScope][p[-2].upper()],1)
        self.currentMem = mem
        self.dataTable.getTable(self.currentFunc).insert(p[-1],p[-2],mem)
        self.dataTable.insertParam(self.currentFunc, p[-2][0])
        
    @_('"," parametros2')
    def parametros3(self, p):
        pass

    @_('empty')
    def parametros3(self, p):
        pass

    #BLOQUE
    @_('"{" bloque2 "}"')
    def bloque(self, p):
        pass

    @_('estatuto bloque2')
    def bloque2(self, p):
        pass

    @_('empty')
    def bloque2(self, p):
        pass

    #ESTATUTO save1
    @_('asignacion',
        'escritura',
        'lee',
        'estDesicion',
        'estRepNoCond',
        'estRepCond',
        'regresa',
        'llamada ";"')
    def estatuto(self, p):
        pass

    #ASIGNACION
    @_('identificadores asignacion_insert_var ASSIGN exp asignacion_pop_all ";"')
    def asignacion(self, p):
        pass

    #embedded action save01
    @_('')
    def asignacion_insert_var(self, p):
        t = self.dataTable.getTypeVar(self.currentId, self.currentFunc)
        
        #m = self.dataTable.getAddressVar(self.currentId,self.currentFunc)
        m = self.currentMem
        print("------------------------------MEMORIAS m =", m, "currnetMem", self.currentMem)
        pushOperandType(self.pilaOper, self.pilaType, self.pilaMemoria, self.pilaDimGlob, self.currentId, t, m,self.pilaDimGlob.top())
        self.pilaOp.push("=")
        
    #embedded action
    #save1
    @_('')
    def asignacion_pop_all(self, p):
        while self.pilaOp.length() > 0:
            if self.pilaOp.top() != "=":
                normalQuad(
                    self.pilaOp,
                    self.pilaOper, 
                    self.pilaType,
                    self.pilaMemoria,
                    self.pilaDimGlob,
                    self.quad, 
                    self.tempVar,
                    self.dataTable,
                    self.currentFunc,
                    self.memoryManager,
                    self.memScope,
                    self.constTable
                    )
                self.tempVar = self.tempVar + 1

            else:
                assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.dataTable,
                self.currentFunc,
                self.quad,
                self.memoryManager,
                self.memScope,
                self.constTable
                )
            
    #lee
    @_('READ "(" lee2 ")" ";"')
    def lee(self, p):
        pass

    @_('identificadores lee_quad lee3')
    def lee2(self, p):
        pass

    @_('')
    def lee_quad(self, p):
        if self.dataTable.existVar(self.currentId, self.currentFunc):
            mem = self.dataTable.getAddressVar(self.currentId, self.currentFunc)
            self.quad.add("READ", None, None, mem)

    @_('"," lee2')
    def lee3(self, p):
        pass

    @_('empty')
    def lee3(self, p):
        pass

    #escritura
    @_('PRINT "(" escritura2 ")" ";"')
    def escritura(self, p):
        printQuad('\\n', self.quad)

    @_('exp print_quad1 escritura3')
    def escritura2(self, p):
        pass

    @_('STRING print_quad2 escritura3')
    def escritura2(self, p):
        pass

    @_('"," print_next escritura2')
    def escritura3(self, p):
        pass

    @_('empty')
    def escritura3(self, p):
        pass

    @_('')
    def print_quad1(self, p):
        oper = self.pilaOper.pop()
        m = self.pilaMemoria.pop()
        if(self.pilaDimGlob.top()!=[]):
            raise Exception("{} is an array.Cannot be printed.".format(oper))

        d = self.pilaDimGlob.pop()
        if test:
            printQuad(oper, self.quad)
        else:
            printQuad(m, self.quad)
        
    @_('')
    def print_quad2(self, p):
        if self.constTable.existVar(p[-1]):
            memo = self.constTable.getAddress(p[-1])
        else: 
            memo = self.memoryManager.get(MEM["CONST"]["STRING"],1)
            self.constTable.insert(p[-1],"string",memo)
        
        printQuad(memo, self.quad)
        
    @_('')
    def print_next(self, p):
        printQuad(' ', self.quad)

    #regresa
    @_('RETURN "(" exp ")" ";"')
    def regresa(self, p):
        returnQuad(self.pilaType, self.pilaOper, self.pilaMemoria , self.pilaDimGlob , self.dataTable, self.currentFunc, self.quad)

    #estatuto de decision
    @_('IF "(" expOR ")" if_gotF bloque estDesicion2 if_fill_gotF')
    def estDesicion(self, p):
        pass
    
    #embeded action
    @_('')
    def if_gotF(self, p):
        gotoFQuad(
            self.pilaOper,
            self.pilaType,
            self.pilaJump,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad
        )

    #embeded action
    @_('')
    def if_fill_gotF(self, p):
        fillGotoFQuad(self.quad, self.pilaJump)
        
    @_('ELSE if_goto bloque')
    def estDesicion2(self, p):
        pass
    
    #embeded action
    @_('')
    def if_goto(self, p):
        gotoQuad(
            self.quad,
            self.pilaJump
        )

    @_('empty')
    def estDesicion2(self, p):
        pass
    
    # estatuto de repeticion condicional

    @_('while_push_pila_jumps WHILE "(" expOR ")" if_gotF DO bloque while_goto')
    def estRepCond(self, p):
        pass

    #embedded action
    @_('')
    def while_push_pila_jumps(self, p):
        self.pilaJump.push(self.quad.getCount())

    #embeded action
    @_('')
    def while_goto(self, p):
        gotoQuad(
            self.quad,
            self.pilaJump
        )
        fillGotoQuad(
            self.quad,
            self.pilaJump
        )

    # estatuto de repeticion no condicional

    @_(' FROM identificadores ASSIGN from_create exp from_assign TO exp from_gotF DO2 bloque from_suma from_goto')
    def estRepNoCond(self, p):
        pass
    
    #embeded action save9
    @_('')
    def from_create(self, p):
        self.pilaForOp.push(self.currentId)
        self.pilaOp.push('=')
        
    #embeded action
    @_('')
    def from_assign(self, p):
        assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.dataTable,
                self.currentFunc,
                self.quad,
                self.memoryManager,
                self.memScope,
                self.constTable
                )
        
    #embeded action
    @_('')
    def from_gotF(self, p):
        m = self.dataTable.getAddressVar(self.pilaForOp.top(),self.currentFunc)
        #CODIGOROJO
        d = self.dataTable.getCompleteDimentions(self.currentFunc, self.pilaForOp.top())
        self.pilaOper.push(self.pilaForOp.top())
        self.pilaOp.push('>=')
        self.pilaType.push('int')
        self.pilaMemoria.push(m)
        self.pilaDimGlob.push(d)
        
        self.pilaJump.push(self.quad.getCount())
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad,
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope,
            self.constTable
        )
        self.tempVar= self.tempVar +1
        
        self.pilaJump.push(self.quad.getCount())
        self.quad.add("GOTOF", self.pilaMemoria.top(), None, None)
        
    @_('')
    def from_goto(self, p):
        gotoQuad(
            self.quad,
            self.pilaJump
        )
        
        fillGotoQuad(
            self.quad,
            self.pilaJump
        )

    @_('')
    def from_suma(self, p):
        controlVar = self.pilaForOp.pop()
        m = self.dataTable.getAddressVar(controlVar,self.currentFunc)
        
        #push controlVar for addition
        pushOperandType(self.pilaOper, self.pilaType, self.pilaMemoria, self.pilaDimGlob, controlVar, 'int', m,[])

        #push controlVar for assigning result
        pushOperandType(self.pilaOper, self.pilaType, self.pilaMemoria, self.pilaDimGlob, controlVar, 'int', m,[])
        
        #push add
        self.pilaOp.push('+')

        #get +1, and push it
        memConst = 0
        if self.constTable.existVar(1):
            memConst = self.constTable.getAddress(1)
        else:
            memConst = self.memoryManager.get(MEM['CONST']['INT'],1)
            self.constTable.insert(1,'int', memConst)

        pushOperandType(self.pilaOper, self.pilaType, self.pilaMemoria, self.pilaDimGlob, 1, 'int', memConst,[])

        #add controlVar + 1
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad,
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope,
            self.constTable
        )
        
        self.pilaOp.push('=')

        assignQuad(
            self.pilaOp,
            self.pilaOper,
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.dataTable,
            self.currentFunc,
            self.quad,
            self.memoryManager,
            self.memScope,
            self.constTable
        )
        
        self.tempVar=self.tempVar+1
    
    # identificadores Declaracion
    @_('ID save_id_table identificadoresDec2')
    def identificadoresDec(self, p):
        pass

    @_('')
    def save_id_table(self, p):
        self.currentId = p[-1]
        
    @_('"[" INTNUMBER "]" arraySetArray identificadoresDec2')
    def identificadoresDec2(self, p):
        self.isArray = False
        self.dim = 0
        self.dimR = 1

    # embedded action save22
    @_('')
    def arraySetArray(self, p):
        if not self.dataTable.getTable(self.currentFunc).existVar(self.currentId):
            mem = self.memoryManager.get(MEM[self.memScope][self.currentType.upper()])
            self.currentMem = mem
            self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType, mem)
            self.dataTable.addNumLocals(self.currentFunc)
        
        self.isArray = True
        self.dim += 1
        lim = p[-2]

        self.dataTable.getTable(self.currentFunc).dimStoreLim(self.currentId, 1, lim)
        self.dimR = ( lim ) * self.dimR
        print("DIMR",self.dimR)
        #self.dataTable.getTable(self.currentFunc).dimStoreDimR(self.currentId,self.dimR)


    @_('empty')
    def identificadoresDec2(self, p):
        if self.isArray:
            size = self.dimR
            for i in range(0, self.dim):
                self.dimR = self.dataTable.getTable(self.currentFunc).dimStoreMi(self.currentId, i, self.dimR)
            
            self.memoryManager.setNext(MEM[self.memScope][self.currentType.upper()],size)
            self.dataTable.getTable(self.currentFunc).dimStoreDimR(self.currentId,size)
        else:
            mem = self.memoryManager.get(MEM[self.memScope][self.currentType.upper()],1)
            self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType, mem)
            self.dataTable.addNumLocals(self.currentFunc)
        
    #CODE ID1
    # identificadores con dimension
    @_('ID dim_push identificadores2')
    def identificadores(self, p):   
        self.currentId = p.ID
        pastId = self.currentId
        mem = self.dataTable.getAddressVar(self.currentId,self.currentFunc)
        type = self.dataTable.getTypeVar(self.currentId, self.currentFunc)
        #CODIGOROJO
        d = self.dataTable.getCompleteDimentions(self.currentFunc,self.currentId)
        isArray = self.pilaIsArray.pop()

        #dime = self.dataTable.getTable(self.currentFunc).getDimentions(p.ID)
        
        if not self.badAid.isdigit() and self.pilaOper.top() != '(' and not isArray :
            memTemp = self.memoryManager.get(MEM[self.memScope]["TEMP"][type.upper()],1)
            if test:
                self.quad.add(self.badAid,self.currentId,None,temp)
            else:
                self.quad.add(self.badAid,mem,None,memTemp)
            '''
            else:
                memTemp = self.memoryManager.get(MEM[self.memScope]["TEMP"][type.upper()],1)
                self.memoryManager.setNext(MEM[self.memScope]["TEMP"][self.currentType.upper()],self.dataTable.getTable(self.currentFunc).getDimR(self.pilaOper.top()))
            '''
            temp = 't' + str(self.tempVar)
            
            self.badAid= '0'
            self.currentId= temp
            self.tempVar = self.tempVar + 1
            mem = memTemp
            self.currentMem = mem

        if not isArray:
            pushOperandType(
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.currentId, 
                self.dataTable.getTypeVar(pastId, self.currentFunc),
                mem,
                d)
            self.currentMem = mem
        else:
            #falta
            '''
            pushOperandType(
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.currentId, 
                self.dataTable.getTypeVar(pastId, self.currentFunc),
                mem,
                [])
            '''
        #print("PILASSSSSSSSSSSSSSSSSS 3")
        #print(pastId)
        #self.quad.print()
        #self.pilaMemoria.print()
        #self.pilaOper.print()
        #print("PILASSSSSSSSSSSSSSSSSS 3")
        

    #CODE: ID2
    #This part of identifiers checks for dimentions and stores them
    @_('"[" dim_cor_start exp "]" dim_cor_end dimGenQuad identificadores2')
    def identificadores2(self, p):
        pass

    #add dim to stack and dim Count
    #used on ID1
    @_('')
    def dim_push(self, p):
        self.pilaDim.push(p[-1])
        self.pilaDimCount.push(0)
        self.pilaIsArray.push(False)

    #update dim 
    #used on ID2
    @_('')
    def dim_cor_start(self, p):
        #verify id has dim
        var = self.pilaDim.top()
        self.dataTable.getTable(self.currentFunc).hasDim(var)
        
        if not self.pilaIsArray.top():
            self.pilaIsArray.pop()
            self.pilaIsArray.push(True)
        dimCount = self.pilaDimCount.top()
        self.pilaDimCount.push(dimCount + 1)
        self.pilaOp.push(p[-1])

    #resolve exp 
    #used on ID2
    @_('')
    def dim_cor_end(self, p):
        expQuads(
                "[",
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope,
                self.constTable
            )
        self.tempVar = self.tempVar + 1
    
    #create verify quad, and add mi quad 
    #used on ID2
    @_('')
    def dimGenQuad(self, p):
        var = self.pilaDim.top()
        dim = self.pilaDimCount.top()
        limCte = self.dataTable.getTable(self.currentFunc).dimGetLim(var,dim)
        
        if self.constTable.existVar(limCte):
            mem = self.constTable.getAddress(limCte)
        else:
            mem = self.memoryManager.get(MEM['CONST']['INT'],1)
            self.constTable.insert(limCte,'int', mem)
        
        if test:
            verQuad(self.pilaOper, self.pilaType, self.pilaMemoria, limCte, self.quad)
        else:
            verQuad(self.pilaOper, self.pilaType, self.pilaMemoria, mem, self.quad)

        if self.dataTable.getTable(self.currentFunc).isNextDim(var, dim):
            miCte = self.dataTable.getTable(self.currentFunc).dimGetMi(var, dim)
            if self.constTable.existVar(miCte):
                mi = self.constTable.getAddress(miCte)
            else:
                mi = self.memoryManager.get(MEM['CONST']['INT'],1)
                self.constTable.insert(miCte,'int', mi)
                
            miDimQuad(
                mi,
                self.tempVar,
                self.pilaOper,
                self.pilaType, 
                self.pilaMemoria,
                self.pilaDimGlob,
                self.memoryManager, 
                self.memScope,
                self.quad
                )
            
            self.tempVar += 1
        if dim > 1:
            miAddQuad(
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.tempVar,
                self.memoryManager,
                self.memScope,
                self.quad
                )
            self.tempVar += 1
    
    @_('empty')
    def identificadores2(self, p):
        if self.pilaIsArray.top():
            var = self.pilaDim.top()
            addBaseCte = self.dataTable.getTable(self.currentFunc).getAddress(var)
            varType = self.dataTable.getTypeVar(var, self.currentFunc)

            if self.constTable.existVar(addBaseCte):
                address = self.constTable.getAddress(addBaseCte)
            else:
                address = self.memoryManager.get(MEM['CONST']['INT'],1)
                self.constTable.insert(addBaseCte,'int', address)
            
            dimAddressQuad(
                address,
                varType,
                self.pilaOper,
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.tempVar,
                self.memoryManager,
                self.memScope,
                self.quad
                )

            self.currentMem = self.pilaMemoria.top()
            
            #Get error if variable is missing dimensions
            if self.dataTable.getTable(self.currentFunc).isNextDim(var, self.pilaDimCount.top()):
                dimErr(var)
            
            #save13
            if not self.badAid.isdigit():
                mem = self.memoryManager.get(MEM[self.memScope]['TEMP'][self.pilaType.top().upper()],1)
                #CODIGOROJO
                d = self.dataTable.getCompleteDimentions(self.currentFunc, var)
                self.quad.add(
                            self.badAid,
                            self.pilaMemoria.top(),
                            None,
                            mem
                        )
                self.badAid= '0'
                self.currentId= 't' + str(self.tempVar)
                self.currentMem = mem
                self.tempVar = self.tempVar + 1
                self.pilaMemoria.pop()
                self.pilaMemoria.push(mem)
                self.pilaDimGlob.push(d)
        
        self.pilaDim.pop()
        self.pilaDimCount.pop()

    # TIPO
    @_('INT')
    def tipo(self, p):
        self.currentType = 'int'
        return 'int'

    @_('CHAR')
    def tipo(self, p):
        self.currentType = 'char'
        return 'char'

    @_('FLOAT')
    def tipo(self, p):
        self.currentType = 'float'
        return 'float'

    # OR
    @_('expAND expOR2')
    def expOR(self, p):
        pass

    @_('OR push_or expOR push_or2')
    def expOR2(self, p):
        pass

    @_('empty')
    def expOR2(self, p):
        pass

    @_('')
    def push_or(self, p):
        self.pilaOp.push('|')
        
    @_('')
    def push_or2(self, p):
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope,
            self.constTable
        )

    # AND
    @_('expresion expAND2')
    def expAND(self, p):
        pass

    @_('AND push_and expAND push_and2')
    def expAND2(self, p):
        pass

    @_('empty')
    def expAND2(self, p):
        pass
    
    @_('')
    def push_and(self, p):
        self.pilaOp.push('&')
        
    @_('')
    def push_and2(self, p):
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope,
            self.constTable
        )

        self.tempVar = self.tempVar + 1
        pass
    
    #EXPRESION

    @_('exp expresion2 quad_expresion')
    def expresion(self, p):
        pass

    @_('')
    def quad_expresion(self, p):
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.pilaDimGlob,
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope,
            self.constTable
        )

        self.tempVar = self.tempVar + 1

    @_( 'LT push_bool_op exp',
        'GT push_bool_op exp',
        'EQ push_bool_op exp',
        'ELT push_bool_op exp',
        'EGT push_bool_op exp',
        'NE push_bool_op exp')
    def expresion2(self, p):
        pass

    @_('')
    def push_bool_op(self, p):
        self.pilaOp.push(p[-1])

    @_('empty')
    def expresion2(self, p):
        pass

    @_('termino exp2')
    def exp(self, p):
        if self.pilaOper.length()>1 and self.pilaOp.top() == "+" or self.pilaOp.top() == "-" or self.pilaOp.top() == "/" or self.pilaOp.top() == "*" :
            normalQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope,
                self.constTable
            )

    @_('PLUS exp_op_insert exp',
        'MINUS exp_op_insert exp')
    def exp2(self, p):
        pass

    @_('')
    def exp_op_insert(self, p):
        if self.pilaOper.length() > 1:
            if self.pilaOp.top() == "/" or self.pilaOp.top() == "*":
                while self.pilaOp.top() == "/" or self.pilaOp.top() == "*":
                    normalQuad(
                        self.pilaOp,
                        self.pilaOper, 
                        self.pilaType,
                        self.pilaMemoria,
                        self.pilaDimGlob,
                        self.quad,
                        self.tempVar,
                        self.dataTable,
                        self.currentFunc,
                        self.memoryManager,
                        self.memScope,
                        self.constTable
                    )
                    self.tempVar = self.tempVar + 1
            if self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                while self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                    normalQuad(
                        self.pilaOp,
                        self.pilaOper, 
                        self.pilaType,
                        self.pilaMemoria,
                        self.pilaDimGlob,
                        self.quad,
                        self.tempVar,
                        self.dataTable,
                        self.currentFunc,
                        self.memoryManager,
                        self.memScope,
                        self.constTable
                    )
                    self.tempVar = self.tempVar + 1
        self.pilaOp.push(p[-1])
        

    @_('empty')
    def exp2(self, p):
        pass

    # factor
    @_('"(" exp_par_start exp ")" exp_par_end ')
    def factor(self, p):
        return p.exp

    @_('')
    def exp_par_start(self, p):
        self.pilaOp.push(p[-1])

    @_('')
    def exp_par_end(self, p):
        while self.pilaOp.top() != '(':
            normalQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.pilaDimGlob,
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope,
                self.constTable
            )
            self.tempVar = self.tempVar + 1
        self.pilaOp.pop()

    @_('PLUS plus_varcte varcte')
    def factor(self, p):
        pass

    @_('MINUS minus_varcte varcte')
    def factor(self, p):
        pass
    
    @_('')
    def plus_varcte(self, p):
        self.badAid = '+'
    
    @_('')
    def minus_varcte(self, p):
        self.badAid = '-'
        
    @_('varcte')
    def factor(self, p):
        return p[0]
        pass
        
    #OPMAT save00
    @_('factor opmat2')
    def opmat(self, p):
        if p.opmat2:
            if(self.dataTable.getTable(self.currentFunc).getDimentions(self.currentId) == 0):
                varNotArray(self.currentId)
            else:
                dimR = self.dataTable.getTable(self.currentFunc).getDimR(self.pilaOper.top())
                print("dimr",dimR, self.pilaOper.top())
                mem = self.memoryManager.get(MEM[self.memScope]["TEMP"][self.pilaType.top().upper()],dimR)
                dimQuad(
                        self.currentId, 
                        self.pilaDimGlob.top(),
                        self.memScope, 
                        self.constTable, 
                        self.memoryManager,
                        self.quad,
                    )

                if p.opmat2 == '?':
                    self.pilaDimGlob.pop()
                    self.pilaDimGlob.push([])
                    
                self.quad.add(
                            p.opmat2,
                            self.pilaMemoria.pop(),
                            None,
                            mem
                        )
                self.badAid= '0'
                self.currentId= 't' + str(self.tempVar)
                self.currentMem = mem
                self.pilaMemoria.pop()
                self.pilaMemoria.push(mem)
                
                self.tempVar = self.tempVar + 1
            
        else:
            return p.factor


    @_('TRANSPOSE', 
    'INVERSE', 
    'DETERMINANT')
    def opmat2(self, p):
        return p[0]

    @_('empty')
    def opmat2(self, p):
        pass

    # TERMINO

    @_('opmat termino2')
    def termino(self, p):
        return p.opmat
        pass
        
    @_('TIMES term_op_insert termino',
       'DIVIDE term_op_insert termino')
    def termino2(self, p):
        pass
    
    @_('')
    def term_op_insert(self, p):
        op = self.pilaOp.top()
        if self.pilaOp.length() > 1:
            if op == "/" or op == "*":
                normalQuad(
                    self.pilaOp,
                    self.pilaOper, 
                    self.pilaType,
                    self.pilaMemoria,
                    self.pilaDimGlob,
                    self.quad, 
                    self.tempVar,
                    self.dataTable,
                    self.currentFunc,
                    self.memoryManager,
                    self.memScope,
                    self.constTable
                )
                self.tempVar = self.tempVar + 1
        self.pilaOp.push(p[-1])
        
    @_('empty')
    def termino2(self, p):
        pass

    # LLAMADA save14
    @_('ID era_call "(" call_par_start llamada2 ")" exp_par_end')
    def llamada(self, p):
        param = self.pilaparamCount.pop()
        validParamLen(param - 1, len(self.dataTable.getParams(self.pilaCallId.top())), self.pilaCallId.top())
        self.quad.add("GOSUB", p.ID, None, None)
        funcType = self.dataTable.getType(self.pilaCallId.top())
        if funcType != 'void':
            m = self.dataTable.getAddressVar(p.ID, "global")
            #dosent need dimention change nvm it did idiot
            self.pilaDimGlob.push([])
            callAssignQuad(p.ID, funcType, self.tempVar, self.pilaType, self.pilaOper, self.pilaMemoria, m, self.memoryManager, self.memScope, self.quad)
            self.tempVar = self.tempVar + 1
            if not self.badAid.isdigit():
                #si algo esta fallando modifique esto porque segun yo le faltaba temp al mem
                mem = self.memoryManager.get(MEM[self.memScope]["TEMP"][self.pilaType.top().upper()],1)
                #dosent need a dimention change
                self.quad.add(
                            self.badAid,
                            self.pilaMemoria.pop(),
                            None,
                            mem
                        )
                self.badAid= '0'
                self.currentId= 't' + str(self.tempVar)
                self.currentMem = mem
                self.pilaMemoria.pop()
                self.pilaMemoria.push(mem)
                self.tempVar = self.tempVar + 1
        self.pilaCallId.pop()
            
    #embedded action
    @_('')
    def era_call(self, p):
        self.pilaCallId.push(p[-1])
        self.pilaparamCount.push(1)
        eraQuad(self.dataTable, self.pilaCallId.top(), self.quad)

    @_('')
    def call_par_start(self, p):
        self.pilaOp.push("(")

    @_('')
    def call_par_end(self, p):
        
        expQuads('(',self.pilaOp,self.pilaOper, self.pilaType,self.pilaMemoria, self.pilaDimGlob ,self.quad, self.tempVar,self.dataTable,self.currentFunc,self.memoryManager,self.memScope,self.constTable)
        self.tempVar = self.tempVar + 1

    @_('exp param_call llamada3')
    def llamada2(self, p):
        pass

    @_('empty')
    def llamada2(self, p):
        pass

    #embedded action
    @_('')
    def param_call(self, p):
        param = self.pilaparamCount.pop()
        paramQuad(self.pilaType, self.pilaOper, self.pilaMemoria, self.pilaDimGlob, self.dataTable, self.pilaCallId.top(), self.quad, param)
        self.pilaparamCount.push(param + 1)

    @_('"," call_par_end call_par_start llamada2')
    def llamada3(self, p):
        pass

    @_('empty')
    def llamada3(self, p):
        pass

    # VARCTE
    @_('identificadores')
    def varcte(self, p):
        pass

#save4
    @_('INTNUMBER')
    def varcte(self, p):
        self.isConst = True
        cte = p[0]
        pastId = cte

        memConst = None
        
        if self.constTable.existVar(cte):
            memConst = self.constTable.getAddress(cte)
        else:
            memConst = self.memoryManager.get(MEM['CONST']['INT'],1)
            self.constTable.insert(cte,'int', memConst)
        
        if not self.badAid.isdigit() and self.pilaOp.top() != '(' and not self.pilaIsArray.top():
            temp = 't' + str(self.tempVar)
            memTemp = self.memoryManager.get(MEM[self.memScope]["TEMP"]['INT'],1)

            if test:
                self.quad.add(self.badAid,cte,None,temp)
            else:
                self.quad.add(self.badAid,memConst,None,memTemp)
                
            memConst = memTemp
            self.badAid= '0'
            pastId= temp
            self.tempVar = self.tempVar + 1
            self.isConst = False
            
        pushOperandType(self.pilaOper,self.pilaType,self.pilaMemoria,self.pilaDimGlob,pastId,"int",memConst,[])
        self.currentId = pastId
        self.currentMem = memConst
        self.currentType = "int"
        
    @_('CHARACTER')
    def varcte(self, p):
        cte = p[0]
        memConst = None
        
        if self.constTable.existVar(cte):
            memConst = self.constTable.getAddress(cte)
        else:
            memConst = self.memoryManager.get(MEM['CONST']['CHAR'],1)
            self.constTable.insert(cte,'char', memConst)

        self.isConst = True
        if not self.badAid.isdigit():
            cantAssign(self.badAid, "'" + cte + "'")
            
        pushOperandType(self.pilaOper,self.pilaType,self.pilaMemoria,self.pilaDimGlob,cte,"char",memConst,[])
        
        self.currentId = cte
        self.currentType = "char"
        self.currentMem = memConst
        
    @_('FLOATNUMBER')
    def varcte(self, p):
        self.isConst = True
        cte = p[0]
        pastId = cte

        memConst = None

        if self.constTable.existVar(cte):
            memConst = self.constTable.getAddress(cte)
        else:
            memConst = self.memoryManager.get(MEM['CONST']['FLOAT'],1)
            self.constTable.insert(cte,'float', memConst)

        if not self.badAid.isdigit() and self.pilaOp.top() != '(' and not self.pilaIsArray.top():
            temp = 't' + str(self.tempVar)
            memTemp = self.memoryManager.get(MEM[self.memScope]["TEMP"]['FLOAT'],1)

            if test:
                self.quad.add(self.badAid,cte,None,temp)
            else:
                self.quad.add(self.badAid,memConst,None,memTemp)

            memConst = memTemp
            self.badAid= '0'
            pastId= temp
            self.tempVar = self.tempVar + 1
            self.isConst = False
        
        pushOperandType(self.pilaOper,self.pilaType,self.pilaMemoria,self.pilaDimGlob,pastId,"float",memConst,[])
        self.currentId = pastId
        self.currentType = "float"
        self.currentMem = memConst
        
    @_('llamada')
    def varcte(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        raise Exception("Error on line {} on {}".format(p.lineno, p.value))

    def printParser(self):
        print("dataTable:")
        self.dataTable.print()
        print("quadruple:")
        self.quad.print()
        print(self.constTable.table)