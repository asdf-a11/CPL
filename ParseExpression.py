from Util import il
import Util
import Lexer
import Operators
import IR
import Types
import copy
#import matplotlib.pyplot as plt

expLevel = 0
  
class Exp():
    def __init__(self):
        self.expTokens = None
        self.resultVar = None
    def ReadIn(self, tokenList, idx, escChar=";", oppEscChar=None):
        self.expTokens = []
        errMsg = "Failed to read in equation"
        escCharCounter = 1
        while idx < len(tokenList):
            if oppEscChar != None:
                if il(tokenList,idx,errMsg).tokenType in list(oppEscChar):
                    escCharCounter += 1
            if escChar != None:
                if il(tokenList,idx,errMsg).tokenType in list(escChar):
                    escCharCounter -= 1
                    if escCharCounter == 0:
                        break
            self.expTokens.append(tokenList[idx])
            idx += 1
        return idx
    def GenExpList(self, irList):
        self.ErrorChecking()
        tdx = 0
        def ReplaceListIndexWithTempVar(irList):
            global expLevel
            name = self.expTokens[tdx].tokenContent
            self.expTokens.pop(tdx)
            self.expTokens.pop(tdx)#pop opening [
            indexExp = Exp()
            newIdx = indexExp.ReadIn(self.expTokens, tdx, escChar="]", oppEscChar="[")
            for i in range(tdx, newIdx):
                self.expTokens.pop(tdx)

            indexTempVar = IR.Variable(expTemp=True)
            irList.append(IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN",indexTempVar.name])) 
            #Moves contents of [] into tempVar
            expLevel += 1
            newCode = indexExp.ToIasm(indexTempVar.name)
            irList += newCode
            valueTempVar = IR.Variable(expTemp=True)
            irList.append(IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN",valueTempVar.name])) 
            irList.append(IR.Instruction("[]", [valueTempVar.name, name, indexTempVar.name])) 
            '''
            tempVarName = "_#EXP_INDEX_" + str(expLevel)
            irList.append(IR.Instruction("CREATE", ["UNKNOWN",tempVarName])) 
            expLevel += 1
            newCode = indexExp.ToIasm(tempVarName)
            irList += newCode
            irList.append(IR.Instruction("*", [tempVarName, tempVarName, "VAR_TYPE_SIZE"])) 
            irList.append(IR.Instruction("LDR", [tempVarName, name, tempVarName])) 
            '''
            self.expTokens.pop(tdx)#delete closing ]
            replaceToken = Lexer.Token()
            replaceToken.tokenContent = valueTempVar.name
            replaceToken.tokenSubset = valueTempVar.name
            replaceToken.tokenType = "NAME" 
            self.expTokens.insert(tdx, replaceToken)
        def ReplaceFunctionWithTempVar(irList):
            global expLevel
            functionName = self.expTokens[tdx].tokenContent
            self.expTokens.pop(tdx)
            self.expTokens.pop(tdx)#pop opening bracket
            argumentExpList = []    
            closeBracketCounter = 0
            currentExpList = []
            while 1:
                token = self.expTokens.pop(tdx)
                if token.tokenType == "(":
                    closeBracketCounter += 1
                if token.tokenType == ")":
                    closeBracketCounter -= 1
                if closeBracketCounter == -1:
                    if len(currentExpList) > 0:
                        argumentExpList.append(currentExpList)
                    break
                if token.tokenType == ",":
                    argumentExpList.append(currentExpList.copy())
                    currentExpList = []
                else:
                    currentExpList.append(token)
            argumentNameList = []
            for argumentTokenList in argumentExpList:
                tempVar = IR.Variable(expTemp=True)
                #tempVarName = "_#EXP_FUNCTION_ARGUMENT_"+str(expLevel)
                irList.append(IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN",tempVar.name]))                
                exp = Exp()
                exp.ReadIn(argumentTokenList, 0, escChar=None)
                exp.GenExpList(irList=irList)
                irList += exp.ToIasm(tempVar.name)
                argumentNameList.append(tempVar.name)
                expLevel += 1
            #n = "_#EXP_FUNCTION_RETURN_"+str(expLevel)
            tempVar = IR.Variable(expTemp=True)
            irList.append(IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", tempVar.name]))
            expLevel += 1
            argumentNameList.insert(0,functionName); argumentNameList.insert(0,tempVar.name)
            irList.append(IR.Instruction("CALL", argumentNameList))
            replaceToken = Lexer.Token()
            replaceToken.tokenContent = tempVar.name#[1:]
            replaceToken.tokenSubset = tempVar.name#[1:]
            replaceToken.tokenType = "NAME"    
            return replaceToken       
        def ReplaceListWithVaraible(irList, tdx):
            global expLevel
            position = tdx + 1
            insideCounter = 0
            newExpTokenList = []
            listExpList = []
            while True:
                if position >= len(self.expTokens):
                    raise Exception("Unclosed list in expression")
                if self.expTokens[position].tokenType in list("(["):
                    insideCounter += 1
                if self.expTokens[position].tokenType in [",","]"] and insideCounter == 0:
                    exp = Exp()
                    exp.expTokens = newExpTokenList.copy()
                    newExpTokenList = []
                    listExpList.append(exp)
                    #position += 1
                else:
                    newExpTokenList.append(self.expTokens[position])
                if self.expTokens[position].tokenType in list("])"):
                    insideCounter -= 1
                    if insideCounter == -1: 
                        break
                position += 1
            varList = []
            for exp in listExpList:
                var = IR.Variable(True)
                irList.append(IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", var.name]))
                genIr = []
                exp.GenExpList(genIr)
                genIr += exp.ToIasm(var.name, writeToAddr=False)
                irList += genIr
                varList.append(var.name)
            listName = IR.Variable(True)
            irList.append(IR.Instruction("CREATE", ["UNKNOWN", listName.name, len(varList)]))
            irList.append(IR.Instruction("SETLIST", [listName.name]+varList))
            del self.expTokens[tdx:position+1]
            listNameToken = Lexer.Token()
            listNameToken.tokenType = "NAME"
            listNameToken.tokenSubset = listName.name
            listNameToken.tokenContent = listName.name
            self.expTokens.insert(tdx,listNameToken)
            tdx += 1
            return tdx
        def ReplaceSingleAritySubtractOperator():
            tdx = 0
            while tdx < len(self.expTokens):
                currentToken = self.expTokens[tdx]
                if type(currentToken) == Lexer.Token:
                    if currentToken.tokenType == "OPERATOR" and currentToken.tokenSubset == "-":
                        if tdx == 0:
                            self.expTokens.insert(0, Lexer.Token("0","CONST"))
                            tdx += 1
                        else:
                            self.expTokens.insert(tdx, Lexer.Token("0","CONST"))
                            self.expTokens.insert(tdx, Lexer.Token("+","OPERATOR"))
                            tdx += 2
                tdx += 1
        #
        ReplaceSingleAritySubtractOperator()
        while tdx < len(self.expTokens):
            if type(self.expTokens[tdx]) == Lexer.Token:
                if self.expTokens[tdx].tokenType == "NAME":
                    if tdx < len(self.expTokens)-1:
                        if self.expTokens[tdx+1].tokenType == "(":
                           self.expTokens.insert(tdx,ReplaceFunctionWithTempVar(irList))
                           tdx -= 1
                           continue
                        if self.expTokens[tdx+1].tokenType == "[":
                            ReplaceListIndexWithTempVar(irList)
                            tdx -= 1
                            continue
                if self.expTokens[tdx].tokenType == "(":
                    e = Exp()
                    newIdx = e.ReadIn(self.expTokens, tdx+1, escChar=")", oppEscChar="(")
                    e.GenExpList(irList)
                    del self.expTokens[tdx:newIdx+1]
                    self.expTokens.insert(tdx, e)   
                    tdx = 0            
                    continue
                #Handle - as a single arity operator

                '''
                if self.expTokens[tdx].tokenType == "OPERATOR":
                    if len(self.expTokens) > tdx+2:
                        if type(self.expTokens[tdx+1]) == Lexer.Token:
                            if self.expTokens[tdx+1].tokenSubset == "-":
                                e = Exp()
                                e.expTokens = self.expTokens[tdx+1:tdx+3].copy()
                                self.expTokens[tdx+1] = e
                                self.expTokens.pop(tdx+2)
                '''
                if self.expTokens[tdx].tokenType == "[":
                    tdx = ReplaceListWithVaraible(irList, tdx)
            tdx += 1        
        self.ApplyBidmas(irList)
    def ErrorChecking(self):
        pass#TODO
    def ApplyBidmas(self, irList):
        while len(self.expTokens) > 3:
            op = None
            opIdx = None
            for idx,i in enumerate(self.expTokens):
                if type(i) == Lexer.Token:
                    if i.tokenType == "OPERATOR":
                        opTest = Operators.IndexOperatorByName(i.tokenSubset)
                        if op == None:
                            op = opTest
                            opIdx = idx
                        elif opTest.bidmasLevel > op.bidmasLevel:
                            op = opTest
                            opIdx = idx
            exp = Exp()            
            if op.argCount == 1:
                tokenForOperator = 2
                deletePosition = opIdx
            else:
                exp.expTokens = self.expTokens[opIdx-1:opIdx+2]
                deletePosition = opIdx -1
                tokenForOperator = 3
            exp.GenExpList(irList)
            for i in range(tokenForOperator):
                del self.expTokens[deletePosition]
            self.expTokens.insert(deletePosition, exp)
    def ExpValToIasmArg(self, value):
        if type(value) == Exp:
            return value.resultVar.name
        if type(value) == Lexer.Token:
            return value.tokenContent
        raise Exception("Invalude value type")    
    def GenInstArgumentList(self, writeInto, operatorArgLength):
        if operatorArgLength == 1:
            return [writeInto, self.ExpValToIasmArg(self.expTokens[0])]
        if operatorArgLength == 2:
            return [writeInto, self.ExpValToIasmArg(self.expTokens[1])]
        if operatorArgLength == 3:
            return [writeInto,self.ExpValToIasmArg(self.expTokens[0]),
                        self.ExpValToIasmArg(self.expTokens[2])]
    def ToIasm(self, writeInto, writeToAddr=False):
        if len(self.expTokens) < 1 or len(self.expTokens) > 3:
            raise Exception("Expression not properly generated")
        instList = []
        expResultList = []
        for i in self.expTokens:
            if type(i) == Exp:
                expResultList.append(IR.Variable(expTemp=True))
                i.resultVar = expResultList[-1]
                instList.append(IR.Instruction("CREATE_TEMP_VAR", [Types.unknownType.name, expResultList[-1].name]))
                instList += i.ToIasm(expResultList[-1].name)
        if writeInto != None:
            if len(self.expTokens) == 1:
                instName = "MOV" if writeToAddr == False else "WRITE_ADDR"
                instList.append(IR.Instruction(instName, [writeInto, self.ExpValToIasmArg(self.expTokens[0])]))
            if len(self.expTokens) == 2:
                instName = self.expTokens[0].tokenSubset
                instList.append(IR.Instruction(instName, [writeInto, self.ExpValToIasmArg(self.expTokens[1])]))
            if len(self.expTokens) == 3:
                instName = self.expTokens[1].tokenSubset
                instList.append(IR.Instruction(instName, [writeInto,
                                                        self.ExpValToIasmArg(self.expTokens[0]),
                                                            self.ExpValToIasmArg(self.expTokens[2])]))
        return instList
    def Print(self, ret=False):
        out = ""
        for t in self.expTokens:
            if type(t) == Exp:
                out += "["+t.Print(ret=True)+"]"
            else:
                out += t.Print(ret=True, nl=False)
                out += ", "
        if ret:
            return out
        print(out)
def ExpToIasm(tokenList, idx, writeInto, escChar=";", oppEscChar=None, writeToAddr=False):#, indexedAt=None
    exp = Exp()
    newIdx = exp.ReadIn(tokenList, idx, escChar, oppEscChar=oppEscChar)
    irList = []
    exp.GenExpList(irList=irList)
    #exp.Print()
    
    irList += exp.ToIasm(writeInto, writeToAddr=writeToAddr)#indexedAt=indexedAt
    return irList, newIdx