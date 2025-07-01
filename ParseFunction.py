from Util import *
import ParseExpression
import IR
import Function
import Struct
import Lexer

tempVarNameNumber = 0
def CreateNewTempVar(instList):
    global tempVarNameNumber
    name = "EXP_TEMP_VAR_" + str(tempVarNameNumber)
    instList.append(IR.Instruction("CREATE_TEMP_VAR",[
        "UNKNOWN",
        name
    ]))
    tempVarNameNumber += 1
    return name
def EvalSquareBrackets(tokenList, idx):
    instList = []
    expName = CreateNewTempVar(instList)
    newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, idx, expName, escChar="]", oppEscChar="[")
    instList += newIrList
    return instList, newIdx, expName

#!!!!!!!!!!!!!!!!!!!!!!!!!
def IsEqu(idx, instList, tokenList):

    #Is EQU if has = and no other keywords
    isEqu = tokenList[idx].tokenType != "TYPE"
    existsEquals = False
    i = idx
    while True:
        if tokenList[i].tokenType == "=":
            existsEquals = True
        if tokenList[i].tokenType in [j.upper() for j in Lexer.keyWordList]:
            isEqu = False
            break
        if tokenList[i].tokenType == ";":
            break
        i += 1
    isEqu = isEqu and existsEquals

    if isEqu:
        #Parse left hand side
        leftEvalTempVar = CreateNewTempVar(instList)
        leftEvalMemAddrTempVar = CreateNewTempVar(instList)
        newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, idx, leftEvalTempVar, escChar="=")
        instList += newIrList
        instList.append(IR.Instruction("&", [leftEvalMemAddrTempVar, leftEvalTempVar]))
        #Parse right hand side
        newIdx += 1#jump over = sign
        rightEvalTempVar = CreateNewTempVar(instList)
        newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, newIdx, rightEvalTempVar, escChar=";")
        instList += newIrList
        instList.append(IR.Instruction("DREF_MOV", [leftEvalMemAddrTempVar, rightEvalTempVar]))
        newIdx += 1#jump over ;
        return True, newIdx
    else:
        return False, 0 

    '''
    errMsg = "Failed to read in Equ"
    nameToken = il(tokenList,idx,errMsg)
    ptr = False
    if nameToken.tokenType == "OPERATOR" and nameToken.tokenSubset == "$":
        idx += 1
        nameToken = il(tokenList,idx,errMsg)
        ptr = True
    if nameToken.tokenType == "NAME":
        expName = None
        equPos = idx + 1
        if il(tokenList,idx+1,errMsg).tokenType == "[":
            newInstructions, newIdx, _ = EvalSquareBrackets(tokenList, idx + 2)
            equPos = newIdx + 1
            instList += newInstructions
        if il(tokenList,idx+1,errMsg).tokenType == ".":
            pass
            #What about a pass before with replaces all . and -> with ptr notation
        if il(tokenList,equPos,errMsg).tokenType == "=":
            expName2 = CreateNewTempVar(instList)
            newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, equPos + 1, expName2)#, indexedAt=expName
            instList += newIrList
            argList = [
                nameToken.tokenSubset,
                expName2
            ]
            if expName != None:
                argList.append(expName)
            instName = "WRITE_ADDR" if ptr else "MOV"
            instList.append(IR.Instruction(instName,argList))
            return True, newIdx + 1
    return False, 0
    '''
def IsTypeDef(idx, instList, tokenList):
    errMsg = "Failed to read in type because end of token list"
    tt = il(tokenList,idx,errMsg).tokenType 
    if tt == "TYPE" or tt == "NAME":
        namePos = idx + 1
        isList = False
        isPtr = False
        if il(tokenList, idx+1, errMsg).tokenType == "[":
            #size = int(tokenList[idx + 2].tokenSubset)
            #namePos = idx + 1+1+1+1
            isList = True
            newInstructions, newIdx, sizeVarName = EvalSquareBrackets(tokenList, idx + 2)
            namePos = newIdx + 1
            instList += newInstructions
        if il(tokenList, idx+1, errMsg).tokenSubset == "$":
            isPtr = True
            namePos += 1
        if il(tokenList,namePos,errMsg).tokenType == "NAME":
            if isList:
                instList.append(IR.Instruction("CREATELIST",[
                    tokenList[idx].tokenSubset + "$" * isPtr,
                    tokenList[namePos].tokenSubset,
                    sizeVarName
                ]))
            else:
                instList.append(IR.Instruction("CREATE",[
                    tokenList[idx].tokenSubset + "$" * isPtr,
                    tokenList[namePos].tokenSubset,
                ]))
            hap,newIdx = IsEqu(namePos, instList, tokenList)
            if hap == False:                    
                if tokenList[namePos+1].tokenType != ";":
                    raise Exception("No semi colon after varaible def")
                return True, namePos + 2
            else:
                return True, newIdx
    return False, 1
