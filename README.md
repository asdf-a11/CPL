# CPL
*CPL (chapman programming language)* 
CPL is a programming language designed to improve upon certain aspects of C++ these being:
- Conditionals handerling types of varaibles / templates.
- Provides a simpler IR (Intermediate reprisentation) that makes it easier to embed into other applications.
- In built vector maths through supporting arithmetic operations on arrays.
- More aggressive optimisations through bending the symantics of the program, e.g replaceing small mallocs with alloca where possible.
- Slightly improved syntax
- Returning multiple values from a function

### Example CPL Syntax
This code shows how to print a intiger number in CPL.
```
fn void println(){
	printc(10); #Prints new line character#
	printc(13); #Prints carrage return character to send curser back to start of new line#
}
fn void printn(i32 number){	
	i32 bufferSize = 11;
	i32[bufferSize] buffer = 0;
	i32 pointer = 10;
	i32 runOnceFlag = 1;
	while number != 0 or runOnceFlag == 1{
		i32 digit = number % 10;
		number = number / 10;
		buffer[pointer] = digit + 48;		
		pointer = pointer - 1;
		runOnceFlag = 0;
	}
	pointer = pointer + 1;
	while pointer < bufferSize{
		printc(buffer[pointer]);
		pointer = pointer + 1;
	}
}
# Print the number 356 followed by a new line#
printn(356);
println();
```
There is a example file in InputCode/RayCaster.cpl this is an example of a more complex project in cpl.

### Featurs of CPL so far
- Support for floats through f32 data type
- Arrays
- Pointers
- Structs ```struct testing{i32 var;}```
- Variable length stack arrays ```i32[x] arr;```

### Stages of compilation
1. Pre processing, cpl uses ? to denote pre-process instruction
2. Lexing, main token types are CONST, NAME, KEYWORD
3. Parsing, the code is converted to intermediate reprisentation
4. Generation of the controll flow graph (not fully implimented yet)
5. Const propergation / Type propergation
6. Breaking down operations, e.g array operations are replaced with loops that iterate of each element
7. Conversion to either assembly or C++

### Running
Use python version 3.10 or higher.
Write you program in InputCode/code.cpl then run Main_.py file to compiler.

### Current limitations
Currently the code can transpile and run in C++ fine, but when compiling to assembly it may not work because const propergation is not fully implimented yet meaning varaible types cannot be propergated through the code. This is something that will be fixed soon. 

