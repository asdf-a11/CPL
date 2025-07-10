import IRConversionDataStructures as IRDataStructures
import IRCoversionToDataStructures as IRToDataStructures
import Types
from Util import *
import Struct
import IR
import copy
import Operators
import Function


class InvalidNameError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

arithmeticInstructionNameList=[
    "+","-","/","*","%", "<", ">", "==", "!", "or", "and"
]

#Needs to know the return type of inbuilt functions for type evaluation
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
    def GetNumberOfElements(self):
        if len(self.typeModifiers) == 0:
            return 1
        l = self.typeModifiers[-1]
        if l == "$":
            return 1
        if l[0] != "[":
            return 1
        return l[1:-1]
    def GetSize(self):
        numberOfElements = self.GetNumberOfElements()
        baseTypeSize = self.baseType.sizeInBytes
        return numberOfElements * baseTypeSize
    def fromString(self, string):
        pass
    def AsString(self):
        s = self.baseType.name
        s += "".join(self.typeModifiers)
        return s
class Variable():
    def __init__(self, dataType,  name):#, listSize
        self.name = name
        self.dataType = dataType
        #self.listSize = listSize
        self.hardSetType = False if self.dataType.baseType.name == "UNKNOWN" else True
        #If value for Type is known then it is stored here
        #self.typeValue = None
        self.knownValue = None
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

class ControllFlowNode():
    def __init__(self, instList):
        self.functionName = None
        self.instList = instList
        #self.SetFunctionName()
    #def SetFunctionName(self):
    #    if self.instList[0].name == "CREATE_FUNCTION":
    #        self.functionName = self.instList[0].argList[0]
    def AsString(self,cfgList, tabs=""):
        tabs = ""
        s = "" if self.functionName == None else f"funcName: {self.functionName}\n"
        for i in self.instList:
            s += tabs + i.Print(ret=True) + "\n"
            if i.name == "CFG_BLOCK" and False:
                s += tabs + "{\n"
                s += cfgList[i.argList[0]].AsString(cfgList, tabs=tabs+"\t")
                s += tabs + "}\n"            
        return s
        



def GenerateControllFlowGraph(instList):
    cfgList = []
    lst = []
    controllFlowInstructions = [
        "IF", "CREATE_FUNCTION", "RETURN", "BREAK", "ELSE", "ENDIF", "REPEAT",
        "END_REPEAT"
    ]
    nextFunctionName = None
    for inst in instList:
        lst.append(inst)
        if inst.name in controllFlowInstructions:
            lst.append(IR.Instruction("CFG_BLOCK", [len(cfgList)+1]))
            cfn = ControllFlowNode(lst.copy())
            cfn.functionName = nextFunctionName
            cfgList.append(cfn)
            lst = []
            if inst.name == "CREATE_FUNCTION":
                nextFunctionName = inst.argList[0]
            else:
                nextFunctionName = None
    if len(lst) != 0:
        cfn = ControllFlowNode(lst.copy())
        cfgList.append(cfn)
    return cfgList

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
def GetBaseTypeFromString(string):
    name = ""
    for i in string:
        if i in ["$", "[", "]"]:
            break
        name += i
    return name
def GetDataTypeByName(string):
    name = GetBaseTypeFromString(string)
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
    raise InvalidNameError("Failed to find varaible")
def IsDataType(argument, scopeList) -> bool:
    baseType = GetBaseTypeFromString(argument)
    validNames = [i.name for i in Types.typeList]
    validNames += [v.name for s in reversed(scopeList) for v in s if type(v) == Struct.Struct]
    return baseType in validNames    
