class Scope():
    def __init__(self, something):
        pass
class Function():
    def __init__(self,name):
        self.argumentList = []
class Converter():
    def __init__(self):
        self.tabs = ""
        self.commentIR = False
        self.functionDefStringList = []
        self.firstFunction = True
    
    #############
    #convertion functions
    ##############
    def Mov(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + argList[0] + " = " + argList[1] + ";\n"
        return code
    def Ldr(self, instList, instIdx, argList):
        code = f"{self.tabs}{argList[0]} = {argList[1]}[{argList[2]}/sizeof(UNKNOWN)];\n"
        return code
    def Create(self, instList, instIdx, argList):
        code = ""
        t = argList[0]
        if "$" in t:
            t = f"CPLPtr<{t.replace("$","")}>"
        code += self.tabs + t + " " + argList[1] + ";\n"
        return code
    def CreateList(self, instList, instIdx, argList):
        t = argList[0]
        #code = f"{self.tabs}{t}* {argList[1]} = ({t}*)alloca(sizeof({t})*{argList[2]});\n"
        #code = f"{self.tabs}std::vector<{t}> {argList[1]}({argList[2]});\n"
        code = f"{self.tabs}CPL_LIST<{t}> {argList[1]}({argList[2]});\n"
        return code
    def SetList(self, instList, instIdx, argList):
        code = ""
        for i in range(1,len(argList)):
            code += f"{self.tabs}{argList[0]}[{i-1}] = {argList[i]};\n"
        return code
    def CreateArgument(self, instList, instIdx, argList):
        #self.functionList[-1].argumentList.append((argList[0], argList[1]))
        return ""
    def Repeat(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "while(1)\n"
        return code
    def EndRepeat(self, instList, instIdx, argList):
        return ""
    def OpenScope(self, instList, instIdx, argList):
        code = self.tabs + "{\n"
        self.tabs += "\t"
        return code
    def CloseScope(self, instList, instIdx, argList):
        self.tabs = self.tabs[:len(self.tabs)-1]
        v = ";" if len(self.tabs) != 0 else ""
        return self.tabs + "}"+v+"\n"
    def SingleOperandOperation(self, instList, instIdx, argList):
        code = ""
        opSymbol = instList[instIdx].name
        code += self.tabs + argList[0] + " = " + opSymbol + argList[1] + ";\n"
        return code
    def DoubleOperandOperation(self, instList, instIdx, argList):
        code = ""
        opSymbol = instList[instIdx].name
        code += self.tabs + argList[0] + " = " + argList[1] + " "+opSymbol+" " + argList[2] + ";\n"
        return code
    def DoubleOrSingleOperandOperation(self, instList, instIdx, argList):
        if len(argList) == 3:
            return self.DoubleOperandOperation(instList, instIdx, argList)
        elif len(argList) == 2:
            return self.SingleOperandOperation(instList, instIdx, argList)
        else:
            raise Exception("Invalid number of args for operand")
    def If(self, instList, instIdx, argList):
        return self.tabs + "if(" + argList[0] + ")\n"
    def EndIf(self, instList, instIdx, argList): return ""
    def Break(self, instList, instIdx, argList):
        return self.tabs + "break;\n"
    def CreateFunction(self, instList, instIdx, argList):
        if self.firstFunction:
            self.firstFunction = False
            code = self.tabs + argList[1] + " " + argList[0] + "("
            functionDefString = code
        else:
            code = f"{self.tabs}auto {argList[0]} = []("
            functionDefString = f"{argList[1]} (*{argList[0]})("
        functionArgumentList = argList[2].split("~")
        paramString = ""
        for idx,i in enumerate(functionArgumentList):
            #if i == "void": continue
            paramString += i
            if idx != len(functionArgumentList)-1:
                paramString += " " if idx % 2 == 0 else ", "
        paramString += ")"
        functionDefString += paramString
        code += paramString
        self.functionDefStringList.append(functionDefString)
        code += "\n"
        return code
    def EndFunction(self, instList, instIdx, argList):
        return ""
    def Else(self, instList, instIdx, argList):
        code = self.tabs + "else\n"
        return code
    def GetMemoryAddress(self, instList, instIdx, argList):
        return f"{self.tabs}{argList[0]} = &({argList[1]});\n"
    def Call(self, instList, instIdx, argList):
        code = self.tabs + argList[1] + "("
        for i in range(2, len(argList)):
            code += argList[i]
            if i != len(argList)-1:
                code += ", "
        code += ");\n"
        return code
    def CreateStruct(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + "struct " + argList[0] + "{\n"
        nameList = argList[1].split("~")[1::2]
        typeList = argList[1].split("~")[0::2]
        for n, t in zip(nameList, typeList):
            code += self.tabs + "\t" + t + " " + n + ";\n"
        code += self.tabs + "};\n"
        return code
    def DotOperator(self, instList, instIdx, argList):
        code = ""
        code += self.tabs + f"{argList[0]} = {argList[1]}.{argList[2]};\n"
        return code
    def DrefMov(self, instList, instIdx, argList):
        code = self.tabs + f"*({argList[0]}) = {argList[1]};\n"
        return code
    def Nop(self, instList, instIdx, argList):
        return ""
    ###########
    #stuff
    ###########
    def GetFunctionForInstruction(self, instName):
                    #["LDR", self.Ldr], should be $
        lst = [  
            ["NOP", self.Nop] ,         
            ["MOV", self.Mov],
            ["DREF_MOV", self.DrefMov],
            ["CREATE", self.Create],
            ["CREATE_TEMP_VAR", self.Create],
            ["CREATELIST", self.CreateList],
            ["SETLIST", self.SetList],
            ["CREATE_STRUCT", self.CreateStruct],
            ["CREATE_ARGUMENT", self.CreateArgument],
            ["REPEAT", self.Repeat],
            ["OPENSCOPE", self.OpenScope],
            ["CLOSESCOPE", self.CloseScope],
            ["<", self.DoubleOperandOperation],
            [">", self.DoubleOperandOperation],
            ["IF", self.If],
            ["ELSE", self.Else],
            ["ENDIF", self.EndIf],
            ["ENDELSE", self.EndIf],
            ["ENDREPEAT", self.EndRepeat],
            ["BREAK", self.Break],
            ["+", self.DoubleOperandOperation],
            ["-", self.DoubleOrSingleOperandOperation],
            ["==", self.DoubleOperandOperation],
            ["!=", self.DoubleOperandOperation],
            ["CREATE_FUNCTION", self.CreateFunction],
            ["END_FUNCTION", self.EndFunction],
            ["CALL", self.Call],
            ["!", self.SingleOperandOperation],
            ["~", self.SingleOperandOperation],
            ["%", self.DoubleOperandOperation],
            ["*", self.DoubleOperandOperation],
            ["/", self.DoubleOperandOperation],
            ["//", self.DoubleOperandOperation],
            ["or", self.DoubleOperandOperation],
            ["&&", self.DoubleOperandOperation],
            ["|", self.DoubleOperandOperation],
            [">>", self.DoubleOperandOperation],
            ["<<", self.DoubleOperandOperation],
            ["&", self.GetMemoryAddress],
            [".", self.DotOperator]
        ]
        for i in lst:
            if i[0] == instName:
                return i[1]
        raise Exception("Failed to find instruction name -> " + instName)
    def CleanInstructionArgList(self, argList):
        cleanedList = []
        for arg in argList:
            cleanedList.append(arg.replace("_","").replace("#", ""))
        return cleanedList
    def PreCode(self):
        defines = """
#define SAFE true
#include <iostream>
#include <vector>
#include <cstddef>
#include \"../CppFiles/CplCppList.hpp\"
#include \"../CppFiles/CplPtr.hpp\"
#include \"../CppFiles/CPLGraphics.hpp\"

#define i32 int
#define i16 short
#define i8 signed char
#define f32 float
#define UNKNOWN int
#define byte unsigned char

#define VARTYPE sizeof(int)

void printc(i32 character){
    std::cout << (char)character;
}
void printf(f32 value){
    std::cout << value;
}
void printn(i32 value){
    std::cout << value;
}

"""
        return defines
    def AfterCode(self):
        string = """

int main(){
    cplMain();
    return 0;
}

"""
        return string
    def AddFunctionDeclorations(self):
        code = ""
        for i in self.functionDefStringList:
            code += i + ";\n"
        code += "\n"
        return code
    def CleanInstructionList(self, instList):
        for inst in instList:
            for a in range(len(inst.argList)):
                if "::" in inst.argList[a]:
                    l = inst.argList[a].split("::")
                    inst.argList[a] = f"CPLPtr<char>((void*)(offsetof({l[0]},{l[1]})))"
                    if inst.name == "CREATE":
                        inst.name = "NOP"
                        break
    def Convert(self, instList, settings):
        self.scopeList = [Scope(0)]
        self.tabs = ""
        code = ""
        self.CleanInstructionList(instList)
        for instIdx,inst in enumerate(instList):            
            func = self.GetFunctionForInstruction(inst.name)
            if func == None: continue
            newCode = ""
            if self.commentIR:
                newCode += self.tabs + "//" + inst.Print(ret=True)+"\n"
            cleanedArgList = self.CleanInstructionArgList(inst.argList)
            newCode += func(instList, instIdx, cleanedArgList)            
            code += newCode
        code = self.PreCode() + code + self.AfterCode()#self.AddFunctionDeclorations()
        return code

#define or ||
#define and &&  

'''
["CREATE", self.Create],
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
'''