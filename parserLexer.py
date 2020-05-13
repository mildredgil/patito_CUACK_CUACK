# -----------------------------------------------------------------------------
# proyecto patito++
# AUTHORS: Mildred Gil Melchor, RAUL FLORES
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
from dataTable import *
from dataStructure import stack
from typeMatching import *
from quad import *
from stackHelpers import *

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
        self.pilaOp = stack.Stack()
        self.pilaOper = stack.Stack()
        self.pilaType = stack.Stack()
        self.pilaJump = stack.Stack()
        self.pilaForOp = stack.Stack()
        self.pilaForGo = stack.Stack()
        self.quad = Quad()
        self.tempVar = 0
        self.tempVarTable = VarTable()

        self.currentId = None
        self.currentType = None

        self.currentFunc = None
        self.globalFunc = None
    
    # PROGRAMA
    @_('PROGRAM ID set_global ";" programa2 programa3 PRINCIPAL "(" ")" bloque')
    def programa(self, p):
        pass
    
    #embedded action
    @_('')
    def set_global(self, p):
        self.dataTable.insert("global", "void")
        self.globalFunc = p[-1]
        self.currentFunc = "global"

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

    @_('identificadores set_id ids2')
    def ids(self, p):
        pass
    
    #embeded action
    @_('')
    def set_id(self, p):
        self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType)
        
    @_('"," ids')
    def ids2(self, p):
        pass

    @_('empty')
    def ids2(self, p):
        pass

    # FUNCION
    
    @_('FUNCTION funcion2 ID save_id parametros vars bloque')
    def funcion(self, p):
        pass

    #embedded action
    @_('')
    def save_id(self, p):
        #guardar funcion y tipo
        self.dataTable.insert(p[-1], self.currentType)
        self.currentFunc = p[-1]

    @_('tipo')
    def funcion2(self, p):
        pass

    @_('VOID')
    def funcion2(self, p):
        return 'void'

    # PARAMETROS
    
    @_('"(" parametros2 ")"')
    def parametros(self, p):
        pass
        
    @_('tipo ID parametros3')
    def parametros2(self, p):
        self.currentId = p.ID
        self.dataTable.getTable(self.currentFunc).insert(self.currentId,self.currentType)
        
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
        'regresa')
    def estatuto(self, p):
        pass

    #assignacion
    @_('identificadores asignacion_insert_var ASSIGN exp asignacion_pop_all ";"')
    def asignacion(self, p):
        pass

    #embedded action
    @_('')
    def asignacion_insert_var(self, p):  
        t = self.dataTable.getTypeVar(self.currentId, self.currentFunc)
        pushOperandType(self.pilaOper, self.pilaType, self.currentId, t)
        self.pilaOp.push("=")
        
    #embedded action
    @_('')
    def asignacion_pop_all(self, p):
        self.pilaOper.print()
        self.pilaOp.print()
        print("sacando")
        while self.pilaOp.length() > 0:
            if self.pilaOp.top() != "=":
                print("normal")
                normalQuad(
                    self.pilaOp,
                    self.pilaOper, 
                    self.pilaType,
                    self.quad, 
                    self.tempVar)
                self.tempVar = self.tempVar + 1

            else:
                print("assign")
                assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
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
        if self.dataTable.existVar(self.currentId, self.currentFunc):
            self.quad.add("lee", None, None, self.currentId)

    @_('"," lee2')
    def lee3(self, p):
        pass

    @_('empty')
    def lee3(self, p):
        pass

    #escritura
    
    @_('PRINT "(" escritura2 ")" ";"')
    def escritura(self, p):
        pass

    @_('exp escritura3')
    def escritura2(self, p):
        pass

    @_('STRING escritura3')
    def escritura2(self, p):
        pass

    @_('"," escritura2')
    def escritura3(self, p):
        pass

    @_('empty')
    def escritura3(self, p):
        pass

    #regresa

    @_('RETURN "(" exp ")" ";"')
    def regresa(self, p):
        pass

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
        self.pilaJump.print()
        gotoQuad(
            self.quad,
            self.pilaJump
        )
        self.pilaJump.print()
        fillGotoQuad(
            self.quad,
            self.pilaJump
        )

    # estatuto de repeticion no condicional

    @_(' FROM identificadores ASSIGN from_create exp from_assign TO exp from_gotF DO2 bloque from_suma from_goto')
    def estRepNoCond(self, p):
        pass
    
    #embeded action
    @_('')
    def from_create(self, p):
        self.pilaForOp.push(self.currentId)
        self.pilaOper.push(self.currentId)
        self.pilaType.push('int')
        self.pilaOp.push('=')

        
    
    #embeded action
    @_('')
    def from_assign(self, p):
        print("parte 2")
        # self.pilaForGo.push()
        assignQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.quad)
        self.quad.print()
        

    #embeded action
    @_('')
    def from_gotF(self, p):
        self.pilaOper.push(self.pilaForOp.top())
        self.pilaOp.push('>')
        self.pilaType.push('int')
        normalQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.quad,
            self.tempVar)
        self.tempVar= self.tempVar +1
        self.pilaJump.push(self.quad.getCount())
        self.pilaJump.push(self.quad.getCount())
        self.quad.add("GOTOF", self.pilaOper.top(), None, None)
        print('acabo desmadre')

    @_('')
    def from_goto(self, p):
        gotoQuadFor(
            self.quad,
            self.pilaJump
        )
        self.pilaJump.print()
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
            self.quad,
            self.tempVar)
        
        self.pilaOper.push(self.pilaForOp.pop())
        self.pilaType.push('int')
        self.pilaOper.push('t'+str(self.tempVar))
        self.pilaType.push('int')
        self.pilaOp.push('=')
        assignQuad(
            self.pilaOp,
            self.pilaOper, 
            self.pilaType,
            self.quad)
        
        self.tempVar=self.tempVar+1
    
    # identificadores
    @_('ID identificadores2')
    def identificadores(self, p):
        self.currentId = p.ID
        
    @_('"[" exp "]" identificadores3')
    def identificadores2(self, p):
        pass

    @_('empty')
    def identificadores2(self, p):
        pass

    @_('"[" exp "]"')
    def identificadores3(self, p):
        pass

    @_('empty')
    def identificadores3(self, p):
        pass

    # TIPO
    @_('INT')
    def tipo(self, p):
        self.currentType = 'int'

    @_('CHAR')
    def tipo(self, p):
        self.currentType = 'char'

    @_('FLOAT')
    def tipo(self, p):
        self.currentType = 'float'

    # OR
    @_('expAND expOR2')
    def expOR(self, p):
        pass

    @_('OR expOR')
    def expOR2(self, p):
        pass

    @_('empty')
    def expOR2(self, p):
        pass

    # AND
    @_('expresion expAND2')
    def expAND(self, p):
        pass

    @_('AND expAND')
    def expAND2(self, p):
        pass

    @_('empty')
    def expAND2(self, p):
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
            self.quad, 
            self.tempVar)

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

    #exp

    @_('termino exp2')
    def exp(self, p):    
        return p.termino

    @_('PLUS exp_op_insert exp',
        'MINUS exp_op_insert exp')
    def exp2(self, p):
        pass

    @_('')
    def exp_op_insert(self, p):
        print("estamos sumando")
        print("past op", self.pilaOp.top())
        print("current op", p[-1])
        if self.pilaOper.length() > 1:
            if self.pilaOp.top() == "/" or self.pilaOp.top() == "*":
                while self.pilaOp.top() == "/" or self.pilaOp.top() == "*":
                    normalQuad(
                        self.pilaOp,
                        self.pilaOper, 
                        self.pilaType,
                        self.quad,
                        self.tempVar)
                    self.tempVar = self.tempVar + 1
            if self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                while self.pilaOp.top() == "+" or self.pilaOp.top() == "-":
                    normalQuad(
                        self.pilaOp,
                        self.pilaOper, 
                        self.pilaType,
                        self.quad,
                        self.tempVar)
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
        while self.pilaOp.top() != '(':
            normalQuad(
                self.pilaOp,
                self.pilaOper, 
                self.pilaType,
                self.quad, 
                self.tempVar)
            self.tempVar = self.tempVar + 1
        self.pilaOp.pop()

    @_('PLUS varcte plus_varcte')
    def factor(self, p):
        pass

    @_('MINUS varcte plus_varcte')
    def factor(self, p):
        pass

    @_('')
    def plus_varcte(self, p):
        self.quad.add(
            p[-2],
            self.currentId,
            None,
            't' + str(self.tempVar)
        )
        self.pilaOper.push('t' + str(self.tempVar))
        self.tempVar = self.tempVar + 1
        

    @_('varcte')
    def factor(self, p):
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
        pass
        
    @_('TIMES term_op_insert termino',
       'DIVIDE term_op_insert termino')
    def termino2(self, p):
        print('estamos multiplicando')
        pass
    
    @_('')
    def term_op_insert(self, p):
        print("estamos mult")
        op = self.pilaOp.top()
        print("past op", op)
        print("current op", p[-1])
        if self.pilaOp.length() > 1:
            if op == "/" or op == "*":
                normalQuad(
                    self.pilaOp,
                    self.pilaOper, 
                    self.pilaType,
                    self.quad, 
                    self.tempVar
                )
                self.tempVar = self.tempVar + 1
        self.pilaOp.push(p[-1])
        
    @_('empty')
    def termino2(self, p):
        pass

    # LLAMADA    
    @_('ID "(" llamada2 ")"')
    def llamada(self, p):
        pass

    @_('exp llamada3')
    def llamada2(self, p):
        pass

    @_('"," llamada2')
    def llamada3(self, p):
        pass

    @_('empty')
    def llamada3(self, p):
        pass

    # VARCTE
    @_('identificadores')
    def varcte(self, p):
        pushOperandType(
            self.pilaOper, 
            self.pilaType, 
            self.currentId, 
            self.dataTable.getTypeVar(self.currentId, self.currentFunc))

    @_('INTNUMBER')
    def varcte(self, p):
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            p[0],
            "int"
        )
        self.currentId = p[0]
        self.currentType = "int"
        
    @_('CHARACTER')
    def varcte(self, p):
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            p[0],
            "char"
        )
        self.currentId = p[0]
        self.currentType = "char"
        
    @_('FLOATNUMBER')
    def varcte(self, p):
        pushOperandType(
            self.pilaOper,
            self.pilaType,
            p[0],
            "float"
        )
        self.currentId = p[0]
        self.currentType = "float"

    @_('llamada')
    def varcte(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass
