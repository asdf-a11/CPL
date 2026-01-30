import IRConversionDataStructures as IRDataStructures
import IRCoversionToDataStructures as IRToDataStructures
import Types
from Util import *
import Struct
import IR
import copy
import Operators
import Function
import Propergation

arithmeticInstructionNameList=[
    "+","-","/","*","%"
]

inbuiltFunctionList = [
    Function.Function("_shalloc", ["ui8$"], ["i32"], ["size"]),
    Function.Function("_graphicsinit", ["i32"], ["i32", "i32"], ["x","y"]),
    Function.Function("_drawpixel", ["i32"], ["i32"]*5, list("xyrgb")),
    Function.Function("_shalloc", ["i32"], ["i32"], ["ticks"]),
    Function.Function("_printn", ["void"], ["i32"], ["number"]),
    Function.Function("_printc", ["void"], ["i32"], ["character"]),
    Function.Function("_printf", ["void"], ["f32"], ["value"]),
    Function.Function("_graphicspump", ["void"], [], []),
    Function.Function("_sin", ["f32"], ["f32"], ["theta"]),
    Function.Function("_cos", ["f32"], ["f32"], ["theta"]),
    Function.Function("_tan", ["f32"], ["f32"], ["theta"]),
    Function.Function("_arctan", ["f32"], ["f32"], ["value"]),
    Function.Function("_sqrt", ["f32"], ["f32"], ["value"]),
]

variableNameCounter = 0
def GetNewTempVarName():
    global variableNameCounter
    out = "IR_OPT_" + str(variableNameCounter)
    variableNameCounter += 1
    return out


class DataType():
    def __init__(self, baseType, typeModifiers):
        self.baseType = baseType
        self.typeModifiers = typeModifiers
    def fromString(self, string):
        pass
    def toString(self):
        return self.baseType.name + "".join(self.typeModifiers)
class Variable():
    def __init__(self, dataType,  name):#, listSize
        self.name = name
        self.dataType = dataType
        #self.listSize = listSize
        self.hardSetType = False if self.dataType.baseType.name == "UNKNOWN" else True
        #If value for Type is known then it is stored here
        self.typeValue = None
        pass
class TempVariable():
    REPLACE_VARAIBLE_STRING = "##"
    def __init__(self, dataType=None, name=None, listSize=None):
        #super().__init__(dataType, name, listSize)
        self.name = name
        self.dataType = dataType
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
    name = ""
    for i in string:
        if i in ["$", "[", "]"]:
            break
        name += i
    dt = Types.GetTypeByName(name)
    r = DataType(dt, [])
    if dt == False:
        r.baseType = Types.Type(
            name=string,
            style="struct",
            sizeInBytes=-1
        )
    i = len(name)
    while i < len(string):
        if string[i] == "$":
            r.typeModifiers.append("$")
        if string[i] == "[":
            i += 1
            s = "["
            while string[i] != "]":
                s += string[i]
                i += 1
            s += "]"
            r.typeModifiers.append(s)
        i += 1
    return r
def LogCreatedVariable(argList, currentScope):
    dataType = GetDataTypeByName(argList[0])
    varName = argList[1]
    #if len(argList) == 3:
    #    dataType.numberOfElements = argList[2]
    currentScope.append(Variable(dataType, varName))
def GetVaraibleFromScopeList(name, scopeList):
    for i in reversed(scopeList):
        for v in i:
            if v.name == name:
                return v
    raise Exception("Failed to find varaible " + str(name))
def IsDataType(argument):
    for i in Types.typeList:
        if i.name == argument:
            return i
    return False
def GetArgumentType(argument, scopeList) -> DataType:
    r = DataType(None, [])
    if IsConstant(argument):
        if "." in argument:
            r.baseType = copy.deepcopy(Types.f32Type)
            return r
        r.baseType = copy.deepcopy(Types.i32Type)    
        return r
    t = IsDataType(argument)
    if t != False:
        r.baseType = copy.deepcopy(t)
        return r
    var = GetVaraibleFromScopeList(argument, scopeList)
    return copy.deepcopy(var.dataType)
