import Lexer
import IR
import IRConversion
import os
import time
import IROptimise
import PreProcessor
import Settings
import Function

def Compile(sourceCode, outputPreProcessedCode=False):    
    startPreProc = time.time()
    sourceCode = PreProcessor.PreProcess(sourceCode)
    print("PreProc took -> ", time.time() - startPreProc)
    if outputPreProcessedCode:
        f = open(f"Compiled{Settings.FILE_SEPERATOR}PreProc.txt", "w")
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
    wholeProgramIR = []
    wholeProgramFunction = Function.Function(
        name="cplMain"
    )
    wholeProgramFunction.tokenList = tokenList
    wholeProgramFunction.GenerateIR()
    wholeProgramIR = wholeProgramFunction.IRList
    
    programIR = IR.PrintInstList(wholeProgramIR, ret=True)
    #
    f = open("Compiled/irCode_unOptimised.txt","w")
    f.write(programIR)
    f.close()
    #
    programIR = IROptimise.PerformOperations(programIR)
    f = open("Compiled/irCode.txt","w")
    f.write(programIR)
    f.close()
    #settingsString_x86 = "-m86 -COS"
    #outputProgram = IRConversion.Convert(programIR, "x86", settingsString_x86)
    outputProgram = IRConversion.Convert(programIR, "cpp", "")
    return outputProgram

    
if __name__ == "__main__":
    print("Starting")
    
    f = open("InputCode/code.cpl","r")
    content = f.read()
    f.close()
    start = time.time()
    program = Compile(content,
        outputPreProcessedCode=True                  
    )
    print("Compiled in -> ", time.time() - start)
    print("\n\n---Prog---\n", program)
    f = open("Compiled/out.cpp", "w")
    f.write(program)
    f.close()
    if True:
        execString = [
            "g++ Compiled/out.cpp",
            "./a.out"
        ]
        os.system(" && ".join(execString))
    #os.system("nasm -f bin Compiled/out.asm -o Compiled\out.bin")
    #os.system("nasm -f bin Compiled/bootloader.asm -o Compiled/bootloader.bin")
    ##os.system("copy /b Compiled\\bootloader.bin Compiled\\os.flp")
    #os.system("copy /b Compiled\\bootloader.bin + Compiled\\out.bin Compiled\\os.flp")
    ##command = open("Compiled/run.cmd","r").read()
    ##os.system(command)
    print("Done")

'''
<!DOCTYPE html>
<html>
<body>

<h2>A polygon with four sides</h2>

<svg height="250" width="500">
  <polygon points="130,125 0,125 130,250 350,200" style="fill:rgb(140,35,40);" />  
  <polygon points="0,125 130,125 130,125 130, 0" style="fill:rgb(230,25,25);" />
  <polygon points="130,125 130, 0 350,50" style="fill:rgb(230,25,25);" />
  <circle cx="130" cy="125" r="70" stroke="white" stroke-width="20" fill-opacity="0.0" />
  <polygon points="130,125 130,125 350,50 350,200" style="fill:rgb(185,25,28);" />
  <!--The P-->
  <rect width="10" height="75" x="230" y="87.5" style="fill:rgb(255,255,255);" />
  <rect width="40" height="10" x="230" y="87.5" style="fill:rgb(255,255,255);" />
  <rect width="10" height="40" x="260" y="87.5" style="fill:rgb(255,255,255);" />
  <rect width="40" height="10" x="230" y="117.5" style="fill:rgb(255,255,255);" />
  <!--The L-->
	<rect width="10" height="75" x="290" y="87.5" style="fill:rgb(255,255,255);" />
    <rect width="45" height="10" x="290" y="152.5" style="fill:rgb(255,255,255);" />
</svg>

</body>
</html>

'''

    
