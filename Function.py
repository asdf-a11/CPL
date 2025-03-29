import Lexer
from Util import il
#import IRConversion
import IR
import ParseFunction

class Function():
    def __init__(self, name=None , returnTypeList=[], perameterTypeList=[], perameterNameList=[], tokenList=[]):
        self.name = name
        self.returnTypeList = returnTypeList
        self.perameterTypeList = perameterTypeList
        self.perameterNameList = perameterNameList
        self.tokenList = tokenList
        self.IRList = []
        self.convertedIRList = []
    def CreateArguments(self):
        instList = []
        for i in range(0, len(self.perameterNameList)):
            instList.append(IR.Instruction("CREATE_ARGUMENT", [self.perameterTypeList[i], self.perameterNameList[i]]))
        return instList
    def GenerateIR(self):
        self.IRList = []
        #1st function name
        #2nd return type list
        #3rd param type, name list
        paramList = [self.name, "", ""]
        for i in range(len(self.perameterNameList)):
            paramList[2] += self.perameterTypeList[i] + "~"
            paramList[2] += self.perameterNameList[i] + ("~" if i != len(self.perameterNameList)-1 else "")
        if len(self.perameterNameList) == 0:
            paramList[2] += "void"
        for i in range(len(self.returnTypeList)):
            paramList[1] += self.returnTypeList[i] + ("~" if i != len(self.returnTypeList)-1 else "")
        if len(self.returnTypeList) == 0:
            paramList[1] += "void"
        self.IRList.append(IR.Instruction("CREATE_FUNCTION", paramList))
        self.IRList.append(IR.Instruction("OPENSCOPE"))
        self.IRList += self.CreateArguments()
        self.IRList += ParseFunction.GenerateIR(self.tokenList)
        self.IRList.append(IR.Instruction("CLOSESCOPE"))
        self.IRList.append(IR.Instruction("END_FUNCTION"))
    def WriteConvertedIRToFile(self, filePath):
        f = open(filePath, "w")
        for i in self.convertedIRList:
            f.write(i + "\n")
        f.close()
    def PrintTokens(self):
        print("fn ", end = "")
        for i in self.returnTypeList:
            print(i, end = " ") 
        print(" " + self.name, end = " (")
        for i in range(len(self.perameterTypeList)):
            print(self.perameterTypeList[i],self.perameterNameList[i], end = "")
            if len(self.perameterTypeList)-1 != i:
                print(", ", end = "")
        print(") { ")
        Lexer.PrintTokenList(self.tokenList)
        print("}")

