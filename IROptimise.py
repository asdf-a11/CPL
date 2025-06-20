import IRConversionDataStructures as IRDataStructures
import IRCoversionToDataStructures as IRToDataStructures
import Types
from Util import *

arithmeticInstructionNameList=[
    "+","-","/","*","%"
]

variableNameCounter = 0
def CreateNewTempVar():
    global variableNameCounter
    out = "IR_OPT_" + str(variableNameCounter)
    variableNameCounter += 1
    return out

class Variable():
    def __init__(self, dataType,  name, listSize):
        self.name = name
        self.dataType = dataType
        self.listSize = listSize
        self.hardSetType = False if self.dataType.name == "UNKNOWN" else True
class Scope():
    def __init__(self):
        self.varList = []
    def AddVariable(self, dataType, varName, listSize):
        self.varList.append(Variable(dataType, varName, listSize))
def SetVariable(varName, dataType, scopeList):
    for s in reversed(scopeList):
        for i in s.varList:
            if i.name == varName:
                i.dataType = dataType
                return
    raise Exception("Failed to set varaible as it cannot be found name ->"+varName)
def GenerateScopes(instList):
    scopeList = [Scope()]
    scopeLevel = 0
    currentScopeList = []
    for i in instList:
        if i.name == "OPENSCOPE":
            if scopeLevel == 1:
                scopeList.append(currentScopeList)
                scopeLevel = 0
            currentScopeList.append(Scope())
            scopeLevel += 1            
        if i.name == "CLOSESCOPE":
            if scopeLevel == 0:
                currentScopeList = scopeList[-1]
            scopeLevel -= 1
        if i.name == "CREATE":
            pass
def LogCreatedVariable(argList, currentScope):
    dataType = Types.GetTypeByName(argList[0])
    varName = argList[1]
    if len(argList) == 2:
        listSize = 1
    else:
        listSize = int(argList[2])    
    currentScope.AddVariable(dataType, varName, listSize)
def GetVaraibleFromScopeList(name, scopeList):
    for i in reversed(scopeList):
        for v in i.varList:
            if v.name == name:
                return v
    raise Exception("Failed to find varaible")
def GetArgumentType(argument, scopeList):
    if IsConstant(argument):
        if "." in argument:
            return Types.f32Type
        return Types.i32Type
    var = GetVaraibleFromScopeList(argument, scopeList)
    return var.dataType
def UpdateVarTypeFromArithmetic(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    type1 = GetArgumentType(argList[1], scopeList)
    if argList[2] == "VAR_TYPE":
        type2 = type1
    else:
        type2 = GetArgumentType(argList[2], scopeList)
    if writeIntoVar.hardSetType == False:
        isStyleFloat = writeIntoVar.dataType.style == "float"
        isStyleFloat = isStyleFloat or type1.style == "float"
        isStyleFloat = isStyleFloat or type2.style == "float"

        isUnsigned = writeIntoVar.dataType.style == "unsigned"
        isUnsigned = isUnsigned and type1.style == "unsigned"
        isUnsigned = isUnsigned and type2.style == "unsigned"

        if isStyleFloat: style = "float"
        else:
            if isUnsigned: style = "unsigned"
            else: style = "int"

        writeIntoVatSize = 0 if writeIntoVar.dataType.sizeInBytes == None else writeIntoVar.dataType.sizeInBytes

        maxSize = max(type1.sizeInBytes, type2.sizeInBytes)
        maxSize = max(maxSize, writeIntoVatSize)

        writeIntoVar.dataType = Types.GetTypeByStyleAndSize(style, maxSize)

        SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)   
def UpdateVarTypeFromMov(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    typ = GetArgumentType(argList[1], scopeList)
    #If it is allready hardset then it shouldnt change else it needs to be evaluated
    if writeIntoVar.hardSetType == False:
        #Following the rules of update to float, to bigger or if is currently UNKNOWN
        condition = writeIntoVar.dataType.name == "UNKNOWN"
        condition = condition or (writeIntoVar.dataType.style == "int" and typ.style == "float")
        condition = condition or (writeIntoVar.dataType.style == typ.style and typ.sizeInBytes > writeIntoVar.dataType.sizeInBytes)
        if condition:
            writeIntoVar.dataType = typ
            SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)   