def GetArgumentType(argument, scopeList) -> DataType:
    r = DataType(None, [])
    if IsConstant(argument):
        if "." in argument:
            r.baseType = copy.deepcopy(Types.f32Type)
            return r
        r.baseType = copy.deepcopy(Types.i32Type)    
        return r
    if IsDataType(argument, scopeList):
        r = GetDataTypeByName(argument)
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
        lst = [type1]
        if type2 != None: 
            lst.append(type2)
        writeIntoVar.dataType = EvaluateDataTypesFromTypeList(lst) 
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
    if argList[0] == "void":
        return
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
    newInst = None
    if inst.name == "CALL":
        match inst.argList[1]:
            case "_declindtype":
                if len(inst.argList) != 3:
                    raise Exception("Invalid number of arguments for _declindtype")
                #Get type of variable
                var = copy.deepcopy(GetVaraibleFromScopeList(inst.argList[2], scopeList))
                #if var.dataType.isPtr == 0:
                #    raise Exception("Cannot get index type of non pointer variable")
                #inst.argList[0] = f"{var.dataType.name}*"
                #inst.argList[1] = "i32"
                #TODO check if it is a list otherwise throw error
                var.dataType.typeModifiers.pop()
                newInst = copy.deepcopy(inst)
                newInst.name = "MOV"
                newInst.argList = [inst.argList[0],  var.dataType.AsString()]
            case "_sizeof":
                if len(inst.argList) != 3:
                    raise Exception("Invalid number of arguments for _sizeof")
                if IsDataType(inst.argList[2],scopeList):
                    t = GetDataTypeByName(inst.argList[2])
                    newInst = copy.deepcopy(inst)
                    newInst.name = "MOV"
                    sizeString = str(t.GetSize())
                    newInst.argList = [inst.argList[0],  sizeString]
    return newInst
#Runs per line and is varaible types are updated per line
def ReplaceVarWithKnownType(inst, scopeList):
    newInst = None
    for idx, arg in enumerate(inst.argList):
        f = False
        for scope in reversed(scopeList):
            for i in scope:
                if type(i) == Variable:
                    if i.name == arg:
                        if i.typeValue != None:
                            newInst = copy.deepcopy(inst)
                            newInst.argList[idx] = i.typeValue.AsString()
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
        
        newInst = EvaluateCompileTimeFunction(inst, scopeList)
        if newInst != None:
            instList.insert(idx, IR.Instruction(";", [instList[idx].name,
                *instList[idx].argList]))
            instList[idx+1] = newInst
            
        #if hap:
        #    instList[idx] = newInstruction
        #    inst = newInstruction
        
        #newInst = ReplaceVarWithKnownType(inst, scopeList)
        #if newInst != None:
        #    instList[idx] = newInst
        #instList[idx] = newInstruction
        #inst = newInstruction

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
    return False  

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
    scopeList = []
    idx = 0
    hap = False
    while idx < len(instList):
        inst = instList[idx]
        if inst.name == "OPENSCOPE":
            scopeList.append([])
        elif inst.name == "CLOSESCOPE":
            scopeList.pop()
        elif inst.name in ["CREATE", "CREATE_ARGUMENT", "CREATE_TEMP_VAR"]:
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "MOV":
            writeInto = GetVaraibleFromScopeList(inst.argList[0],scopeList)
            
            
            writeIntoNumElements = writeInto.dataType.GetNumberOfElements()
            if writeIntoNumElements != 1:
                fromVar = GetVaraibleFromScopeList(inst.argList[1],scopeList)
                #TODO error checking for mismatch in sized lists
                #instList.pop(idx)
                instList[idx].argList.append(instList[idx].name)
                instList[idx].name = ";"
                idx += 1

                counter = GetNewTempVarName()
                ifEvalVar = GetNewTempVarName()
                repeatName = GetNewTempVarName()
                valueOfListIndex = GetNewTempVarName()
                memAddressOfListIndex = GetNewTempVarName()
                tempValueOfFromVar = GetNewTempVarName()
                #writeIntoVarSize = Types.GetTypeByName(writeInto.dataType).sizeInBytes
                #writeIntoListSize = writeInto.listSize * writeIntoVarSize
                lst = [
                    IRDataStructures.Instruction("CREATE",["i32", counter]),
                        IRDataStructures.Instruction("OPENSCOPE"),
                        IRDataStructures.Instruction("MOV",[counter, "0"]),
                        IRDataStructures.Instruction("REPEAT",[repeatName]),
                            IRDataStructures.Instruction("OPENSCOPE"),
                            IRDataStructures.Instruction("CREATE",["UNKNOWN", ifEvalVar]),
                            IRDataStructures.Instruction("==",[ifEvalVar, counter, str(writeIntoNumElements)]),
                            IRDataStructures.Instruction("IF",[ifEvalVar]),
                                IRDataStructures.Instruction("OPENSCOPE"),
                                IRDataStructures.Instruction("BREAK", [repeatName]),
                                IRDataStructures.Instruction("CLOSESCOPE"),
                            IRDataStructures.Instruction("ENDIF"),
                            IRDataStructures.Instruction("CREATE_TEMP_VAR",["UNKNOWN", valueOfListIndex]),                            
                            IRDataStructures.Instruction("[]",[valueOfListIndex, writeInto.name, counter]),
                            IRDataStructures.Instruction("CREATE_TEMP_VAR",["UNKNOWN", memAddressOfListIndex]),
                            IRDataStructures.Instruction("&",[memAddressOfListIndex, valueOfListIndex]),

                            #TODO assumes from var is another list of equal size
                            #could be just single value like 0
                            IRDataStructures.Instruction("CREATE_TEMP_VAR",["UNKNOWN", tempValueOfFromVar]),
                            IRDataStructures.Instruction("[]",[tempValueOfFromVar, fromVar.name, counter]),
                            IRDataStructures.Instruction("DREF_MOV",[memAddressOfListIndex, tempValueOfFromVar]),


                            IRDataStructures.Instruction("+",[counter, counter, "1"]),
                            IRDataStructures.Instruction("CLOSESCOPE"),
                    IRDataStructures.Instruction("ENDREPEAT"),
                    IRDataStructures.Instruction("CLOSESCOPE")
                ]
                for i in reversed(lst):
                    instList.insert(idx, i)
                hap = True
                #Allows for recursive expansion
                continue
        idx += 1
    return hap
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
        for i in reversed(scopeList):
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
                #instList.pop(instructionIndex)
                instList[instructionIndex].argList.append(instList[instructionIndex].name)
                instList[instructionIndex].name = ";"    
                instructionIndex += 1            
                addrInstList = tempVar.GetAddressInstructionList(writeIntoName=inst.argList[0])
                for i in reversed(addrInstList):
                    instList.insert(instructionIndex, i)
                #Means instruction is first instruction in addrInstList
                continue
        #Store memory address instructions
        elif len(inst.argList) > 0:
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
    return False
