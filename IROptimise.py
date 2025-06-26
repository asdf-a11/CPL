import IRConversionDataStructures as IRDataStructures
import IRCoversionToDataStructures as IRToDataStructures
import Types
from Util import *
import Struct
import IR
import copy
import Operators

arithmeticInstructionNameList=[
    "+","-","/","*","%"
]


variableNameCounter = 0
def GetNewTempVarName():
    global variableNameCounter
    out = "IR_OPT_" + str(variableNameCounter)
    variableNameCounter += 1
    return out

class TempVariable():
    REPLACE_VARAIBLE_STRING = "##"
    def __init__(self, dataType=None, name=None, listSize=None):
        self.name = name
        self.addressInstList = []
    def GetAddressInstructionList(self, writeIntoName):
        if len(self.addressInstList) == None:
            raise Exception("Address inst list is empty")
        ret = []
        for i in self.addressInstList:
            inst = copy.deepcopy(i)
            for a in range(len(inst.argList)):
                if inst.argList[a] == self.REPLACE_VARAIBLE_STRING:
                    inst.argList[a] = writeIntoName
            ret.append(inst)
        return ret
class Variable():
    def __init__(self, dataType,  name, listSize):
        self.name = name
        self.dataType = dataType
        self.listSize = listSize
        self.hardSetType = False if self.dataType.name == "UNKNOWN" else True
        pass
class Scope():
    def __init__(self):
        self.varList = []
    def AddVariable(self, dataType, varName, listSize):
        self.varList.append(Variable(dataType, varName, listSize))
def SetVariable(varName, dataType, scopeList):
    for s in reversed(scopeList):
        for i in s:
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
def GetDataTypeByName(string):
    dt = Types.GetTypeByName(string)
    if dt == False:
        return Types.Type(
            name=string,
            style="struct",
            sizeInBytes=-1
        )
    return dt
def LogCreatedVariable(argList, currentScope):
    dataType = GetDataTypeByName(argList[0])
    varName = argList[1]
    if len(argList) == 2:
        listSize = 1
    else:
        listSize = int(argList[2])    
    #currentScope.AddVariable(dataType, varName, listSize)
    currentScope.append(Variable(dataType, varName, listSize))
def GetVaraibleFromScopeList(name, scopeList):
    for i in reversed(scopeList):
        for v in i:
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
    if len(argList) >= 3:
        if argList[2] == "VAR_TYPE":
            type2 = type1
        else:
            type2 = GetArgumentType(argList[2], scopeList)
    else:
        type2 = None
    if writeIntoVar.hardSetType == False:
        isStyleFloat = writeIntoVar.dataType.style == "float"
        isStyleFloat = isStyleFloat or type1.style == "float"
        if type2 != None:
            isStyleFloat = isStyleFloat or type2.style == "float"

        isUnsigned = writeIntoVar.dataType.style == "unsigned"
        isUnsigned = isUnsigned and type1.style == "unsigned"
        if type2 != None:
            isUnsigned = isUnsigned and type2.style == "unsigned"

        isPtr = type1.isPtr
        if type2 != None:
            isPtr = isPtr or type2.isPtr

        if isStyleFloat: style = "float"
        else:
            if isUnsigned: style = "unsigned"
            else: style = "int"

        writeIntoVatSize = 0 if writeIntoVar.dataType.sizeInBytes == None else writeIntoVar.dataType.sizeInBytes

        if type2 != None:
            maxSize = max(type1.sizeInBytes, type2.sizeInBytes)
        else:
            maxSize = type1.sizeInBytes
        maxSize = max(maxSize, writeIntoVatSize)

        writeIntoVar.dataType = Types.GetTypeByStyleAndSize(style, maxSize)
        writeIntoVar.dataType.isPtr = isPtr

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
        c = instList[idx].name == "CREATE" or instList[idx].name == "CREATE_ARGUMENT"
        c = c or instList[idx].name == "CREATE_TEMP_VAR"
        if c:
            var = GetVaraibleFromScopeList(instList[idx].argList[1], scopeList)
            instList[idx].argList[0] = var.dataType.name + ("$" if var.dataType.isPtr else "")
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
def UpdateVarTypeFromDot(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        structVar = GetVaraibleFromScopeList(argList[1], scopeList)
        typ = GetVarTypeFromStruct(structName=structVar.dataType.name, attribName=argList[2], scopeList=scopeList)
        writeIntoVar.dataType = copy.deepcopy(typ)
        SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)  
def UpdateVarTypeFromGetAddress(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        typ = GetArgumentType(argList[1], scopeList)
        writeIntoVar.dataType = copy.deepcopy(typ)
        writeIntoVar.dataType.isPtr = True
        SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)  
def GetVarTypeFromStruct(structName, attribName, scopeList):
    struct = None
    for scope in reversed(scopeList):
        for item in scope:
            if type(item) == Struct.Struct and item.name == structName:
                struct = item
                break
        if struct != None:
            break
    for idx, i in enumerate(struct.varNameList):
        if i == attribName:
            return GetDataTypeByName(struct.varTypeList[idx])
    raise Exception("You suck")
def LogStructure(argList, scopeList):
    struct = Struct.Struct()
    struct.name = argList[0]
    struct.varTypeList = argList[1].split("~")[0::2]
    struct.varNameList = argList[1].split("~")[1::2]
    scopeList[-1].append(struct)
