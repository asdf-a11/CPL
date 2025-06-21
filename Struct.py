import Function
import IR

class Struct():
    def __init__(self):
        self.name = None
        self.varNameList = []
        self.varTypeList = []
        self.functionList = []
    def GetFunctionDefinitionIrCode(self):  
        out = []      
        for f in self.functionList:
            irList = f.IRList.copy()
            irList[0].argList[2] += f"~{self.name}$~this"
            irList[0].argList[0] = self.name+"::"+irList[0].argList[0]
            irList.insert(2,
                IR.Instruction("CREATE_ARGUMENT", [self.name+"$", "this"])
            )
            out += irList
        return out


    
def CreateStruct(tokenList, idx):
    if tokenList[idx].tokenType != "STRUCT":
        raise Exception("Can create struct from not struct")
    s = Struct()
    if tokenList[idx+1].tokenType != "NAME":
        raise Exception("Expecting a name after struct keyword")
    s.name = tokenList[idx+1].tokenContent

    #Read in the data in the struct as if it were a function
    func = Function.Function()
    endOfStructIdx = func.ReadInScope(tokenList, 2)

    #Convert it to IR code

    func.GenerateIR()
    irList = func.IRList

    #Find all variables defined as part of the struct

    scopeCounter = 0
    for inst in irList:
        if inst.name == "OPENSCOPE":
            scopeCounter += 1
        if inst.name == "CLOSESCOPE":
            scopeCounter -= 1
        if inst.name == "CREATE" and scopeCounter == 1:
            if inst.argList[1][0] == "_":
                s.varTypeList.append(inst.argList[0])
                s.varNameList.append(inst.argList[1])

    #Find and set all functions defined

    for instIndex,inst in enumerate(irList):
        if inst.name == "CREATE_FUNCTION" and instIndex != 0:
            f = Function.Function(
                name=inst.argList[0],
                returnTypeList=inst.argList[1].split("~"),
                perameterTypeList=inst.argList[2].split("~")[0::2],
                perameterNameList=inst.argList[2].split("~")[1::2]
            )

            funcDepthCounter = 0
            for i in irList[instIndex:]:
                if i.name == "CREATE_FUNCTION":
                    #Runs include function self therefore funcDepthCounter is 1
                    #when on highest depth
                    funcDepthCounter += 1
                if i.name == "END_FUNCTION":
                    if funcDepthCounter ==  1:
                        f.IRList.append(i)
                        break
                    funcDepthCounter -= 1
                f.IRList.append(i)

            s.functionList.append(f)
    
    return endOfStructIdx, s
        