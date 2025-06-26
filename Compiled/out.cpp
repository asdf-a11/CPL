
#define SAFE
#include <iostream>
#include <vector>
#include <cstddef>
#include "../CppFiles/CplCppList.hpp"
#include "../CppFiles/CplPtr.hpp"

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

void cplMain(void);

void cplMain(void)
{
	struct Test{
		i32 a;
		i32 b;
	};
	Test g;
	i32 EXPTEMPVAR6;
	CPLPtr<i32> EXPTEMPVAR7;
	EXPTEMPVAR6 = g.a;
	CPLPtr<Test> IROPT0;
	IROPT0 = &(g);
	EXPTEMPVAR7 = IROPT0 + CPLPtr<char>((void*)(offsetof(Test,a)));
	i32 EXPTEMPVAR8;
	EXPTEMPVAR8 = 10;
	*(EXPTEMPVAR7) = EXPTEMPVAR8;
	i32 EXPTEMPVAR9;
	CPLPtr<i32> EXPTEMPVAR10;
	EXPTEMPVAR9 = g.b;
	CPLPtr<Test> IROPT1;
	IROPT1 = &(g);
	EXPTEMPVAR10 = IROPT1 + CPLPtr<char>((void*)(offsetof(Test,b)));
	i32 EXPTEMPVAR11;
	EXPTEMPVAR11 = 15;
	*(EXPTEMPVAR10) = EXPTEMPVAR11;
	i32 EXPFUNCTIONARGUMENT0;
	EXPFUNCTIONARGUMENT0 = g.a;
	UNKNOWN EXPFUNCTIONRETURN1;
	printn(EXPFUNCTIONARGUMENT0);
	i32 EXPFUNCTIONARGUMENT2;
	EXPFUNCTIONARGUMENT2 = g.b;
	UNKNOWN EXPFUNCTIONRETURN3;
	printn(EXPFUNCTIONARGUMENT2);
}


int main(){
    cplMain();
    return 0;
}

