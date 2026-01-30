import Operators
import Types
import re
import StdFunctions


constantStatus = {
    "UNKNOWN": 0,
    "CONSTANT": 1,
    "NON_CONSTANT": 2
}

class Bound():
    def __init__(self, start, end, value):
        self.start = start
        self.end = end
        self.value = value
    def __str__(self):
        return f"[{self.start}->{self.value}<-{self.end}]"
    __repr__ = __str__

#TODO this does cause the prob of not allowing functions within different scopes to have
#the same name as each other but i am lazy

functionList = None

class Function():
    def __init__(self, name, returnTypeString):
        self.returnList = returnTypeString.split("~")
        self.name = name

class Var:
    def __init__(self, name, dataType):
        self.name = name
        self.dataType = dataType
        self.fixedDataType = dataType != "UNKNOWN"
        self.constantList = [Bound(0,2**64-1, constantStatus["UNKNOWN"])]
        #TODO propergate types when doing CALL
        #TODO bug obvs doesnt work because value changes and pointers change therefore
        #Maybe keep list of values to different regions of code or something idk
        #Also a bug where if a var changes itself it still thinks it is constant when it is not e.g !
        self.valueList = []  # actual constant value if known
        #Sometimes pointers point to known varaibles used for expressions
        #Needed to propergate consts when mem address are known variables

    def setConstant(self, value, lineNumber, instList):
        for idx,i in enumerate(self.constantList):
            if i.start <= lineNumber:
                if i.end >= lineNumber:
                    #Dont have multiple bounds for same value
                    if i.value == value:
                        return
                    self.constantList[idx].end = lineNumber-1
        b = Bound(lineNumber, len(instList), value)
        self.constantList.append(b)
    def getConstant(self, lineNumber):
        for i in self.constantList:
            if i.start <= lineNumber:
                if i.end >= lineNumber:
                    return i.value
        raise Exception("Does not have a constant value for line number "+str(lineNumber))
    def getValue(self,lineNumber):
        for i in self.valueList:
            if i.start <= lineNumber:
                if i.end >= lineNumber:
                    return i.value
        raise Exception("Does not have a value for line number "+str(lineNumber))
    def addValue(self, value, lineNumber, instList):
        for idx,i in enumerate(self.valueList):
            if i.start <= lineNumber:
                if i.end >= lineNumber:
                    #Dont have multiple bounds for same value
                    if i.value == value:
                        return
                    self.valueList[idx].end = lineNumber-1
        b = Bound(lineNumber, len(instList), value)
        self.valueList.append(b)

def getFuncByName(string):
    for i in functionList:
        if i.name == string:
            return i
    raise Exception("Failed to find func with name " + str(string))
def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def getValueOfConstArg(arg, currentScope, lineNumber):
    if isNumber(arg):
        return arg
    else:
        return getVarByName(arg, currentScope).getValue(lineNumber)
def getTypeAndIsConstant(string, currentScope, lineNumber):
    # literal number
    if isNumber(string):
        if "." in string:
            return "f32", constantStatus["CONSTANT"]
        else:
            return "i32", constantStatus["CONSTANT"]
    # explicit type name
    if isDataType(string):
        return string, constantStatus["CONSTANT"]
    # variable
    var = getVarByName(string, currentScope)
    return var.dataType, var.getConstant(lineNumber)
def isDataType(string):
    string = re.split(r"[\[\]\$]", string)
    if len(string) == 0:
        return False
    typeName = string[0]
    if typeName in Types.typeNameList:
        return True
    return False
def getVarByName(string, currentScope):
    while currentScope != None:
        for i in currentScope.varList:
            if i.name == string:
                return i
        currentScope = currentScope.parent
    raise Exception("Cant find var with name " + str(string))


class Scope():
    def __init__(self):
        self.varList = []
        self.childScopeList = []
        self.parent = None
    def print(self, tabs=""):
        for i in self.varList:
            print(f"{tabs}{i.name}-{i.dataType}-{i.constantList}-{i.fixedDataType}")
        for i in self.childScopeList:
            print(f"{tabs}[")
            i.print(tabs+"\t")
            print(f"{tabs}]")

def generateScope(instList):
    currentScope = Scope()
    mainScope = currentScope
    for i in instList:
        if i.name == "OPENSCOPE":
            newScope = Scope()
            newScope.parent = currentScope
            currentScope.childScopeList.append(newScope)
            currentScope = newScope
        elif i.name == "CLOSESCOPE":
            currentScope = currentScope.parent
        elif i.name in ["CREATE", "CREATE_TEMP_VAR", "CREATE_ARGUMENT"]:
            var = Var(i.argList[1], i.argList[0])
            currentScope.varList.append(var)
    return mainScope

