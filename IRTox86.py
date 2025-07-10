import copy
import Util
import Types

MaxBits = -1
platform = None
stackPointerName = "esp"
stackBasePointerName = "ebp"
builtInFunctionPath = "InBuiltFunctions_COS/"
asmType = "nasm"

class BuiltInFunction():
    def __init__(self, name, includeName, returnTypeList, parameterList):
        self.name = name
        self.includeName = includeName
        self.returnTypeList = returnTypeList
        self.parameterList = parameterList
        self.includedAllready = False
builtInFunctionList = [
    BuiltInFunction("_printc", "printc.asm", [], ["i32"]),
    BuiltInFunction("_setCursor", "setCursor.asm", [], ["i32","i32"])
    #BuiltInFunction("_printb", "printb.asm", [], ["i32"]),
    #BuiltInFunction("_printf", "printf.asm", [], ["f32"])
]

def UpdateSettings(settings):
    global MaxBits,stackBasePointerName,stackPointerName, platform, asmType
    settings = settings.replace(" ", "")
    settingsList = settings.split("-")
    for s in settingsList:
        if s == "m86":
            MaxBits = 32
        elif s == "m64":
            MaxBits = 64
            stackBasePointerName = "rbp"
            stackPointerName = "rsp"
        elif s == "windows":
            platform = "windows"
        elif s == "COS":
            platform = "COS"
        elif s == "masm":
            asmType = "masm"
    #if platform == None:
    #    raise Exception("Please specify target platform")
class DataType():
    def __init__(self, baseType, typeModList):
        self.baseType = baseType
        self.typeModifiers = typeModList
        self.isDynamicList = self.IsDynamicList()
    def IsDynamicList(self):
        for i in reversed(self.typeModifiers):
            if i[0] == "[":
                if Util.IsConstant(i[1:-1]) == False:
                    return True
        return False
    def GetSize(self):
        numberOfElements = 1
        isPtr = False
        for i in reversed(self.typeModifiers):
            if i[0] == "[":
                if Util.IsConstant(i[1:-1]):
                    numberOfElements *= int(i[1:-1])
                else:
                    raise Exception("Cant get size of dynamic array")
            elif i == "$":
                isPtr = True
                break
        baseSize = 4 if isPtr else self.baseType.sizeInBytes
        return baseSize * numberOfElements
    def AsSizeString(self, sizeOverride=None):
        size = self.GetSize()
        if sizeOverride != None:
            size = sizeOverride
        if size == 4:
            return "dword"
        if size == 2:
            return "word"
        if size == 1:
            return "byte"
        raise Exception("Invalid size")
def GetRegisterFromSize(size, regChar="a"):
    match(size):
        case 1:
            return f"{regChar}l"
        case 2:
            return f"{regChar}x"
        case 4:
            return f"e{regChar}x"
        case _:
            raise Exception("Invalid size")
def GetDataTypeFromString(dataTypeName):
    baseTypeString = ""
    for i in dataTypeName:
        if i in ["$", "["]:
            break
        baseTypeString += i
    baseTypeRef = None
    for i in Types.typeList:
        if i.name == baseTypeString:
            baseTypeRef = i
            break
    if baseTypeRef == None:
        raise Exception("Could not find base type -> " + baseTypeString)
    typeModifiers = []
    restOfString = dataTypeName[len(baseTypeString):]
    i = 0
    while i < len(restOfString):
        if restOfString[i] == "$":
            typeModifiers.append("$")
        if restOfString[i] == "[":
            typeModifiers.append("[")
            while 1:
                typeModifiers[-1] += restOfString[i]
                if restOfString[i] == "]":
                    break
                i += 1
        i += 1
    return DataType(copy.deepcopy(baseTypeRef), typeModifiers)


class Register():
    def __init__(self, name, size, childList):
        self.name = name
        self.size = size
        self.childList = childList
        self.inUse = False