def BackTrackAndSetTypes(idx, instList, scopeList):
    openScopeCounter = 0
    while 1:
        if instList[idx].name == "OPENSCOPE":
            openScopeCounter += 1
        if openScopeCounter > 0:
            if instList[idx].name == "CLOSESCOPE":
                openScopeCounter -= 1
            idx += 1
            continue
        if instList[idx].name == "CLOSESCOPE":
            break
        if instList[idx].name == "CREATE":
            var = GetVaraibleFromScopeList(instList[idx].argList[1], scopeList)
            instList[idx].argList[0] = var.dataType
        idx += 1
def InstListToProgram(instList):
    out = ""
    tabs = ""
    for i in instList:
        if i.name == "OPENSCOPE":
            tabs += "\t"
        out += tabs + i.name + " "
        for a in i.argList:
            out += str(a) + ", "
        if len(i.argList) != 0:
            out = out[:-2]
        out += "\n"
        if i.name == "CLOSESCOPE":
            tabs = tabs[:-1]
    return out
def RemoveUnknownVarType(instList):    
    scopeList = [Scope()]
    openScopePositionList = []
    for idx,inst in enumerate(instList):
        if inst.name == "OPENSCOPE":
            scopeList.append(Scope())
            openScopePositionList.append(idx+1)
        elif inst.name == "CLOSESCOPE":
            BackTrackAndSetTypes(openScopePositionList[-1], instList, scopeList)
            openScopePositionList.pop(-1)
            scopeList.pop(-1)
        elif inst.name == "CREATE" or inst.name == "CREATE_ARGUMENT":
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name in arithmeticInstructionNameList:
            UpdateVarTypeFromArithmetic(inst.argList, scopeList)
        elif inst.name == "MOV":
            UpdateVarTypeFromMov(inst.argList, scopeList)
def RemoveVarType(instList):
    for idx,inst in enumerate(instList):
        for adx,a in enumerate(inst.argList):
            if a == "VAR_TYPE":
                name = instList[idx].argList[adx-1]
                instList[idx].argList[adx] = str(4)
'''
OPENSCOPE
    CREATE I32 TEMP1
    MOV TEMP1, 0
    REPEAT new_rep_0
        OPENSCOPE
        CREATE UNKNOWN, TEMP2
        mov temp2, temp1
        == temp2, temp2, LIST_SIZE * VAR_TYPE
        IF temp2
            OPENSCOPE
            BREAK new_rep_0
            CLOSESCOPE
        ENDIF
        MOV write_into, arg2, temp1
        add temp1, temp1 , VAR_SIZE
        CLOSESCOPE
    ENDREPEAT new_rep_0
CLOSESCOPE
'''    
def RemoveListSetting(instList):
    scopeList = [Scope()]
    idx = 0
    while idx < len(instList):
        inst = instList[idx]
        if inst.name == "OPENSCOPE":
            scopeList.append(Scope())
        elif inst.name == "CLOSESCOPE":
            scopeList.pop(-1)
        elif inst.name == "CREATE" or inst.name == "CREATE_ARGUMENT":
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "MOV":
            writeInto = GetVaraibleFromScopeList(inst.argList[0],scopeList)
            if writeInto.listSize > 1 and len(inst.argList) == 2:
                instList.pop(idx)
                pointer = CreateNewTempVar()
                ifEvalVar = CreateNewTempVar()
                repeatName = CreateNewTempVar()
                writeIntoVarSize = Types.GetTypeByName(writeInto.dataType).sizeInBytes
                writeIntoListSize = writeInto.listSize * writeIntoVarSize
                instList.insert(idx, IRDataStructures.Instruction("OPENSCOPE")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("CREATE",["i32", pointer])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("MOV",[pointer, "0"])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("REPEAT",[repeatName])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("OPENSCOPE")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("CREATE",["UNKNOWN", ifEvalVar])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("MOV",[ifEvalVar, pointer])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("==",[ifEvalVar, ifEvalVar, str(writeIntoListSize)])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("IF",[ifEvalVar])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("OPENSCOPE")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("BREAK", [repeatName])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("CLOSESCOPE")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("ENDIF")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("MOV",[inst.argList[0], inst.argList[1], pointer])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("+",[pointer, pointer, str(writeIntoVarSize)])); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("CLOSESCOPE")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("ENDREPEAT")); idx += 1
                instList.insert(idx, IRDataStructures.Instruction("CLOSESCOPE"))
        idx += 1
def PerformOperations(program):
    instList = IRToDataStructures.ToInstructionList(program)    
    RemoveListSetting(instList)
    RemoveUnknownVarType(instList)
    RemoveVarType(instList)
    return InstListToProgram(instList)   
    



