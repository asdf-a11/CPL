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
    tokenList = Lexer.ConcaternateStrings(tokenList)
    tokenList = Lexer.StringsToLists(tokenList)
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
    #print(programIR[:200*len("CREATE_TEMP_VAR i32, EXP_TEMP_VAR_0")])
    f = open("Compiled/irCode.txt","w")
    f.write(programIR)
    f.close()
    settingsString_x86 = "-m86 -COS"
    outputProgram = IRConversion.Convert(programIR, "x86", settingsString_x86)
    #outputProgram = IRConversion.Convert(programIR, "cpp", "")
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
            "g++ Compiled/out.cpp -lX11",# -luser32 -lgdi32
            "./a.out"
            #"start a.exe"
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

'''
0
: 
"rgb(0, 0, 0)"
1
: 
"rgb(0, 0, 170)"
2
: 
"rgb(0, 170, 0)"
3
: 
"rgb(0, 170, 170)"
4
: 
"rgb(170, 0, 0)"
5
: 
"rgb(170, 0, 170)"
6
: 
"rgb(170, 85, 0)"
7
: 
"rgb(170, 170, 170)"
8
: 
"rgb(85, 85, 85)"
9
: 
"rgb(85, 85, 255)"
10
: 
"rgb(85, 255, 85)"
11
: 
"rgb(85, 255, 255)"
12
: 
"rgb(255, 85, 85)"
13
: 
"rgb(255, 85, 255)"
14
: 
"rgb(255, 255, 85)"
15
: 
"rgb(255, 255, 255)"
16
: 
"rgb(0, 0, 0)"
17
: 
"rgb(16, 16, 16)"
18
: 
"rgb(32, 32, 32)"
19
: 
"rgb(53, 53, 53)"
20
: 
"rgb(69, 69, 69)"
21
: 
"rgb(85, 85, 85)"
22
: 
"rgb(101, 101, 101)"
23
: 
"rgb(117, 117, 117)"
24
: 
"rgb(138, 138, 138)"
25
: 
"rgb(154, 154, 154)"
26
: 
"rgb(170, 170, 170)"
27
: 
"rgb(186, 186, 186)"
28
: 
"rgb(202, 202, 202)"
29
: 
"rgb(223, 223, 223)"
30
: 
"rgb(239, 239, 239)"
31
: 
"rgb(255, 255, 255)"
32
: 
"rgb(0, 0, 255)"
33
: 
"rgb(65, 0, 255)"
34
: 
"rgb(130, 0, 255)"
35
: 
"rgb(190, 0, 255)"
36
: 
"rgb(255, 0, 255)"
37
: 
"rgb(255, 0, 190)"
38
: 
"rgb(255, 0, 130)"
39
: 
"rgb(255, 0, 65)"
40
: 
"rgb(255, 0, 0)"
41
: 
"rgb(255, 65, 0)"
42
: 
"rgb(255, 130, 0)"
43
: 
"rgb(255, 190, 0)"
44
: 
"rgb(255, 255, 0)"
45
: 
"rgb(190, 255, 0)"
46
: 
"rgb(130, 255, 0)"
47
: 
"rgb(65, 255, 0)"
48
: 
"rgb(0, 255, 0)"
49
: 
"rgb(0, 255, 65)"
50
: 
"rgb(0, 255, 130)"
51
: 
"rgb(0, 255, 190)"
52
: 
"rgb(0, 255, 255)"
53
: 
"rgb(0, 190, 255)"
54
: 
"rgb(0, 130, 255)"
55
: 
"rgb(0, 65, 255)"
56
: 
"rgb(130, 130, 255)"
57
: 
"rgb(158, 130, 255)"
58
: 
"rgb(190, 130, 255)"
59
: 
"rgb(223, 130, 255)"
60
: 
"rgb(255, 130, 255)"
61
: 
"rgb(255, 130, 223)"
62
: 
"rgb(255, 130, 190)"
63
: 
"rgb(255, 130, 158)"
64
: 
"rgb(255, 130, 130)"
65
: 
"rgb(255, 158, 130)"
66
: 
"rgb(255, 190, 130)"
67
: 
"rgb(255, 223, 130)"
68
: 
"rgb(255, 255, 130)"
69
: 
"rgb(223, 255, 130)"
70
: 
"rgb(190, 255, 130)"
71
: 
"rgb(158, 255, 130)"
72
: 
"rgb(130, 255, 130)"
73
: 
"rgb(130, 255, 158)"
74
: 
"rgb(130, 255, 190)"
75
: 
"rgb(130, 255, 223)"
76
: 
"rgb(130, 255, 255)"
77
: 
"rgb(130, 223, 255)"
78
: 
"rgb(130, 190, 255)"
79
: 
"rgb(130, 158, 255)"
80
: 
"rgb(186, 186, 255)"
81
: 
"rgb(202, 186, 255)"
82
: 
"rgb(223, 186, 255)"
83
: 
"rgb(239, 186, 255)"
84
: 
"rgb(255, 186, 255)"
85
: 
"rgb(255, 186, 239)"
86
: 
"rgb(255, 186, 223)"
87
: 
"rgb(255, 186, 202)"
88
: 
"rgb(255, 186, 186)"
89
: 
"rgb(255, 202, 186)"
90
: 
"rgb(255, 223, 186)"
91
: 
"rgb(255, 239, 186)"
92
: 
"rgb(255, 255, 186)"
93
: 
"rgb(239, 255, 186)"
94
: 
"rgb(223, 255, 186)"
95
: 
"rgb(202, 255, 186)"
96
: 
"rgb(186, 255, 186)"
97
: 
"rgb(186, 255, 202)"
98
: 
"rgb(186, 255, 223)"
99
: 
"rgb(186, 255, 239)"
[100 … 199]
100
: 
"rgb(186, 255, 255)"
101
: 
"rgb(186, 239, 255)"
102
: 
"rgb(186, 223, 255)"
103
: 
"rgb(186, 202, 255)"
104
: 
"rgb(0, 0, 113)"
105
: 
"rgb(28, 0, 113)"
106
: 
"rgb(57, 0, 113)"
107
: 
"rgb(85, 0, 113)"
108
: 
"rgb(113, 0, 113)"
109
: 
"rgb(113, 0, 85)"
110
: 
"rgb(113, 0, 57)"
111
: 
"rgb(113, 0, 28)"
112
: 
"rgb(113, 0, 0)"
113
: 
"rgb(113, 28, 0)"
114
: 
"rgb(113, 57, 0)"
115
: 
"rgb(113, 85, 0)"
116
: 
"rgb(113, 113, 0)"
117
: 
"rgb(85, 113, 0)"
118
: 
"rgb(57, 113, 0)"
119
: 
"rgb(28, 113, 0)"
120
: 
"rgb(0, 113, 0)"
121
: 
"rgb(0, 113, 28)"
122
: 
"rgb(0, 113, 57)"
123
: 
"rgb(0, 113, 85)"
124
: 
"rgb(0, 113, 113)"
125
: 
"rgb(0, 85, 113)"
126
: 
"rgb(0, 57, 113)"
127
: 
"rgb(0, 28, 113)"
128
: 
"rgb(57, 57, 113)"
129
: 
"rgb(69, 57, 113)"
130
: 
"rgb(85, 57, 113)"
131
: 
"rgb(97, 57, 113)"
132
: 
"rgb(113, 57, 113)"
133
: 
"rgb(113, 57, 97)"
134
: 
"rgb(113, 57, 85)"
135
: 
"rgb(113, 57, 69)"
136
: 
"rgb(113, 57, 57)"
137
: 
"rgb(113, 69, 57)"
138
: 
"rgb(113, 85, 57)"
139
: 
"rgb(113, 97, 57)"
140
: 
"rgb(113, 113, 57)"
141
: 
"rgb(97, 113, 57)"
142
: 
"rgb(85, 113, 57)"
143
: 
"rgb(69, 113, 57)"
144
: 
"rgb(57, 113, 57)"
145
: 
"rgb(57, 113, 69)"
146
: 
"rgb(57, 113, 85)"
147
: 
"rgb(57, 113, 97)"
148
: 
"rgb(57, 113, 113)"
149
: 
"rgb(57, 97, 113)"
150
: 
"rgb(57, 85, 113)"
151
: 
"rgb(57, 69, 113)"
152
: 
"rgb(81, 81, 113)"
153
: 
"rgb(89, 81, 113)"
154
: 
"rgb(97, 81, 113)"
155
: 
"rgb(105, 81, 113)"
156
: 
"rgb(113, 81, 113)"
157
: 
"rgb(113, 81, 105)"
158
: 
"rgb(113, 81, 97)"
159
: 
"rgb(113, 81, 89)"
160
: 
"rgb(113, 81, 81)"
161
: 
"rgb(113, 89, 81)"
162
: 
"rgb(113, 97, 81)"
163
: 
"rgb(113, 105, 81)"
164
: 
"rgb(113, 113, 81)"
165
: 
"rgb(105, 113, 81)"
166
: 
"rgb(97, 113, 81)"
167
: 
"rgb(89, 113, 81)"
168
: 
"rgb(81, 113, 81)"
169
: 
"rgb(81, 113, 89)"
170
: 
"rgb(81, 113, 97)"
171
: 
"rgb(81, 113, 105)"
172
: 
"rgb(81, 113, 113)"
173
: 
"rgb(81, 105, 113)"
174
: 
"rgb(81, 97, 113)"
175
: 
"rgb(81, 89, 113)"
176
: 
"rgb(0, 0, 65)"
177
: 
"rgb(16, 0, 65)"
178
: 
"rgb(32, 0, 65)"
179
: 
"rgb(49, 0, 65)"
180
: 
"rgb(65, 0, 65)"
181
: 
"rgb(65, 0, 49)"
182
: 
"rgb(65, 0, 32)"
183
: 
"rgb(65, 0, 16)"
184
: 
"rgb(65, 0, 0)"
185
: 
"rgb(65, 16, 0)"
186
: 
"rgb(65, 32, 0)"
187
: 
"rgb(65, 49, 0)"
188
: 
"rgb(65, 65, 0)"
189
: 
"rgb(49, 65, 0)"
190
: 
"rgb(32, 65, 0)"
191
: 
"rgb(16, 65, 0)"
192
: 
"rgb(0, 65, 0)"
193
: 
"rgb(0, 65, 16)"
194
: 
"rgb(0, 65, 32)"
195
: 
"rgb(0, 65, 49)"
196
: 
"rgb(0, 65, 65)"
197
: 
"rgb(0, 49, 65)"
198
: 
"rgb(0, 32, 65)"
199
: 
"rgb(0, 16, 65)"
[200 … 255]
200
: 
"rgb(32, 32, 65)"
201
: 
"rgb(40, 32, 65)"
202
: 
"rgb(49, 32, 65)"
203
: 
"rgb(57, 32, 65)"
204
: 
"rgb(65, 32, 65)"
205
: 
"rgb(65, 32, 57)"
206
: 
"rgb(65, 32, 49)"
207
: 
"rgb(65, 32, 40)"
208
: 
"rgb(65, 32, 32)"
209
: 
"rgb(65, 40, 32)"
210
: 
"rgb(65, 49, 32)"
211
: 
"rgb(65, 57, 32)"
212
: 
"rgb(65, 65, 32)"
213
: 
"rgb(57, 65, 32)"
214
: 
"rgb(49, 65, 32)"
215
: 
"rgb(40, 65, 32)"
216
: 
"rgb(32, 65, 32)"
217
: 
"rgb(32, 65, 40)"
218
: 
"rgb(32, 65, 49)"
219
: 
"rgb(32, 65, 57)"
220
: 
"rgb(32, 65, 65)"
221
: 
"rgb(32, 57, 65)"
222
: 
"rgb(32, 49, 65)"
223
: 
"rgb(32, 40, 65)"
224
: 
"rgb(45, 45, 65)"
225
: 
"rgb(49, 45, 65)"
226
: 
"rgb(53, 45, 65)"
227
: 
"rgb(61, 45, 65)"
228
: 
"rgb(65, 45, 65)"
229
: 
"rgb(65, 45, 61)"
230
: 
"rgb(65, 45, 53)"
231
: 
"rgb(65, 45, 49)"
232
: 
"rgb(65, 45, 45)"
233
: 
"rgb(65, 49, 45)"
234
: 
"rgb(65, 53, 45)"
235
: 
"rgb(65, 61, 45)"
236
: 
"rgb(65, 65, 45)"
237
: 
"rgb(61, 65, 45)"
238
: 
"rgb(53, 65, 45)"
239
: 
"rgb(49, 65, 45)"
240
: 
"rgb(45, 65, 45)"
241
: 
"rgb(45, 65, 49)"
242
: 
"rgb(45, 65, 53)"
243
: 
"rgb(45, 65, 61)"
244
: 
"rgb(45, 65, 65)"
245
: 
"rgb(45, 61, 65)"
246
: 
"rgb(45, 53, 65)"
247
: 
"rgb(45, 49, 65)"
248
: 
"rgb(0, 0, 0)"
249
: 
"rgb(0, 0, 0)"
250
: 
"rgb(0, 0, 0)"
251
: 
"rgb(0, 0, 0)"
252
: 
"rgb(0, 0, 0)"
253
: 
"rgb(0, 0, 0)"
254
: 
"rgb(0, 0, 0)"
255
: 
"rgb(0, 0, 0)"


'''

    