class Variable():
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType
        #self.listSize = listSize
        #self.listSizeBytes = listSize * dataType.size
        self.storedIn = "stack"
        self.scopeTag = None
        #self.ptrString = ptrString
    def GetPositionInCurrentScope(self,scopeList):
        #counts from ebp
        scopePosition = 0        
        for sdx,s in enumerate(reversed(scopeList)):
            inScopePosition = 0
            searchList = s.variableList
            #Because looking from the opposite direction aka (looking up the stack not down)
            #When looking at all prevoise stack frames therefore must be reversed
            if sdx != 0:
                searchList = reversed(searchList)
            for v in searchList:
                if sdx != 0:
                    inScopePosition += v.dataType.GetSize()
                if v == self:
                    if sdx == 0:
                        inScopePosition -= 4
                    return scopePosition + inScopePosition 
                if sdx == 0:
                    inScopePosition -= v.dataType.GetSize()
            if sdx != 0:#for the first scope leaving ebp does not include stack frame            
                scopePosition += 4 if MaxBits == 32 else 8
        raise Exception("Can find self in scope List")
    def GetMemoryAddressFromBasePtr(self, scopeList):
        relPos = self.GetPositionInCurrentScope(scopeList)
        return str(relPos)
    def GetMemoryAddress(self, scopeList):
        relPos = self.GetPositionInCurrentScope(scopeList)
        return stackBasePointerName + " + " + str(relPos)
    def AsString(self, scopeList, clipVarSize=None):
        currentScope = scopeList[self.scopeTag]
        code = ""
        if self.storedIn == "stack":
            relPos = self.GetPositionInCurrentScope(scopeList)
            masmString = " ptr " if asmType == "masm" else ""
            code += self.dataType.AsSizeString(sizeOverride=clipVarSize) + masmString + "[" + stackBasePointerName + " + " + str(relPos) + "]"
        return code
class ControllFlow():
    def __init__(self, is_if = False, is_repeat = False, has_else = False):
        self.is_if = is_if
        self.is_repeat = is_repeat
        #is if
        self.has_else = has_else
class Scope():
    def __init__(self, tag):
        self.variableList = []
        self.tag = tag
    def GetSize(self):
        total = 0
        for v in self.variableList:
            if v.dataType.isDynamicList:
                total += 4
            else:
                total += v.dataType.GetSize()
        return total
class Function():
    def __init__(self, name , returnList, paramTypeList, paramNameList):
        self.name = name
        self.paramTypeList = paramTypeList
        self.paramNameList = paramNameList
        self.returnList = returnList
    def GetParamStackPosition(self, varName):
        reversedNameList = self.paramNameList[::-1]
        idx = reversedNameList.index(varName)
        out = 6
        reversedTypeList = self.paramTypeList[::-1]
        for i in range(idx):
            dataType = GetDataTypeFromName(reversedTypeList[i])
            out += dataType.size
        return out
dataBlockCounter = 0
class DataBlock():
    def __init__(self, kind, size, dataList):
        global dataBlockCounter
        self.kind = kind
        self.size = size
        self.dataList = dataList
        self.name = "DataBlock_" + str(dataBlockCounter)
        dataBlockCounter += 1
    def GetAllocationString(self):
        kindSize = Types.GetTypeByName(self.kind).sizeInBytes
        if kindSize == 1: return "db"
        if kindSize == 2: return "dw"
        if kindSize == 4: return "dd"
        if kindSize == 8: return "dq"
        raise Exception("Failed")
    def AsString(self):
        out = self.name + ":\n"
        allocationString = self.GetAllocationString()
        for i in range(self.size):
            out += "\t" + allocationString + " " + self.dataList[i]
        return out

