
class Writer():
    @classmethod
    def prepareOBJ(self, filename, parser):
        if not parser.quad:
            raise Exception("Quad is empty")

        f = open(filename + "_obj", "w")
        f.write("1,2,3,4,5,6\n")
        f.write("#QUAD\n")
        self.writeQuad(self, f, parser)
        f.write("#DIRFUNC\n")
        self.writeDirFunc(self,f,parser)
        f.write("#CONST\n")
        self.writeDirConst(self,f,parser)
        f.close()

    def writeQuad(self, f, parser):
        for value in parser.quad.list:
            switcher = {
                'None': '_'
            }
            
            f.write(str(value[0]) + "," + switcher.get(str(value[1]), str(value[1])) + "," + switcher.get(str(value[2]), str(value[2])) + "," + switcher.get(str(value[3]), str(value[3])) + "\n")

    def writeDirFunc(self, f, parser):
        for fun in parser.dataTable.table:
            if fun != "global" and parser.dataTable.table[fun]["type"] != "void":
                f.write(fun + "," + parser.dataTable.table[fun]["type"] + "," + parser.dataTable.table[fun]["params"] + "," + str(parser.dataTable.table[fun]["startCounter"])+ ',' + str(parser.dataTable.getTable("global").getAddress(fun)) + ','+ str(parser.dataTable.table[fun]["numLocals"])+"\n")
            else:
                f.write(fun + "," + parser.dataTable.table[fun]["type"] + "," + parser.dataTable.table[fun]["params"] + "," + str(parser.dataTable.table[fun]["startCounter"])+ ',' + "-1" + ','+ str(parser.dataTable.table[fun]["numLocals"])+"\n")
            
    def writeDirConst(self, f, parser):
        for const in parser.constTable.table:
            f.write(str(const) + "," + str(parser.constTable.table[const]["address"]) + "\n")
    