def ConstPropergation(instList):
    instCounter = 0
    scopeList = []
    firstOpenScope = True
    hap = False
    while instCounter < len(instList):
        inst = instList[instCounter]
        if inst.name == "OPENSCOPE":
            scopeList.append([])
            if firstOpenScope:
                scopeList[-1] += inbuiltFunctionList
            firstOpenScope = False
        elif inst.name == "CLOSESCOPE":
            scopeList.pop(-1)
        elif inst.name in ["CREATE", "CREATE_TEMP_VAR", "CREATE_ARGUMENT"]:
            LogCreatedVariable(inst.argList, scopeList[-1])
        elif inst.name == "CREATE_FUNCTION" and firstOpenScope == False:
            LogCreatedFunction(inst.argList, scopeList)
        elif inst.name == "CREATE_STRUCT":
            LogStructure(inst.argList, scopeList)        
        elif inst.name == "MOV":
            writeIntoVar = GetVaraibleFromScopeList(inst.argList[0], scopeList)
            if IsConstant(inst.argList[1]):
                writeIntoVar.knownValue = inst.argList[1]
            elif IsDataType(inst.argList[1],scopeList):
                writeIntoVar.knownValue = inst.argList[1]
            else:
                writeIntoVar.knownValue = None
        else:
            for adx in range(len(inst.argList)):
                if adx == 0: continue
                try:
                    v = GetVaraibleFromScopeList(inst.argList[adx], scopeList)
                    if type(v) == Variable and v.knownValue != None:
                        inst.argList[adx] = v.knownValue
                        hap = True
                except InvalidNameError:
                    pass
        instCounter += 1
    return hap