def IsRepeat(idx, instList, tokenList):
    global labelCounter
    if il(tokenList, idx, "Faiuled to get token for while stuf").tokenType == "WHILE":
        writeIntoTempVar = IR.Variable(expTemp=True)
        #starting label
        instList.append(IR.Instruction("REPEAT",[   
            "rep_"+str(labelCounter)                 
        ]))    
        labelCounter += 1  
        #evalutate expression
        openScopeAdditionCode.append([])
        openScopeAdditionCode[-1].append(IR.Instruction("CREATE",[
            "UNKNOWN",
            writeIntoTempVar.name            
        ]))
        newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, idx + 1, writeIntoTempVar.name, escChar="{")
        openScopeAdditionCode[-1] += newIrList
        openScopeAdditionCode[-1].append(IR.Instruction("!",[writeIntoTempVar.name, writeIntoTempVar.name]))
        openScopeAdditionCode[-1].append(IR.Instruction("IF",[writeIntoTempVar.name]))
        openScopeAdditionCode[-1].append(IR.Instruction("OPENSCOPE",[]))
        openScopeAdditionCode[-1].append(IR.Instruction("BREAK",["rep_"+str(labelCounter-1)]))
        openScopeAdditionCode[-1].append(IR.Instruction("CLOSESCOPE",[]))
        openScopeAdditionCode[-1].append(IR.Instruction("ENDIF",[]))
        #ending label and jmp
        #closeScopeAdditionCode.append([
        #    IR.Instruction("LABEL",[
        #        "lab_"+str(labelCounter)                     
        #    ])
        #])
        closeScopeAdditionCode.append([
            IR.Instruction("ENDREPEAT",[                   
            ])
        ])
        #labelCounter += 1
        return True, newIdx
    return False, 0
        
def IsIf(idx, instList, tokenList):
    global closeScopeAdditionCode, labelCounter
    errMsg = "Failed to read in if because end of token list"
    if il(tokenList, idx, errMsg).tokenType == "IF":
        writeIntoTempVar = IR.Variable(expTemp=True)
        instList.append(IR.Instruction("CREATE",[
            "UNKNOWN",
            writeIntoTempVar.name            
        ]))
        newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, idx + 1, writeIntoTempVar.name, escChar="{")
        instList += newIrList
        instList.append(IR.Instruction("IF",[
            writeIntoTempVar.name
            #,"lab_"+str(labelCounter),"NO_ELSE"                       
        ]))
        closeScopeAdditionCode.append([
            IR.Instruction("ENDIF",[
                #"lab_"+str(labelCounter)                     
            ])
        ])
        labelCounter += 1
        return True, newIdx
    return False, 0
def IsElse(idx, instList, tokenList):
    global closeScopeAdditionCode, labelCounter
    errMsg = "Failed to read in else because end of token list"
    if il(tokenList, idx, errMsg).tokenType == "ELSE":
        instList.append(IR.Instruction("ELSE",[
            #"lab_"+str(labelCounter)                      
        ]))
        closeScopeAdditionCode.append([
            IR.Instruction("ENDELSE",[
                #"lab_"+str(labelCounter)                     
            ])
        ])
        labelCounter += 1
        return True, idx + 1
    return False, 0

def IsOpenScope(idx, instList, tokenList):
    errMsg = "Failed to read in open scope because end of token list"
    if il(tokenList, idx, errMsg).tokenType == "{":
        instList.append(IR.Instruction("OPENSCOPE",[]))
        if len(openScopeAdditionCode) > 0:
            instList += openScopeAdditionCode[-1]
            openScopeAdditionCode.pop(-1)
        return True, idx + 1
    return False, 0
