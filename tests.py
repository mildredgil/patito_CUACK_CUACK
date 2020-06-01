from parserLexer import CalcLexer, CalcParser
from virtualMachine import VirtualMachine
from writer import Writer

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    #andOr
    test="andOr"
    test=["andOr","expresiones","funcion3","mientasHaz","simple_expresions","sino","array","desdeHasta"]
    for test in test:
        lexer = CalcLexer()
        parser = CalcParser()
        filename = "autotesting/vm/" + test
        f=open(filename, "r")
        data = f.read()
        parser.parse(lexer.tokenize(data))
        Writer.prepareOBJ("autotesting/new/"+test, parser)
        #check
        fn = open("autotesting/new/"+test+"_obj", "r")
        fo = open("autotesting/old/"+test+"_obj", "r")
        with open("autotesting/new/"+test+"_obj") as f1, open("autotesting/old/"+test+"_obj") as f2:
            for l1, l2 in zip(f1, f2):
                if not l1 == l2:
                    print(l1)
                    print('=/=')
                    print(l2)
                    raise Exception("File "+test+" not equal")
    