def RemoveUnusedVariable(instList):
    def BackTrack(instList, idx, readList, scopeList):
        #flatternedReadList = [i.name for i in readList[-1]]#[j.name for i in readList for j in i]
        notReadNameList = [v.name for v in scopeList[-1] if v not in readList[-1]]
        idx -= 1#Jump over close scope that called backtrack
        scopeCounter = 0
        hap = False
        while 1:
            inst = instList[idx]
            if inst.name == "CLOSESCOPE":
                scopeCounter += 1
            elif inst.name == "OPENSCOPE":
                if scopeCounter == 0:
                    break
                scopeCounter -= 1
            elif inst.name != ";":#inst.name in arithmeticInstructionNameList + ["MOV"]:
                for a in range(len(inst.argList)):
                    if inst.argList[a] in notReadNameList:
                        inst.argList.append(inst.name)
                        inst.name = ";"
                        hap = True
            idx -= 1
        return hap
    instCounter = 0
    scopeList = []
    readList = []
    readFromFirstArgumentList = [
        "DREF_MOV", "IF"
    ]
    hap = False
    while instCounter < len(instList):
        inst = instList[instCounter]
        if inst.name == "OPENSCOPE":
            scopeList.append([])
            readList.append(set())
        elif inst.name == "CLOSESCOPE":
            #Back track deleting
            if len(scopeList) == 1:
                pass
            hap = hap or BackTrack(instList, instCounter, readList, scopeList)
            scopeList.pop(-1)
            readList.pop(-1)
        elif inst.name in ["CREATE", "CREATE_TEMP_VAR"]:#, "CREATE_ARGUMENT"
            LogCreatedVariable(inst.argList, scopeList[-1])      
        elif inst.name != ";":
            startPoint = 0 if inst.name in readFromFirstArgumentList else 1
            for argCounter in range(startPoint,len(inst.argList)):
                try:
                    var = GetVaraibleFromScopeList(inst.argList[argCounter], scopeList)
                    #Variable read in all scopes up to scope it is created in 
                    #stops varaibles that are used but in lower scopes from getting deleted
                    for counter in range(1,len(readList)+10):
                        readList[-counter].add(var)
                        if var in scopeList[-counter]:
                            break

                except InvalidNameError:
                    pass
        instCounter += 1
    return hap
newLabelCounter = 0
def GetNewLabel():
    global newLabelCounter
    newLabelCounter += 1
    return f"cf_{newLabelCounter}"
def HighLevelControllFlowToGoto(instList) -> list:
    class FailedToFindInstruction(Exception):
        def __init__(self, msg):
            super().__init__(msg)
            self.msg = msg
    def ReplaceInstruction(replaceName, replaceInstLst, startIndex, terminateInstName=None):
        for index in range(startIndex, len(instList)):
            if instList[index].name == replaceName:
                #instList[index] = replaceInstruction
                instList.pop(index)
                for i in reversed(replaceInstLst):
                    instList.insert(index, i)
                return
            if instList[index].name == terminateInstName:
                break
        raise FailedToFindInstruction("Failed to find instruction to replace")
    instCounter = 0
    while instCounter < len(instList):
        if instList[instCounter].name == "IF":
            instList[instCounter].name = "CONDITIONAL_GOTO"            
            ifThenLabel = GetNewLabel()
            ifEndLabel = GetNewLabel()
            instList[instCounter].argList.append(ifThenLabel)
            instList.insert(instCounter+1, IR.Instruction("LABEL", [ifThenLabel]))
            labelAfterIf = ifEndLabel
            try:
                ifElseLabel = GetNewLabel()
                ReplaceInstruction("ELSE", [IR.Instruction("LABEL",[ifElseLabel])], instCounter, terminateInstName="ENDIF")
                labelAfterIf = ifElseLabel
            except FailedToFindInstruction:
                pass
            instList.insert(instCounter+1, IR.Instruction("GOTO", [labelAfterIf]))
            ReplaceInstruction("ENDIF", [IR.Instruction("LABEL",[ifEndLabel])], instCounter)
        instCounter += 1
    return instList
def PerformOperations(program):
    instList = IRToDataStructures.ToInstructionList(program)    
    BreakDownStructs(instList)
    instList = HighLevelControllFlowToGoto(instList)
    print(InstListToProgram(instList))
    cfgList = GenerateControllFlowGraph(instList)
    print(cfgList[1].AsString(cfgList).replace("\t"," "))
    hap = True
    while hap:
        hap = True
        while hap:
            hap = False
            hap = hap or EvaluateMemoryAddressOfTempVars(instList)
            #RemoveVar_Type(instList)
            #RemoveUnknownVarType(instList)
            hap = hap or EvaluateDataTypes(instList)
            hap = hap or ConstPropergation(instList)
            hap = hap or RemoveUnusedVariable(instList)
        hap = hap or RemoveListSetting(instList)
    return InstListToProgram(instList)   
    