def EvaluateDataTypesFromTypeList(typeList:list) -> Types.Type:
    #float allways win
    #ptr win next
    #Then bigger wins
    #signed beet unsigned
    #list beat non list ?
    #return copy.deepcopy(typeList[0])
    floatSizeList = []
    for t in typeList:
        if len(t.typeModifiers) == 0:
            if t.baseType.style == "float":
                floatSizeList.append(t.baseType.sizeInBytes)
                continue
        floatSizeList.append(-1)
    largestFloat = argMax(floatSizeList)
    if max(floatSizeList) == -1:
        return copy.deepcopy(typeList[0])
        #Look for ptr
        for t in typeList:
            if t.isPtr != 0:
                return copy.deepcopy(t)
        #Return biggest data type
        sizeList = []
        for t in typeList:
            sizeList.append(t.sizeInBytes)
        largestDataType = argMax(sizeList)
        return copy.deepcopy(typeList[largestDataType])
    else:
        return copy.deepcopy(typeList[largestFloat])
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
        writeIntoVar.dataType = EvaluateDataTypesFromTypeList([type1, type2]) 
def UpdateVarTypeFromMov(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    typ = GetArgumentType(argList[1], scopeList)
    #If it is allready hardset then it shouldnt change else it needs to be evaluated
    if writeIntoVar.hardSetType == False:
        #Following the rules of update to float, to bigger or if is currently UNKNOWN
        #condition = writeIntoVar.dataType.baseType.name == "UNKNOWN"
        #condition = condition or (writeIntoVar.dataType.baseType.style == "int" and typ.baseType.style == "float")
        #condition = condition or (writeIntoVar.dataType.baseType.style == typ.baseType.style and typ.baseType.sizeInBytes > writeIntoVar.dataType.baseType.sizeInBytes)
        #if condition:
        #    writeIntoVar.dataType = typ
        #    SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)   
        writeIntoVar.dataType = EvaluateDataTypesFromTypeList([typ])
    if writeIntoVar.dataType.baseType.name == Types.typeType.name:
        writeIntoVar.typeValue = copy.deepcopy(typ)
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList) 
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

            instList[idx].argList[0] = var.dataType.baseType.name + "".join(var.dataType.typeModifiers)
            #instList[idx].argList[0] = var.dataType.name + "$" * var.dataType.isPtr
            #if len(instList[idx].argList) == 2:
            #    instList[idx].argList.append(None)
            #instList[idx].argList[-1] = var.dataType.numberOfElements
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
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)  
def UpdateVarTypeFromGetAddress(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        typ = GetArgumentType(argList[1], scopeList)
        writeIntoVar.dataType = copy.deepcopy(typ)
        writeIntoVar.dataType.typeModifiers.append("$")
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)  
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
def UpdateVarTypeFromDref(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        typ = GetArgumentType(argList[1], scopeList)
        writeIntoVar.dataType = copy.deepcopy(typ)
        #writeIntoVar.dataType.isPtr = 0
        if writeIntoVar.dataType.typeModifiers[-1] != "$":
            raise Exception("Dereferencing a non pointer variable")
        writeIntoVar.dataType.typeModifiers.pop(-1)
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)
def UpdateVarTypeFromCall(instRef, scopeList):
    argList = instRef.argList
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        #Get return type of function
        for scope in reversed(scopeList):
            for i in scope:
                if type(i) == Function.Function:
                    if i.name == argList[1]:
                        #TODO handle multiple returns probably by generating a struct
                        #Perhaps do this when creating the function unless struct is allready
                        #created for that combination of data types
                        #TODO need to be able to return list from function
                        writeIntoVar.dataType = GetDataTypeByName(i.returnTypeList[0])
                        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)
                        if writeIntoVar.dataType.baseType.name == "void":
                            instRef.argList[0] = "void"
                        return
        #else assume it is a int
        writeIntoVar.dataType.baseType = copy.deepcopy(Types.i32Type)
        writeIntoVar.dataType.typeModifiers = []
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)
def LogCreatedFunction(argList, scopeList):
    scopeList[-1].append(
        Function.Function(
            name=argList[0],
            returnTypeList=argList[1].split("~"),
            perameterTypeList=argList[2].split("~")[0::2],
            perameterNameList=argList[2].split("~")[1::2]
        )
    )
