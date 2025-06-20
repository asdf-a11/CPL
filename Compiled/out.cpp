
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

void cplMain(void);

void cplMain(void)
{
	f32 a;
	f32 EXPTEMPVAR0;
	EXPTEMPVAR0 = 0.0;
	a = EXPTEMPVAR0;
	f32 b;
	f32 EXPTEMPVAR1;
	EXPTEMPVAR1 = 1.0;
	b = EXPTEMPVAR1;
	f32 c;
	f32 EXPTEMPVAR2;
	EXPTEMPVAR2 = b + a;
	c = EXPTEMPVAR2;
	f32 EXPFUNCTIONARGUMENT0;
	EXPFUNCTIONARGUMENT0 = c;
	UNKNOWN EXPFUNCTIONRETURN1;
	printf(EXPFUNCTIONARGUMENT0);
}


int main(){
    cplMain();
    return 0;
}

