from Util import *
from Function import *


def GetFunctionReturnType(tokenList, idx):
    #fn i32, i8, i8 functionName(i32 a, b){}
    errMsg = "Failed to find close of function when finding types"
    returnTypeList = []
    while 1:
        if il(tokenList, idx, errMsg).tokenType not in ["NAME", "TYPE"]:
            raise Exception("Expected a name or type in function retur type list")
        nextToken = il(tokenList, idx, errMsg)
        returnTypeList.append(nextToken.tokenSubset)
        if il(tokenList, idx + 1, errMsg).tokenSubset != ",":
            break
        idx += 1
    if len(returnTypeList) == 0:
        raise Exception("Function must have a return type")
    return returnTypeList, idx + 1
def GetFunctionParameterList(tokenList, idx):
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
    return typeList, nameList, idx+1
def ReadInScope(tokenList, idx):
    if tokenList[idx].tokenType != "{":
        raise Exception("Expected a {")
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
    return out, idx
def FirstLayerParse(tokenList):
    functionList = []
    idx = 0    
    while idx < len(tokenList):
        match tokenList[idx].tokenType:
            case "FN":
                f = Function()
                f.returnTypeList, nameIdx = GetFunctionReturnType(tokenList, idx + 1)
                #nameIdx = idx + 1 + len(f.returnTypeList)
                if tokenList[nameIdx].tokenType != "NAME":
                    raise Exception("Expected function name")
                f.name = tokenList[nameIdx].tokenSubset
                typeList, nameList, scopeIdx = GetFunctionParameterList(tokenList, nameIdx + 1)
                f.perameterNameList = nameList
                f.perameterTypeList = typeList
                f.tokenList, idx = ReadInScope(tokenList, scopeIdx)
                idx += 1
                functionList.append(f)
            case _:
                raise Exception("Expected Function")
    return functionList
    
        