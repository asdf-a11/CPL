#To beat 5500
import Lexer
import FirstLayerParser
import IR
import IRConversion
import os
import time
import IROptimise
import PreProcessor

def Compile(sourceCode):    
    startPreProc = time.time()
    sourceCode = PreProcessor.PreProcess(sourceCode)
    print("PreProc took -> ", time.time() - startPreProc)
    f = open("Compiled\\PreProc.txt", "w")
    f.write(sourceCode)
    f.close()    
    startLexingTime = time.time()
    splitList = Lexer.GenerateSplitList(sourceCode)
    tokenList = Lexer.GenerateTokenList(splitList)       
    tokenList = Lexer.RemoveComments(tokenList)
    Lexer.PrintTokenList(tokenList)
    tokenList = Lexer.RemoveWhiteSpace(tokenList)
    Lexer.PrintTokenList(tokenList)
    print("Lexing took -> ", time.time() - startLexingTime)
    functionList = FirstLayerParser.FirstLayerParse(tokenList)
    for f in functionList:
        f.GenerateIR()
    wholeProgramIR = []
    for f in functionList:
        wholeProgramIR += f.IRList
    
    programIR = IR.PrintInstList(wholeProgramIR, ret=True)
    f = open("Compiled/irCode_unOptimised.txt","w")
    f.write(programIR)
    f.close()
    #programIR = IROptimise.PerformOperations(programIR)
    #f = open("Compiled/irCode.txt","w")
    #f.write(programIR)
    #f.close()
    #settingsString_x86 = "-m86 -COS"
    #outputProgram = IRConversion.Convert(programIR, "x86", settingsString_x86)
    outputProgram = IRConversion.Convert(programIR, "cpp", "")
    return outputProgram

    
if __name__ == "__main__":
    print("Starting")
    
    f = open("code.cpl","r")
    content = f.read()
    f.close()
    start = time.time()
    program = Compile(content)
    print("Compiled in -> ", time.time() - start)
    print("\n\n---Prog---\n", program)
    #f = open("Compiled/out.cpp", "w")
    #f.write(program)
    #f.close()
    if True == True:
        execString = [
            "g++ Compiled/out.cpp",
            "a.exe"
        ]
        os.system(" && ".join(execString))
    #os.system("nasm -f bin Compiled/out.asm -o Compiled\out.bin")
    #os.system("nasm -f bin Compiled/bootloader.asm -o Compiled/bootloader.bin")
    ##os.system("copy /b Compiled\\bootloader.bin Compiled\\os.flp")
    #os.system("copy /b Compiled\\bootloader.bin + Compiled\\out.bin Compiled\\os.flp")
    ##command = open("Compiled/run.cmd","r").read()
    ##os.system(command)
    print("Done")

    
