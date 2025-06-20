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
    def PrintTokens(self) -> None:
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
    def GetFunctionReturnType(self,tokenList, idx) -> int:
        #fn i32, i8, i8 functionName(i32 a, b){}
        errMsg = "Failed to find close of function when finding types"
        returnTypeList = []
        while 1:
            if il(tokenList, idx, errMsg).tokenType not in ["NAME", "TYPE"]:
                raise Exception("Expected a name or type in function return type list")
            nextToken = il(tokenList, idx, errMsg)
            returnTypeList.append(nextToken.tokenSubset)
            if il(tokenList, idx + 1, errMsg).tokenSubset != ",":
                break
            idx += 1
        if len(returnTypeList) == 0:
            raise Exception("Function must have a return type")
        self.returnTypeList = returnTypeList
        return idx + 1
    def GetFunctionParameterList(self,tokenList, idx) -> int:
        typeList = []
        nameList = []
        if tokenList[idx].tokenType != "(":
            raise Exception("Expected open bracked")
        idx += 1
        if tokenList[idx].tokenType == ")":
            return [],[], idx + 1
        while 1:
            if tokenList[idx].tokenType != "TYPE":
                if len(typeList) == 0:
                    raise Exception("Expecteed a type here")
                typeList.append(typeList[-1])
                idx -= 1
            else:
                typeList.append(tokenList[idx].tokenSubset)
            idx += 1
            if tokenList[idx].tokenType != "NAME":
                raise Exception("Expected name here")
            nameList.append(tokenList[idx].tokenSubset)
            idx += 1
            if tokenList[idx].tokenType != ",":
                if tokenList[idx].tokenType == ")":
                    break
                raise Exception("Expected }")
            idx += 1
        self.perameterNameList = nameList
        self.perameterTypeList = typeList
        return idx+1
    def ReadInScope(self,tokenList, idx) -> int:
        if tokenList[idx].tokenType != "{":
            raise Exception("Expected a { at the start of scope when readin in")
        idx += 1
        out = []
        scopeCounter = 0
        errMsg = "Failed to find end of scope before end of file"
        while 1:
            if il(tokenList, idx, errMsg).tokenType == "{":
                scopeCounter += 1
            if tokenList[idx].tokenType == "}":
                if scopeCounter == 0:
                    break
                scopeCounter -= 1
            out.append(tokenList[idx])
            idx += 1
        self.tokenList = out
        return idx