def UpdateIRcode(instList, mainScope):
    currentScope = mainScope
    scopeIndexCounterList = [0]
    madeChange = False
    for lineNumber,i in enumerate(instList):
        instName = i.name
        if instName == "OPENSCOPE":
            currentScope = currentScope.childScopeList[scopeIndexCounterList[-1]]
            scopeIndexCounterList.append(0)
        elif instName == "CLOSESCOPE":
            scopeIndexCounterList = scopeIndexCounterList[:-1]
            scopeIndexCounterList[-1] += 1
            currentScope = currentScope.parent
        if instName not in ["CREATE", "CREATE_TEMP_VAR", "CREATE_ARGUMENT"] and instName not in ["DREF_MOV"]:
            for argIndex,arg in enumerate(i.argList[1:]):
                #Offset by one because starting at index 1
                argIndex += 1
                var = None
                try:
                    var = getVarByName(arg, currentScope)           
                except Exception:
                    pass
                if var != None:
                    if var.getConstant(lineNumber) == constantStatus["CONSTANT"]:
                        i.argList[argIndex] = var.getValue(lineNumber)
                        madeChange = True
        else:
            if instName in ["DREF_MOV"]:
                var = None
                try:
                    var = getVarByName(i.argList[0], currentScope)           
                except Exception:
                    pass
                if var != None:
                    if var.getConstant(lineNumber) == constantStatus["CONSTANT"]:
                        #Pointers directly pointing to a var can just be replaced with a mov
                        #when writing to
                        i.name = "MOV"
                        i.argList[0] = var.getValue(lineNumber)[1:]
                        madeChange = True
            else:
                var = getVarByName(i.argList[1], currentScope)
                i.argList[0] = var.dataType
    return madeChange

def Iteration(instList, mainScope):
    currentScope = mainScope
    madeChange = True
    while madeChange:
        madeChange = False
        scopeIndexCounterList = [0]
        for lineNumber,i in enumerate(instList):
            inst = i
            instName = i.name

            # --- Scope handling ---
            if instName == "OPENSCOPE":
                currentScope = currentScope.childScopeList[scopeIndexCounterList[-1]]
                scopeIndexCounterList.append(0)

            elif instName == "CLOSESCOPE":
                scopeIndexCounterList = scopeIndexCounterList[:-1]
                scopeIndexCounterList[-1] += 1
                currentScope = currentScope.parent

            # --- MOV propagation ---
            elif instName == "MOV":
                dstName = inst.argList[0]
                srcToken = inst.argList[1]
                dst = getVarByName(dstName, currentScope)
                srcType, srcConst = getTypeAndIsConstant(srcToken, currentScope, lineNumber)

                # Type propagation
                if not dst.fixedDataType and dst.dataType != srcType:
                    dst.dataType = srcType
                    #TODO maybe make types win out over other types idk
                    dst.fixedDataType = True
                    madeChange = True

                # Constantness propagation
                if srcConst > dst.getConstant(lineNumber):
                    dst.setConstant(srcConst,lineNumber, instList)
                    madeChange = True
                    if srcConst == constantStatus["CONSTANT"]:
                        value = getValueOfConstArg(srcToken, currentScope, lineNumber)  
                        dst.addValue(value, lineNumber, instList)            
            elif instName == "&":
                var = getVarByName(i.argList[1], currentScope)
                to = getVarByName(i.argList[0], currentScope)
                newDataType = var.dataType+"$"
                if to.fixedDataType == False and to.dataType != newDataType:
                    to.dataType = newDataType
                    to.fixedDataType = True
                    madeChange = True
                if to.getConstant(lineNumber) < constantStatus["CONSTANT"]:
                    to.setConstant(constantStatus["CONSTANT"],lineNumber, instList)
                    madeChange = True
                if to.getConstant(lineNumber) == constantStatus["CONSTANT"]:  
                    to.addValue("&"+var.name, lineNumber, instList)  
            elif instName == "CREATE_FUNCTION":
                func = Function(i.argList[0],i.argList[1])
                functionList.append(func)
            elif instName == "CALL":
                if i.argList[1] not in StdFunctions.compileTimeFunctionList:
                    to = getVarByName(i.argList[0], currentScope)
                    func = getFuncByName(i.argList[1])
                    #TODO just assume 0 for now not quit supported multi value returns
                    newDataType = "void "if len(func.returnList) == 0 else func.returnList[0]
                    if to.fixedDataType == False and to.dataType != newDataType:
                        to.dataType = newDataType
                        dst.fixedDataType = True
                        madeChange = True
            # --- Operator propagation and folding ---
            elif instName in Operators.operatorNameList and instName != "&":
                selfName = inst.argList[0]
                selfVar = getVarByName(selfName, currentScope)

                operandTypes = []
                operandConsts = []
                operandTokens = inst.argList[1:]

                for arg in operandTokens:
                    t, c = getTypeAndIsConstant(arg, currentScope, lineNumber)
                    operandTypes.append(t)
                    operandConsts.append(c)

                # Type propagation
                if instName in Operators.boolOperatorNames:
                    if not selfVar.fixedDataType and selfVar.dataType != "ui8":
                        selfVar.dataType = "ui8"
                        selfVar.fixedDataType = True
                        madeChange = True
                else:
                    #TODO link to the Types py file
                    newType = operandTypes[0]
                    #newType = promote_types(operandTypes)
                    if not selfVar.fixedDataType and selfVar.dataType != newType:
                        selfVar.dataType = newType
                        dst.fixedDataType = True
                        madeChange = True

                # Constantness propagation
                if constantStatus["NON_CONSTANT"] in operandConsts:
                    if selfVar.getConstant(lineNumber) != constantStatus["NON_CONSTANT"]:
                        selfVar.setConstant(constantStatus["NON_CONSTANT"],lineNumber, instList)
                        madeChange = True
    #Values have converged now 
    mainScope.print()
    



#Expects ?= operators to be expanded to normal operators
def PropergateValues(instList):
    global functionList
    change = True
    mainScope = generateScope(instList)
    mainScope.print()
    functionList = []
    for i in StdFunctions.stdFunctionList:
        functionList.append(Function(i.name, "~".join(i.returnTypeList)))
    Iteration(instList, mainScope)
    while change:
        change = False
        change = change or UpdateIRcode(instList, mainScope)
        pass