def EvaluateDataTypes(instList): 
    def RemoveVar_Type(inst, scopeList):
        if len(inst.argList) == 0: return
        if inst.name not in Operators.operatorNameList: return
        vt = GetArgumentType(inst.argList[1], scopeList)
        for adx in range(1,len(inst.argList)):
            inst.argList[adx] = inst.argList[adx].replace("VAR_TYPE",vt.name)   
    scopeList = []
    openScopePositionList = []
    for idx,inst in enumerate(instList):   
        RemoveVar_Type(inst, scopeList)     
        if inst.name == "OPENSCOPE":
            scopeList.append([])
            openScopePositionList.append(idx+1)
        elif inst.name == "CLOSESCOPE":
            BackTrackAndSetTypes(openScopePositionList[-1], instList, scopeList)
            openScopePositionList.pop(-1)
            scopeList.pop(-1)
        elif inst.name == "CREATE" or inst.name == "CREATE_ARGUMENT" or inst.name == "CREATE_TEMP_VAR":
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "CREATE_STRUCT":
            LogStructure(inst.argList, scopeList)
        elif inst.name in arithmeticInstructionNameList:
            UpdateVarTypeFromArithmetic(inst.argList, scopeList)
        elif inst.name == ".":
            UpdateVarTypeFromDot(inst.argList, scopeList)
        elif inst.name == "&":
            UpdateVarTypeFromGetAddress(inst.argList, scopeList)
        elif inst.name == "MOV":
            UpdateVarTypeFromMov(inst.argList, scopeList)
        

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
#Vector operations like + - mov on lists need to be broken down
#individual elements
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
                pointer = GetNewTempVarName()
                ifEvalVar = GetNewTempVarName()
                repeatName = GetNewTempVarName()
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

def BreakDownStructs(instList):
    structList = []
    for idx,inst in enumerate(instList):
        if inst.name == "OPENSCOPE":
            structList.append([])
        if inst.name == "CLOSESCOPE":
            structList.pop(-1)
        if inst.name == "CREATE_STRUCT":
            struct = Struct.Struct()
            struct.name = inst.argList[0]
            struct.varNameList = inst.argList[1].split("~")[1::2]
            struct.varTypeList = inst.argList[1].split("~")[0::2]
            #add offset values
            lst = []
            for name in struct.varNameList:
                lst.append(IR.Instruction("CREATE", ["i32", f"{struct.name}::{name}"]))
            for i in reversed(lst):
                instList.insert(idx+1,i)
        if inst.name == "CREATE_FUNCTION":
            if "::" in inst.argList[0] and len(structList) > 0:
                for idx,struct in enumerate(structList[-1]):
                    if struct.name + "::" in inst.argList[0]:
                        structList[idx].functionList.append()
                        break


def EvaluateMemoryAddressOfTempVars(instList):
    def GetTempVar(scopeList, varName):
        for i in scopeList:
            for j in i:
                if j.name == varName:
                    return j
        return None
    #Loop through instruction list
    scopeList = [[]]
    instructionIndex = 0
    while instructionIndex < len(instList):
        inst = instList[instructionIndex]
        #Handle scoping
        if inst.name == "OPENSCOPE":
            scopeList.append([])
        elif inst.name == "CLOSESCOPE":
            scopeList.pop(-1)
        #Track list of instructions to compute memory address of temp var
        elif inst.name == "CREATE_TEMP_VAR":
            scopeList[-1].append(
                TempVariable(name=inst.argList[1])
            )        
        #Replace instances of & for temp var with instruction list
        elif inst.name == "&":
            #Makes sure getting address of a temp var and not actual var
            tempVar = GetTempVar(scopeList, inst.argList[1])
            if tempVar != None:
                instList.pop(instructionIndex)
                addrInstList = tempVar.GetAddressInstructionList(writeIntoName=inst.argList[0])
                for i in reversed(addrInstList):
                    instList.insert(instructionIndex, i)
        #Store memory address instructions
        else:
            writeIntoVar = GetTempVar(scopeList, inst.argList[0])
            if writeIntoVar != None:
                RVS = TempVariable.REPLACE_VARAIBLE_STRING
                if inst.name == "$":
                    writeIntoVar.addressInstList.append(
                        IR.Instruction("MOV", [RVS, inst.argList[0]])
                    )
                elif inst.name == ".":
                    tempVar = GetNewTempVarName()
                    writeIntoVar.addressInstList += [
                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", tempVar]),
                        IR.Instruction("&", [tempVar, inst.argList[1]]),
                        IR.Instruction("+", [RVS, tempVar, f"VAR_TYPE::{inst.argList[2]}"])
                    ]
                elif inst.name == "MOV":
                    writeIntoVar.addressInstList += [
                        IR.Instruction("&", [RVS, inst.argList[1]]),
                    ]
        instructionIndex += 1

def PerformOperations(program):
    instList = IRToDataStructures.ToInstructionList(program)    
    BreakDownStructs(instList)
    EvaluateMemoryAddressOfTempVars(instList)
    #RemoveListSetting(instList)
    #RemoveVar_Type(instList)
    #RemoveUnknownVarType(instList)
    EvaluateDataTypes(instList)
    return InstListToProgram(instList)   
    



