
#define SAFE
#include <iostream>
#include <vector>
#include "../CppFiles/CplCppList.hpp"

#define i32 int
#define i16 short
#define i8 signed char
#define f32 float
#define UNKNOWN int

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

void cplMain(void);

void cplMain(void)
{
	i32 EXPFUNCTIONARGUMENT0;
	EXPFUNCTIONARGUMENT0 = 48;
	UNKNOWN EXPFUNCTIONRETURN1;
	printc(EXPFUNCTIONARGUMENT0);
}


int main(){
    cplMain();
    return 0;
}