def EvaluateCompileTimeFunction(inst, scopeList):
    hasMadeChanges = False
    newInst = None
    if inst.name == "CALL":
        match inst.argList[1]:
            case "_declindtype":
                if len(inst.argList) != 3:
                    raise Exception("Invalid number of arguments for _declindtype")
                #Get type of variable
                var = GetVaraibleFromScopeList(inst.argList[2], scopeList)
                newInst = copy.deepcopy(inst)
                newInst.name = "MOV_TYPE"
                newInst.argList = [inst.argList[0], var.dataType.toString()]
                hasMadeChanges = True
    return hasMadeChanges, newInst
def ReplaceVarWithKnownType(inst, scopeList):
    newInst = copy.deepcopy(inst)
    for idx, arg in enumerate(inst.argList):
        f = False
        for scope in reversed(scopeList):
            for i in scope:
                if type(i) == Variable:
                    if i.name == arg:
                        if i.typeValue != None:
                            newInst.argList[idx] = i.typeValue.name
                            f = True
                            break
            if f: break
    return newInst
def UpdateVarTypeFromListIndex(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        listVar = GetVaraibleFromScopeList(argList[1], scopeList)
        writeIntoVar.dataType = copy.deepcopy(listVar.dataType)
        if "[" not in writeIntoVar.dataType.typeModifiers[-1]:
            raise Exception("Cannot index non list varaible")
        writeIntoVar.dataType.typeModifiers.pop()
        #SetVariable(writeIntoVar.name, writeIntoVar.dataType, scopeList)
def UpdateVarTypeFromSetList(argList, scopeList):
    writeIntoVar = GetVaraibleFromScopeList(argList[0], scopeList)
    if writeIntoVar.hardSetType == False:
        #Just assumes that types are consistant
        listVar = GetVaraibleFromScopeList(argList[1], scopeList)
        writeIntoVar.dataType = copy.deepcopy(listVar.dataType)
        writeIntoVar.dataType.typeModifiers.append(f"[{len(argList)-1}]")
def EvaluateDataTypes(instList): 
    def RemoveVar_Type(inst, scopeList):
        if len(inst.argList) == 0: return
        if inst.name not in Operators.operatorNameList: return

        for adx in range(1, len(inst.argList)):
            if "VAR_TYPE" in inst.argList[adx]:
                l = inst.argList[adx].split("~")
                if len(l) != 2:
                    raise Exception("you plonker")
                vt = GetArgumentType(l[1], scopeList)
                inst.argList[adx] = vt.name

        #vt = GetArgumentType(inst.argList[1], scopeList)
        #for adx in range(1,len(inst.argList)):
        #    inst.argList[adx] = inst.argList[adx].replace("VAR_TYPE",vt.name) 
          
    scopeList = []
    openScopePositionList = []
    firstOpenScope = True
    for idx,inst in enumerate(instList):   
        #RemoveVar_Type(inst, scopeList)   
        
        hap, newInstruction = EvaluateCompileTimeFunction(inst, scopeList)
        if hap:
            instList[idx] = newInstruction
            inst = newInstruction
        
        newInstruction = ReplaceVarWithKnownType(inst, scopeList)
        instList[idx] = newInstruction
        inst = newInstruction

        if inst.name == "OPENSCOPE":
            scopeList.append([])
            openScopePositionList.append(idx+1)
            if firstOpenScope:
                scopeList[-1] += inbuiltFunctionList
            firstOpenScope = False
        elif inst.name == "CLOSESCOPE":
            BackTrackAndSetTypes(openScopePositionList[-1], instList, scopeList)
            openScopePositionList.pop(-1)
            scopeList.pop(-1)
        elif inst.name == "CREATE" or inst.name == "CREATE_ARGUMENT" or inst.name == "CREATE_TEMP_VAR":
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "CREATE_FUNCTION" and firstOpenScope == False:
            LogCreatedFunction(inst.argList, scopeList)
        elif inst.name == "CREATE_STRUCT":
            LogStructure(inst.argList, scopeList)
        elif inst.name in arithmeticInstructionNameList:
            UpdateVarTypeFromArithmetic(inst.argList, scopeList)
        elif inst.name == ".":
            UpdateVarTypeFromDot(inst.argList, scopeList)
        elif inst.name == "&":
            UpdateVarTypeFromGetAddress(inst.argList, scopeList)
        elif inst.name == "[]":
            UpdateVarTypeFromListIndex(inst.argList, scopeList)
        elif inst.name == "$":
            UpdateVarTypeFromDref(inst.argList, scopeList)
        elif inst.name == "CALL":
            UpdateVarTypeFromCall(inst, scopeList)
        elif inst.name == "SETLIST":
            UpdateVarTypeFromSetList(inst.argList, scopeList)
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
                #Means instruction is first instruction in addrInstList
                continue
        #Store memory address instructions
        else:
            writeIntoVar = GetTempVar(scopeList, inst.argList[0])
            if writeIntoVar != None:
                RVS = TempVariable.REPLACE_VARAIBLE_STRING
                if inst.name == "$":
                    writeIntoVar.addressInstList.append(
                        IR.Instruction("MOV", [RVS, inst.argList[1]])
                    )
                elif inst.name == ".":
                    tempVar = GetNewTempVarName()
                    typeOfStruct = GetNewTempVarName()
                    writeIntoVar.addressInstList += [
                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", tempVar]),
                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", typeOfStruct]),
                        IR.Instruction("&", [tempVar, inst.argList[1]]),
                        IR.Instruction("CALL", [typeOfStruct, "_decltype", inst.argList[1]]),
                        IR.Instruction("+", [RVS, tempVar, f"{typeOfStruct}::{inst.argList[2]}"])
                    ]
                elif inst.name == "MOV":
                    writeIntoVar.addressInstList += [
                        IR.Instruction("&", [RVS, inst.argList[1]]),
                    ]
                elif inst.name == "[]":
                    offsetTempVar = GetNewTempVarName()
                    tempVar2 = GetNewTempVarName()
                    sizeOfTempVar = GetNewTempVarName()
                    typeTempVar = GetNewTempVarName()
                    writeIntoVar.addressInstList += [
                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", offsetTempVar]),
                        IR.Instruction("CREATE_TEMP_VAR", ["type", typeTempVar]),
                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", sizeOfTempVar]), 

                        IR.Instruction("CALL", [typeTempVar, "_declindtype", inst.argList[1]]),
                        IR.Instruction("CALL", [sizeOfTempVar, "_sizeof", typeTempVar]),
                        IR.Instruction("*", [offsetTempVar, inst.argList[2], sizeOfTempVar]),

                        IR.Instruction("CREATE_TEMP_VAR", ["UNKNOWN", tempVar2]),
                        IR.Instruction("&", [tempVar2, inst.argList[1]]),
                        IR.Instruction("+", [RVS, offsetTempVar, tempVar2])
                    ]
        instructionIndex += 1

def ConstPropergation(instList):
    instCounter = 0
    scopeList = []
    while instCounter < len(instList):
        inst = instList[instCounter]
        if inst.name == "OPENSCOPE":
            scopeList.append([])
            if firstOpenScope:
                scopeList[-1] += inbuiltFunctionList
            firstOpenScope = False
        elif inst.name == "CLOSESCOPE":
            scopeList.pop(-1)
        elif inst.name == "CREATE" or inst.name == "CREATE_ARGUMENT" or inst.name == "CREATE_TEMP_VAR":
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "CREATE_FUNCTION" and firstOpenScope == False:
            LogCreatedFunction(inst.argList, scopeList)
        elif inst.name == "CREATE_STRUCT":
            LogStructure(inst.argList, scopeList)
        
        elif inst.name == "MOV":
            writeIntoVar = GetVaraibleFromScopeList(inst.argList[0], scopeList)

        instCounter += 1
def PerformOperations(program):
    instList = IRToDataStructures.ToInstructionList(program)    
    BreakDownStructs(instList)
    EvaluateMemoryAddressOfTempVars(instList)
    #RemoveListSetting(instList)
    #RemoveVar_Type(instList)
    #RemoveUnknownVarType(instList)
    #EvaluateDataTypes(instList)
    #ConstPropergation(instList)
    Propergation.PropergateValues(instList)
    return InstListToProgram(instList)   
    