def IsCloseScope(idx, instList, tokenList):
    errMsg = "Failed to read in close scope because end of token list"
    if il(tokenList, idx, errMsg).tokenType == "}":
        instList.append(IR.Instruction("CLOSESCOPE",[]))
        if len(closeScopeAdditionCode) > 0:
            instList += closeScopeAdditionCode[-1]
            closeScopeAdditionCode.pop(-1)
        return True, idx + 1
    return False, 0
def IsVoidFunctionCall(idx, instList, tokenList):
    errMsg = "Ran out of token to check for function call"
    if il(tokenList,idx,errMsg).tokenType == "NAME":
        if il(tokenList,idx+1,errMsg).tokenType == "(":
            newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, idx, None)
            instList += newIrList
            return True, newIdx + 1
    return False, 0
def IsListAsign(idx, instList, tokenList):
    errMsg = "Ran out of token to check for function call"
    if il(tokenList,idx,errMsg).tokenType == "NAME":
        listName = tokenList[idx].tokenContent
        if il(tokenList,idx+1,errMsg).tokenContent == "-":
            if il(tokenList,idx+2,errMsg).tokenContent == ">":
                if il(tokenList,idx+3,errMsg).tokenType != "[":
                    raise Exception("Expected a square bracket")
                newIdx = idx + 3
                counter = 0
                while 1:
                    if tokenList[newIdx].tokenType == "]": break
                    newIdx += 1
                    if tokenList[newIdx].tokenType == "]": break
                    expName = CreateNewTempVar(instList)
                    newIrList, newIdx = ParseExpression.ExpToIasm(tokenList, newIdx, expName, escChar=",]")              
                    instList += newIrList
                    expName2 = CreateNewTempVar(instList)
                    instList.append(IR.Instruction("*", [expName2, str(counter) , "VAR_TYPE"]))#?listName
                    instList.append(IR.Instruction("MOV", [listName, expName, expName2])) 
                    counter += 1                    
                return True, newIdx + 2
    return False, 0
def IsCreateFunction(idx, instList, tokenList):
    errMsg = "Ran out of tokens to check if it is a new function being created"
    if il(tokenList,idx,errMsg).tokenType == "FN":
        f = Function.Function()
        idx = f.GetFunctionReturnType(tokenList, idx + 1)
        if il(tokenList,idx,errMsg).tokenType != "NAME":
            raise Exception("Expected a name for the function")        
        f.name = tokenList[idx].tokenContent
        idx = f.GetFunctionParameterList(tokenList, idx  + 1) 
        idx = f.ReadInScope(tokenList, idx)
        idx += 1 #step over last }

        f.GenerateIR()
        instList += f.IRList

        return True, idx
    return False, 0

def IsCreateStruct(idx, instList, tokenList):
    errMsg = "Ran out of tokens to check if it is a new function being created"
    if il(tokenList,idx,errMsg).tokenType == "STRUCT":
        newIdx, struct = Struct.CreateStruct(tokenList, idx)

        lst = []
        for i in range(len(struct.varNameList)):
            lst.append(struct.varTypeList[i])
            lst.append(struct.varNameList[i])

        instList.append(IR.Instruction("CREATE_STRUCT", [
            struct.name,
            "~".join(lst)
        ]))

        instList += struct.GetFunctionDefinitionIrCode()

        #idx += 1

        #structName = tokenList[idx]
        #idx += 1
        #structContents, idx = FirstLayerParser.ReadInScope(tokenList, idx)

        #instList.append(IR.Instruction("CREATE_STRUCT", [listName, expName, expName2])) 
        return True, newIdx
    return False, 0

        


labelCounter = 0
closeScopeAdditionCode = []
openScopeAdditionCode = []
functionList = [
    IsCloseScope,
    IsOpenScope,
    IsTypeDef,
    IsEqu,
    IsListAsign,
    IsIf,
    IsElse,
    IsRepeat,
    IsVoidFunctionCall,
    IsCreateFunction,
    IsCreateStruct
]

def GenerateIR(tokenList):
    global closeScopeAdditionCode
    closeScopeAdditionCode = []
    instList = []
    idx = 0
    for t in tokenList:
        foundTokenCombo = False
        for f in functionList:
            #ret[0] = did it happend
            #ret[1] = number of tokens to jump
            ret = f(idx, instList, tokenList)
            if ret[0] == True:
                idx = ret[1]
                if idx >= len(tokenList):
                    return instList
                foundTokenCombo = True
                break
        if foundTokenCombo == False:
            raise Exception("Failed to find token combo idx -> " + str(idx))
    return instList

