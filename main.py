from parserLexer import CalcLexer, CalcParser
from dataTable import *
from dicFunc import *

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    filename = input("write the file name:")
    f=open(filename, "r")
    data = f.read()

    # for tok in lexer.tokenize(data):
    #     print(tok)
    
    parser.parse(lexer.tokenize(data))
    parser.dataTable.print()
    parser.printTokens()
    