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

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = CalcLexer.tokens
    
    def printTokens(self):
        for x in self.dataTable.table:
            self.dataTable.getTable(x).print()

    precedence = (
        ('left', PLUS, MINUS),
    )

    def __init__(self):
        self.dataTable = DirFunc()
        self.constTable = VarTable()
        self.pilaOp = stack.Stack()
        self.pilaOper = stack.Stack()
        self.pilaType = stack.Stack()
        self.pilaMemoria = stack.Stack()
        self.pilaJump = stack.Stack()
        self.pilaForOp = stack.Stack()
        self.pilaForGo = stack.Stack()
        self.pilaCallId = stack.Stack()
        self.pilaparamCount = stack.Stack()
        self.quad = Quad()
        self.tempVar = 0
        self.badAid = '0'
        self.isConst = False

        self.currentId = None
        self.currentType = None
        self.currentFunc = None
        self.globalFunc = None

        self.memScope = "GLOBAL"
        self.currentMemory = -1
        self.memoryManager = MemoryManager()

        self.dim = 0
        self.dimR = 1
        self.isArray = False
        
    #PROGRAMA
    @_('PROGRAM ID set_global ";" programa2 programa3 PRINCIPAL set_principal_quad "(" ")" bloque')
    def programa(self, p):
        self.quad.add("END",None,None, None)
    
    #embedded action
    @_('')
    def set_global(self, p):
        self.dataTable.insert("global", "void")
        self.globalFunc = "global"
        self.currentFunc = "global"
        gotoSimpleQuad(self.quad, self.pilaJump)

    #embedded action
    @_('')
    def set_principal_quad(self, p):
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
        self.dataTable.getTable(self.currentFunc).insert(p[-1],p[-2],mem)
        self.dataTable.insertParam(self.currentFunc, p[-2][0])
        print(self.dataTable.getParams(self.currentFunc))
        
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

    #estatuto
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

    #assignacion
    @_('identificadores asignacion_insert_var ASSIGN exp asignacion_pop_all ";"')
    def asignacion(self, p):
        pass

    #embedded action save4
    @_('')
    def asignacion_insert_var(self, p):
        t = self.dataTable.getTypeVar(self.currentId, self.currentFunc)
        m = self.dataTable.getAdressVar(self.currentId,self.currentFunc)
        pushOperandType(self.pilaOper, self.pilaType, self.pilaMemoria, self.currentId, t, m)
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
                    self.quad, 
                    self.tempVar,
                    self.dataTable,
                    self.currentFunc,
                    self.memoryManager,
                    self.memScope
                    )
                self.tempVar = self.tempVar + 1

            else:
                assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.quad)
            
    #lee
    @_('READ "(" lee2 ")" ";"')
    def lee(self, p):
        pass

    @_('identificadores lee_quad lee3')
    def lee2(self, p):
        pass

    @_('')
    def lee_quad(self, p):
        print(self.currentId, self.currentFunc)
        if self.dataTable.existVar(self.currentId, self.currentFunc):
            mem = self.dataTable.getAdressVar(self.currentId, self.currentFunc)
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
        if test:
            printQuad(oper, self.quad)
        else:
            printQuad(m, self.quad)
        
    @_('')
    def print_quad2(self, p):
        self.constTable.insert(p[-1],"string",self.memoryManager.get(MEM["CONST"]["STRING"],1))
        printQuad(self.memoryManager.get(MEM["CONST"]["STRING"],1), self.quad)
        
    @_('')
    def print_next(self, p):
        printQuad(' ', self.quad)

    #regresa
    @_('RETURN "(" exp ")" ";"')
    def regresa(self, p):
        returnQuad(self.pilaType, self.pilaOper, self.pilaMemoria , self.dataTable, self.currentFunc, self.quad)

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
        m = self.dataTable.getAdressVar(self.currentId,self.currentFunc)
        self.pilaForOp.push(self.currentId)
        self.pilaOper.push(self.currentId)
        self.pilaMemoria.push(m)
        self.pilaType.push('int')
        self.pilaOp.push('=')
    
    #embeded action
    @_('')
    def from_assign(self, p):
        self.quad.print()
        assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.quad)
        
    #embeded action
    @_('')
    def from_gotF(self, p):
        m = self.dataTable.getAdressVar(self.pilaForOp.top(),self.currentFunc)
        self.pilaOper.push(self.pilaForOp.top())
        self.pilaOp.push('>')
        self.pilaType.push('int')
        self.pilaMemoria.push(m)
        
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.quad,
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope
        )
        self.tempVar= self.tempVar +1
        self.pilaJump.push(self.quad.getCount())
        self.pilaJump.push(self.quad.getCount())
        self.quad.add("GOTOF", self.pilaMemoria.top(), None, None)
        
    @_('')
    def from_goto(self, p):
        gotoQuadFor(
            self.quad,
            self.pilaJump
        )
        
        self.pilaJump.push(self.pilaJump.pop())
        fillGotoQuad(
            self.quad,
            self.pilaJump
        )

    @_('')
    def from_suma(self, p):
        self.pilaOper.push(self.pilaForOp.top())
        self.pilaType.push('int')
        self.pilaOper.push(1)
        self.pilaType.push('int')
        self.pilaOp.push('+')
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.quad,
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope
        )
        
        self.pilaOper.push(self.pilaForOp.pop())
        self.pilaType.push('int')
        self.pilaOper.push('t'+str(self.tempVar))
        self.pilaType.push('int')
        self.pilaOp.push('=')
        assignQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.quad)
        
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

    # embedded action
    @_('')
    def arraySetArray(self, p):
        if not self.dataTable.getTable(self.currentFunc).existVar(self.currentId):
            mem = self.memoryManager.get(MEM[self.memScope][self.currentType.upper()])
            self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType, mem)
            self.dataTable.addNumLocals(self.currentFunc)
        
        self.isArray = True
        self.dim += 1
        lim = p[-2]

        self.dataTable.getTable(self.currentFunc).dimStoreLim(self.currentId, 1, lim)
        self.dimR = (lim + 1 ) * self.dimR

    @_('empty')
    def identificadoresDec2(self, p):
        if self.isArray:
            size = self.dimR
            for i in range(0, self.dim):
                self.dimR = self.dataTable.getTable(self.currentFunc).dimStoreMi(self.currentId, i, self.dimR)
            
            self.memoryManager.setNext(MEM[self.memScope][self.currentType.upper()],size)
            self.dataTable.print()
        else:
            mem = self.memoryManager.get(MEM[self.memScope][self.currentType.upper()],1)
            self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType, mem)
            self.dataTable.addNumLocals(self.currentFunc)
        
    # identificadores con dimension
    @_('ID identificadores2')
    def identificadores(self, p):
        self.currentId = p.ID
        
    @_('"[" exp "]" identificadores2')
    def identificadores2(self, p):
        self.dataTable.print()
    
    @_('empty')
    def identificadores2(self, p):
        pass

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
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope
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
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope
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
            self.quad, 
            self.tempVar,
            self.dataTable,
            self.currentFunc,
            self.memoryManager,
            self.memScope
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
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope)

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
                        self.quad,
                        self.tempVar,
                        self.dataTable,
                        self.currentFunc,
                        self.memoryManager,
                        self.memScope
                    )
                    self.tempVar = self.tempVar + 1
            if self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                while self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                    normalQuad(
                        self.pilaOp,
                        self.pilaOper, 
                        self.pilaType,
                        self.pilaMemoria,
                        self.quad,
                        self.tempVar,
                        self.dataTable,
                        self.currentFunc,
                        self.memoryManager,
                        self.memScope
                    )
                    self.tempVar = self.tempVar + 1
        self.pilaOp.push(p[-1])
        

    @_('empty')
    def exp2(self, p):
        pass

    # factor
    @_('"(" exp_par_start exp ")" exp_par_end ')
    def factor(self, p):
        # self.pilaOper.push(p.exp)
        return p.exp

    @_('')
    def exp_par_start(self, p):
        self.pilaOp.push(p[-1])

    @_('')
    def exp_par_end(self, p):
        self.pilaOper.print()
        while self.pilaOp.top() != '(':
            normalQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope
            )
            self.tempVar = self.tempVar + 1
        self.pilaOp.pop()
        self.pilaOper.print()

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
        
    #OPMAT
    @_('factor opmat2')
    def opmat(self, p):
        if p.opmat2:
            print("opmat")
        else:
            return p.factor
        
    @_('TRANSPOSE', 
    'INVERSE', 
    'DETERMINANT')
    def opmat2(self, p):
        pass

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
                    self.quad, 
                    self.tempVar,
                    self.dataTable,
                    self.currentFunc,
                    self.memoryManager,
                    self.memScope
                )
                self.tempVar = self.tempVar + 1
        self.pilaOp.push(p[-1])
        
    @_('empty')
    def termino2(self, p):
        pass

    # LLAMADA    
    @_('ID era_call "(" call_par_start llamada2 ")" exp_par_end')
    def llamada(self, p):
        param = self.pilaparamCount.pop()
        validParamLen(param - 1, len(self.dataTable.getParams(self.pilaCallId.top())), self.pilaCallId.top())
        self.quad.add("GOSUB", p.ID, None, None)
        funcType = self.dataTable.getType(self.pilaCallId.top())
        if funcType != 'void':
            m = self.dataTable.getAdressVar(p.ID, "global")
            callAssignQuad(p.ID, funcType, self.tempVar, self.pilaType, self.pilaOper, self.pilaMemoria, m, self.memoryManager, self.memScope, self.quad)
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
        self.pilaOper.print()
        while self.pilaOp.top() != '(':
            normalQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.pilaMemoria,
                self.quad, 
                self.tempVar,
                self.dataTable,
                self.currentFunc,
                self.memoryManager,
                self.memScope
            )
            self.tempVar = self.tempVar + 1
        self.pilaOp.pop()
        self.pilaOper.print()

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
        paramQuad(self.pilaType, self.pilaOper, self.pilaMemoria, self.dataTable, self.pilaCallId.top(), self.quad, param)
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
        pastId = self.currentId
        mem = self.dataTable.getAdressVar(self.currentId,self.currentFunc)
        
        if not self.badAid.isdigit():
            self.quad.add(
                        self.badAid,
                        self.currentId,
                        None,
                        't' + str(self.tempVar)
                    )
            self.badAid= '0'
            mem = self.memoryManager.get(MEM[self.memScope]['INT'],1)
            self.currentId= 't' + str(self.tempVar)
            self.tempVar = self.tempVar + 1
        
        pushOperandType(
            self.pilaOper, 
            self.pilaType,
            self.pilaMemoria,
            self.currentId, 
            self.dataTable.getTypeVar(pastId, self.currentFunc),
            mem)

