# -----------------------------------------------------------------------------
# proyecto patito++
# AUTHORS: Mildred Gil Melchor, RAUL FLORES
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
from dataTable import *
from dicFunc import *
import copy
class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { 
        STRING, INTNUMBER, FLOATNUMBER, CHARACTER, 
        ID, VAR, PROGRAM, PRINCIPAL,
        IF, ELSE, WHILE,
        PRINT, WRITE,
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
    ID['lee'] = PRINT
    ID['escribe'] = WRITE
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
        self.currentFunc = None
        self.globalFunc = None
    
    # PROGRAMA
    @_('PROGRAM ID ";" programa2 programa3 PRINCIPAL "(" ")" bloque')
    def programa(self, p):
        # self.dataTable = DirFunc()
        self.dataTable.insert(p.ID, "void")
        self.globalFunc = p.ID
        self.currentFunc = p.ID
        # self.currentFunc.print()
        
    @_('vars')
    def programa2(self, p):
        pass

    @_('empty')
    def programa2(self, p):
        pass

    @_('funcion programa2')
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
        for x in p.ids:
            self.dataTable.getTable(self.currentFunc).insert(x, p.tipo)
        pass

    @_('var1')
    def var2(self, p):
        pass
        
    @_('empty')
    def var2(self, p):
        pass

    @_('identificadores ids2')
    def ids(self, p):
        # print('identificadores')
        # print(p.identificadores
        if (p.ids2 != None):
            return [p.identificadores, p.ids2]
        else:
            return p.identificadores
        pass

    @_('"," ids')
    def ids2(self, p):
        return p.ids
        pass

    @_('empty')
    def ids2(self, p):
        pass

    # FUNCION
    
    @_('FUNCTION funcion2 ID parametros vars bloque')
    def funcion(self, p):
        print("creating " + p.ID)
        self.dataTable.insert(p.ID,p[1])
        self.currentFunc = p.ID
        # self.dataTable.getTable(p.ID).insert('a','b')
        # self.currentFunc.insert('a','b')
        pass

    @_('tipo')
    def funcion2(self, p):
        return p.tipo

    @_('VOID')
    def funcion2(self, p):
        return 'void'

    # PARAMETROS
    
    @_('"(" parametros2 ")"')
    def parametros(self, p):
        pass

    @_('tipo ID parametros3')
    def parametros2(self, p):
        self.dataTable.getTable(self.currentFunc).insert(p.ID, p.tipo)
        pass

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

    @_('identificadores ASSIGN exp ";"')
    def asignacion(self, p):
        pass

    #lee

    @_('PRINT "(" lee2 ")" ";"')
    def lee(self, p):
        pass

    @_('identificadores  lee3')
    def lee2(self, p):
        pass

    @_('"," lee2')
    def lee3(self, p):
        pass

    @_('empty')
    def lee3(self, p):
        pass

    #escritura
    
    @_('WRITE "(" escritura2 ")" ";"')
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

    @_('IF "(" expOR ")" bloque estDesicion2')
    def estDesicion(self, p):
        pass

    @_('ELSE bloque')
    def estDesicion2(self, p):
        pass

    @_('empty')
    def estDesicion2(self, p):
        pass
    
    # estatuto de repeticion condicional

    @_('WHILE "(" expOR ")" DO bloque')
    def estRepCond(self, p):
        pass

    # estatuto de repeticion no condicional

    @_('FROM identificadores ASSIGN exp TO exp DO2 bloque')
    def estRepNoCond(self, p):
        pass
    
    # identificadores

    @_('ID identificadores2')
    def identificadores(self, p):
        return p.ID
        pass

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
        return 'int'

    @_('CHAR')
    def tipo(self, p):
        return 'char'

    @_('FLOAT')
    def tipo(self, p):
        return 'float'

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

    @_('exp expresion2')
    def expresion(self, p):
        pass

    @_('LT exp')
    def expresion2(self, p):
        pass

    @_('GT exp')
    def expresion2(self, p):
        pass

    @_('EQ exp')
    def expresion2(self, p):
        pass

    @_('ELT exp')
    def expresion2(self, p):
        pass

    @_('EGT exp')
    def expresion2(self, p):
        pass

    @_('NE exp')
    def expresion2(self, p):
        pass

    @_('empty')
    def expresion2(self, p):
        pass

    #exp

    @_('termino exp2')
    def exp(self, p):
        pass

    @_('PLUS exp')
    def exp2(self, p):
        pass

    @_('MINUS exp')
    def exp2(self, p):
        pass

    @_('empty')
    def exp2(self, p):
        pass

    # factor

    @_('"(" exp ")"')
    def factor(self, p):
        pass

    @_('PLUS varcte')
    def factor(self, p):
        pass

    @_('MINUS varcte')
    def factor(self, p):
        pass

    @_('varcte')
    def factor(self, p):
        return p[0]
        pass

    #OPMAT
    @_('factor opmat2')
    def opmat(self, p):
        pass

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

    @_('TIMES termino')
    def termino2(self, p):
        pass

    @_('DIVIDE termino')
    def termino2(self, p):
        pass

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
        return p[0]
        pass

    @_('INTNUMBER')
    def varcte(self, p):
        return p[0]
        pass

    @_('CHARACTER')
    def varcte(self, p):
        return p[0]
        pass

    @_('FLOATNUMBER')
    def varcte(self, p):
        return p[0]
        pass

    @_('llamada')
    def varcte(self, p):
        return p[0]
        pass

    @_('')
    def empty(self, p):
        pass
