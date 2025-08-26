# CPL
*CPL (chapman programming language)* 
CPL is a programming language designed to improve upon certain aspects of C++ these being:
- Conditionals handerling types of varaibles / templates.
- Provides a simpler IR (Intermediate reprisentation) that makes it easier to embed into other applications.
- In built vector maths through supporting arithmetic operations on arrays.
- More aggressive optimisations through bending the symantics of the program, e.g replaceing small mallocs with alloca where possible.

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
		printc(digit + 48);
		println();
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
# Print 8 zeros to show off arrays #
i32[8] buffer = 49;
i32 counter = 0;
while counter < 8{
	printc(buffer[counter]);
	counter = counter + 1;
}
```

### Running
Use python version 3.10 and higher.
Write you program in InputCode/code.cpl then run Main_.py file to compiler.