class Converter():
    def __init__(self):
        self.scopeList = None
        self.tabs = None
        self.labelCounter = 0
        self.registerList = [
            Register("al", 1, []),
            Register("ah", 1, []),    
            Register("ax", 2, ["al", "ah"]),
            Register("eax", 4, ["ax"])
        ]
        self.controllFlowList = []
        self.functionList = []
        self.repeatLabelList = []
        self.ifLabelList = []
        self.ifLabelCounter = 0
        self.repeatLabelCounter = 0
        self.commentIR = True
        self.includeCode = ""
        self.dataBlockList = []

        if asmType == "nasm":
            pass
        else:
            pass
    def AllocStackBytes(self, sizeBytes):
        code = self.tabs
        code += "sub " + stackPointerName + ", "
        code += str(sizeBytes) + "\n"
        return code    
    def GetVariableByName(self, name) -> Variable:
        for scope in reversed(self.scopeList):
            for v in scope.variableList:
                if v.name == name:
                    return v
        raise Exception("Failed to find varaible -> " + name)
    def IsConstant(self, string):
        return Util.IsConstant(string)      
    def IsFloat(self, string):
        if self.IsVariable(string):
            var = self.GetVariableByName(string)
            return var.dataType.style == "float"
        return "." in string
    def IsVariable(self, string):
        if self.IsConstant(string) == False:
            return True
        return False
    def GetVariableMemoryAddressFromBasePtr(self, string):
        var = self.GetVariableByName(string)
        return var.GetMemoryAddressFromBasePtr(self.scopeList)
    def GetOperandAsString(self, string, clipVarSize=None):
        #if string.replace(".","").isdigit():
        #    return string
        if Util.IsConstant(string):
            if "." in string:
                return "0b"+Util.FloatToIEEE754(float(string))
            else:
                return string
        return self.GetVariableByName(string).AsString(self.scopeList, clipVarSize=clipVarSize)
    def GetFreeRegister(self, sizeReq):
        for r in self.registerList:
            if r.size == sizeReq:
                if not r.inUse:
                    return r
        raise Exception("No free register")
    def CmpArguments(self, arg1, arg2):
        code = ""
        arg1_asmString = self.GetOperandAsString(arg1)
        if self.IsConstant(arg1):
            if self.IsConstant(arg2) == False:
                temp = copy.deepcopy(arg2)
                arg2 = copy.deepcopy(arg1)
                arg1 = temp
            else:
                #TODO assumed constant allways of size 4
                freeRegister = self.GetFreeRegister(4)  
                code += self.tabs + "mov " + freeRegister.name + ", " + self.GetOperandAsString(arg1) + "\n"
                arg1_asmString = freeRegister.name
        arg2_asmString = self.GetOperandAsString(arg2)
        if self.IsConstant(arg1) == False and  self.IsConstant(arg2) == False:   
            arg2Size = self.GetVariableByName(arg2).dataType.size 
            freeRegister = self.GetFreeRegister(arg2Size)                    
            code += self.tabs + "mov " + freeRegister.name + ", " + arg2_asmString + "\n"
            arg2_asmString = freeRegister.name
        code += self.tabs + "cmp " + arg1_asmString + ", " + arg2_asmString + "\n"
        return code
    def MoveUpScopes(self, scopeLevel):
        i = len(self.scopeList) - 1
        totalScopeSize = 0
        while i != scopeLevel:
            totalScopeSize += self.scopeList[i].GetSize()
            totalScopeSize += 4 if MaxBits == 32 else 8
            i -= 1
        code = ""
        code += self.tabs + "add esp, " + str(totalScopeSize) + "\n"
        return code
    def CheckAndIncludeBuiltInFunction(self, functionName):
        for f in builtInFunctionList:
            if f.name == functionName:
                if f.includedAllready == False:
                    f.includedAllready = True
                    return "%include \""+builtInFunctionPath+f.includeName+"\"\n"
                else:
                    return ""
        return ""
    #############
    #convertion functions
    ##############
    def Repeat(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "repeat_" + str(self.repeatLabelCounter) + ":\n"
        #self.endRepeatScopeLevelList.append(len(self.scopeList)-1)
        self.repeatLabelList.append(self.repeatLabelCounter)
        self.repeatLabelCounter += 1
        return code
    def EndRepeat(self, instList, instIdx, argList):
        code = ""       
        code += self.tabs + "jmp repeat_" + str(self.repeatLabelList[-1]) + "\n"  
        code += self.tabs + "endRepeat_" + str(self.repeatLabelList[-1]) + ":\n"         
        self.repeatLabelList.pop(-1)       
        return code
    def Mov(self, instList, instIdx, argList):
        code = ""

        writeIntoVar = self.GetVariableByName(argList[0])        
        reg = "eax"
        if self.IsVariable(argList[1]):      
            var = self.GetVariableByName(argList[1])   
            argSize = var.dataType.GetSize()  
            reg = GetRegisterFromSize(argSize)      
            code += self.tabs + f"mov {reg}, {var.AsString(self.scopeList)}\n"
        else:
            code += self.tabs + f"mov {reg}, {argList[1]}\n"
        code += self.tabs
        code += f"mov {writeIntoVar.AsString(self.scopeList)}, {reg}\n"
        return code
    def Create(self, instList, instIdx, argList):
        currentInst = instList[instIdx]
        dataType = GetDataTypeFromString(currentInst.argList[0])
        variable = Variable(currentInst.argList[1], dataType)
        variable.scopeTag = self.scopeList[-1].tag
        self.scopeList[-1].variableList.append(variable)
        bytesToAlloc = 4 if variable.dataType.isDynamicList else variable.dataType.GetSize()
        #code =  f"{self.tabs};{variable.name} ptrString = {ptrString}\n"
        code = self.AllocStackBytes(bytesToAlloc)
        return code
    def CreateArgument(self, instList, instIdx, argList):
        currentInst = instList[instIdx]
        dataType = GetDataTypeFromName(currentInst.argList[0])        
        variable = Variable(currentInst.argList[1], dataType)
        variable.scopeTag = self.scopeList[-1].tag
        self.scopeList[-1].variableList.append(variable)
        code = ""
        code += self.AllocStackBytes(dataType.size)
        currentFunction = self.functionList[-1]
        stackPos = currentFunction.GetParamStackPosition(variable.name)
        code += self.tabs + "mov eax, dword[ebp+" + str(stackPos)+"]\n"
        code += self.tabs + "mov " + self.GetOperandAsString(variable.name) + ", eax\n"
        return code
    def OpenScope(self,instList, instIdx, argList):
        self.scopeList.append(Scope(len(self.scopeList)))
        self.tabs += "\t"
        code = ""
        code += self.tabs + "push " + stackBasePointerName + "\n"
        code += self.tabs + "mov " + stackBasePointerName + ", " + stackPointerName + "\n"
        return code
    def CloseScope(self,instList, instIdx, argList):
        self.scopeList.pop(-1)        
        code = ""
        code += self.tabs + "mov " + stackPointerName + ", " + stackBasePointerName + "\n"
        code += self.tabs + "pop " + stackBasePointerName + "\n"  
        self.tabs = self.tabs[1:]      
        return code
    def LessThan(self,instList, instIdx, argList):
        code = ""
        code += self.CmpArguments(argList[1], argList[2])
        code += self.tabs + "setl " + self.GetOperandAsString(argList[0], clipVarSize=1) + "\n"
        return code
    def GreaterThan(self,instList, instIdx, argList):
        code = ""
        code += self.CmpArguments(argList[1], argList[2])
        code += self.tabs + "setg " + self.GetOperandAsString(argList[0], clipVarSize=1) + "\n"
        return code
    def Equals(self,instList, instIdx, argList):
        code = ""
        code += self.CmpArguments(argList[1], argList[2])
        code += self.tabs + "sete " + self.GetOperandAsString(argList[0], clipVarSize=1) + "\n"
        return code
    def NotEquals(self,instList, instIdx, argList):
        code = ""
        code += self.CmpArguments(argList[1], argList[2])
        code += self.tabs + "setne " + self.GetOperandAsString(argList[0], clipVarSize=1) + "\n"
        return code
    def Add(self, instList, instIdx, argList):
        code = ""
        isFloatList = [self.IsFloat(i) for i in argList]
        if True in isFloatList:
            movInstNameList = ["fld " if i else "fild " for i in isFloatList]
            for i in range(1,3):
                v = self.GetOperandAsString(argList[i])
                if Util.IsConstant(argList[i]):
                    db = DataBlock("f32" if isFloatList[i] else "i32", 1, [argList[i]])
                    self.dataBlockList.append(db)
                    v = "dword["+db.name+"]"
                code += self.tabs + movInstNameList[1] + v + "\n"#st0
            code += self.tabs + "faddp st1, st0\n"#result in st0
            code += self.tabs + "fstp " + self.GetOperandAsString(argList[0]) + "\n"#pops st0
        else:
            code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
            code += self.tabs + "add eax, " + self.GetOperandAsString(argList[2]) + "\n"
            code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def Sub(self,instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "sub eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def If(self, instList, instIdx, argList):        
        code = ""
        self.controllFlowList.append(ControllFlow(
            is_if=True
        ))
        code += self.CmpArguments(argList[0], "0")
        code += self.tabs + "je endif_"+str(self.ifLabelCounter) + "\n"
        self.ifLabelList.append(self.ifLabelCounter)
        self.ifLabelCounter += 1        
        return code
    def Else(self, instList, instIdx, argList): 
        #else must come after an endif
        if instList[instIdx-1].name != "ENDIF":
            raise Exception("ELSE should only come after ENDIF")  
        code = ""
        self.controllFlowList[-1].has_else = True
        code += self.tabs + "jmp endElse_" + str(self.ifLabelList[-1]) + "\n"
        code += self.tabs + "endif_"+str(self.ifLabelList[-1]) + ":\n" 
        return code
    def EndIf(self, instList, instIdx, argList):     
        if instIdx + 1 < len(instList):
            if instList[instIdx+1].name == "ELSE":
                return ""
        code = ""
        labelName = self.ifLabelList.pop(-1)
        if self.controllFlowList[-1].has_else == False:
            code += self.tabs + "endif_"+str(labelName) + ":\n"   
        else:
            code += self.tabs + "endElse_"+str(labelName) + ":\n" 
        self.controllFlowList.pop(-1)         
        return code
    def Break(self, instList, instIdx, argList):
        code = ""
        scopeCounter = 0
        while 1:
            if instList[instIdx].name == "OPENSCOPE":
                scopeCounter += 1
            elif instList[instIdx].name == "REPEAT":
                break
            instIdx -= 1
            if instIdx < 0:
                raise Exception("Could not find repeate to close")
        for i in range(scopeCounter):
            code += self.tabs + "mov esp, ebp\n"
            code += self.tabs + "pop ebp\n"
        code += self.tabs + "jmp endRepeat_" + str(self.repeatLabelList[-1]) + "\n"
        return code
    def CreateFunction(self, instList, instIdx, argList):
        code = ""
        functionName = argList[0]
        returnTypeList = argList[1].split("~")
        if len(returnTypeList) == 1:
            if returnTypeList[0] == "void":
                returnTypeList = []
        paramList = argList[2].split("~")
        paramNameList = []
        paramTypeList = []
        if len(paramList) == 1 and paramList[0] == "void":
            pass
        else:
            for i in range(0, len(paramList), 2):
                paramTypeList.append(paramList[i])
                paramNameList.append(paramList[i+1])
        self.functionList.append(Function(functionName, returnTypeList, paramTypeList, paramNameList ))
        code += argList[0]+":\n"
        self.tabs += "\t"
        return code
    def EndFunction(self, instList, instIdx, argList):
        code = ""
        self.tabs = self.tabs[1:]
        code += self.tabs + "ret\n"
        return code
    def Call(self, instList, instIdx, argList):
        code = ""
        writeInto = argList.pop(0)
        functionName = argList.pop(0)
        self.includeCode += self.CheckAndIncludeBuiltInFunction(functionName)
        for a in argList:
            code += self.tabs + "mov eax, " + self.GetOperandAsString(a) + "\n"
            code += self.tabs + "push eax\n"
        code += self.tabs + "call " + functionName + "\n"
        for a in argList:
            code += self.tabs + "add esp, 4\n"
        return code
    def LogicalNot(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "not " + self.GetOperandAsString(argList[0]) + "\n"
        code += self.tabs + "and " + self.GetOperandAsString(argList[0]) + ", 1\n"
        return code
    def BitwiseNot(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "not " + self.GetOperandAsString(argList[0]) + "\n"
        return code
    def Mod(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "mov ebx, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "xor edx, edx\n"
        code += self.tabs + "idiv ebx\n"
        code += self.tabs + "mov "+self.GetOperandAsString(argList[0])+", edx\n"
        return code
    def Times(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "imul eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def Division(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "mov ebx, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "xor edx, edx\n"
        code += self.tabs + "idiv ebx\n"
        code += self.tabs + "mov "+self.GetOperandAsString(argList[0])+", eax\n"
        return code
    def LogicalOr(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "or eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def BitwiseOr(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "or eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def BitwiseAnd(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "and eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def RightShift(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "shr eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def LeftShift(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "mov eax, " + self.GetOperandAsString(argList[1]) + "\n"
        code += self.tabs + "shl eax, " + self.GetOperandAsString(argList[2]) + "\n"
        code += self.tabs + "mov " + self.GetOperandAsString(argList[0]) + ", eax\n"
        return code
    def GetMemoryAddress(self, instList, instIdx, argList):
        code = ""
        wi = self.GetVariableByName(argList[0])
        var = self.GetVariableByName(argList[1])
        code += f"{self.tabs}lea eax, [{var.GetMemoryAddress(self.scopeList)}]\n"
        code += self.tabs + f"mov {wi.AsString(self.scopeList)}, eax\n"
        return code
    def DrefMov(self, instList, instIdx, argList):
        code = ""
        wi = self.GetVariableByName(argList[0])
        if self.IsVariable(argList[1]):
            v = self.GetVariableByName(argList[1])
            inst = "movzx" if wi.dataType.GetSize() > v.dataType.GetSize() else "mov"
            reg = GetRegisterFromSize(wi.dataType.GetSize())
            code += f"{self.tabs}{inst} {reg}, {v.AsString(self.scopeList)}\n"
        else:
            reg = argList[1]
        
        ptrReg = GetRegisterFromSize(wi.dataType.GetSize(), "b")
        code += f"{self.tabs}mov {ptrReg}, {wi.AsString(self.scopeList)}\n"

        code += f"{self.tabs}mov {wi.dataType.AsSizeString()}{ptrReg}, {reg}\n"
        return code
    
    ###########
    #stuff
    ###########
    def GetFunctionForInstruction(self, instName):
        lst = [
            ["MOV", self.Mov],
            ["DREF_MOV", self.DrefMov],
            ["CREATE", self.Create],
            ["CREATE_TEMP_VAR", self.Create],
            ["CREATE_ARGUMENT", self.CreateArgument],
            ["REPEAT", self.Repeat],
            ["OPENSCOPE", self.OpenScope],
            ["CLOSESCOPE", self.CloseScope],
            ["<", self.LessThan],
            [">", self.GreaterThan],
            ["IF", self.If],
            ["ELSE", self.Else],
            ["ENDIF", self.EndIf],
            ["ENDELSE", self.EndIf],
            ["ENDREPEAT", self.EndRepeat],
            ["BREAK", self.Break],
            ["+", self.Add],
            ["-", self.Sub],
            ["==", self.Equals],
            ["!=", self.NotEquals],
            ["CREATE_FUNCTION", self.CreateFunction],
            ["END_FUNCTION", self.EndFunction],
            ["CALL", self.Call],
            ["!", self.LogicalNot],
            ["~", self.BitwiseNot],
            ["%", self.Mod],
            ["*", self.Times],
            ["/", self.Division],
            ["//", self.Division],
            ["or", self.LogicalOr],
            ["&&", self.BitwiseAnd],
            ["|", self.BitwiseOr],
            [">>", self.RightShift],
            ["<<", self.LeftShift],
            ["&", self.GetMemoryAddress]
        ]
        for i in lst:
            if i[0] == instName:
                return i[1]
        raise Exception("Failed to find instruction name -> " + instName)
    def AddPlatformSpecificCode(self, code):
        if platform == "COS":
            appendCode = ""            
            appendCode += "[BITS 16]\n"
            appendCode += "ORG 0x7e00\n"
            appendCode += "dd 4\n"
            appendCode += "jmp _main\n"
            appendCode += ";!!!!!!!!!!!!!!!!\n"
            appendCode += """
                %macro Print 1
                    pushad
                    mov al, %1
                    mov ah, 0x9
                    mov bh, 0
                    mov bl, 0x2 ; green
                    mov cx, 1
                    int 0x10
                    popad
                %endmacro
            \n"""
            code = appendCode + code
            code += "times 512*4-($-$$) db 0"
        return code
    def AddDataBlocks(self,code):
        code += "\n\n;--CONSTANTS--\n"
        for db in self.dataBlockList:
            code += db.AsString()
        return code
    def ExpandListOperations(self,instList):
        i = 0
        #while i < len(instList):

        #    i += 1
        return instList
    def UpdateIrForAsm(self, instList):
        instList = self.ExpandListOperations(instList)        
        return instList
    def Convert(self, instList, settings):
        UpdateSettings(settings)
        instList = self.UpdateIrForAsm(instList)
        self.includeCode = ""
        self.scopeList = [Scope(0)]
        self.tabs = ""
        code = ""
        for instIdx,inst in enumerate(instList):            
            func = self.GetFunctionForInstruction(inst.name)
            newCode = ""
            if self.commentIR:
                newCode += self.tabs + ";" + inst.Print(ret=True)+"\n"
            newCode += func(instList, instIdx, inst.argList)            
            #print(newCode,end="")
            code += newCode
        code = self.includeCode + code
        code = self.AddPlatformSpecificCode(code)
        code = self.AddDataBlocks(code)
        return code