#save4
    @_('INTNUMBER')
    def varcte(self, p):
        pastId = p[0]
        mem = None
        
        if self.constTable.existVar(p[0]):
            mem = self.constTable.getAdress(p[0])
        else:
            mem = self.memoryManager.get(MEM['CONST']['INT'],1)
            self.constTable.insert(p[0],'int', mem)

        self.isConst = True
        if not self.badAid.isdigit():
            self.quad.add(
                        self.badAid,
                        p[0],
                        None,
                        't' + str(self.tempVar)
                    )
            self.badAid= '0'
            mem = self.memoryManager.get(MEM[self.memScope]['INT'],1)
            pastId= 't' + str(self.tempVar)
            self.tempVar = self.tempVar + 1
            self.isConst = False
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            self.pilaMemoria,
            pastId,
            "int",
            mem
        )
        self.currentId = pastId
        self.currentType = "int"
        
    @_('CHARACTER')
    def varcte(self, p):
        pastId = p[0]
        mem = None
       
        if self.constTable.existVar(p[0]):
            mem = self.constTable.getAdress(p[0])
        else:
            mem = self.memoryManager.get(MEM['CONST']['CHAR'],1)
            self.constTable.insert(p[0],'char', mem)

        self.isConst = True
        if not self.badAid.isdigit():
            self.quad.add(
                        self.badAid,
                        self.currentId,
                        None,
                        't' + str(self.tempVar)
                    )
            self.badAid= '0'
            mem = self.memoryManager.get(MEM[self.memScope]['CHAR'],1)
            self.currentId= 't' + str(self.tempVar)
            self.tempVar = self.tempVar + 1
            self.isConst = False
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            self.pilaMemoria,
            pastId,
            "char",
            mem
        )
        self.currentId = pastId
        self.currentType = "char"
        
    @_('FLOATNUMBER')
    def varcte(self, p):
        pastId = p[0]
        mem = None
        
        if self.constTable.existVar(p[0]):
            mem = self.constTable.getAdress(p[0])
        else:
            mem = self.memoryManager.get(MEM['CONST']['FLOAT'],1)
            self.constTable.insert(p[0],'float', mem)

        if not self.badAid.isdigit():
            self.quad.add(
                        self.badAid,
                        p[0],
                        None,
                        't' + str(self.tempVar)
                    )
            self.badAid= '0'
            mem = self.memoryManager.get(MEM[self.memScope]['FLOAT'],1)
            pastId= 't' + str(self.tempVar)
            self.tempVar = self.tempVar + 1
            self.isConst = False
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            self.pilaMemoria,
            pastId,
            "float",
            mem
        )
        self.currentId = pastId
        self.currentType = "float"
        
    @_('llamada')
    def varcte(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        raise Exception("Error on line {} on {}".format(p.lineno, p.value))

