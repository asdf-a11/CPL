
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
	i32 counter;
	i32 EXPTEMPVAR0;
	EXPTEMPVAR0 = 1;
	counter = EXPTEMPVAR0;
	i32 sign;
	i32 EXPTEMPVAR1;
	EXPTEMPVAR1 = -1;
	sign = EXPTEMPVAR1;
	f32 pi;
	i32 EXPTEMPVAR2;
	EXPTEMPVAR2 = 4;
	pi = EXPTEMPVAR2;
	while(1)
	{
		UNKNOWN EXPVAR0;
		EXPVAR0 = counter < 100;
		EXPVAR0 = !EXPVAR0;
		if(EXPVAR0)
		{
			break;
		};
		f32 EXPTEMPVAR3;
		f32 EXPVAR1;
		f32 EXPVAR2;
		i32 EXPVAR3;
		i32 EXPVAR4;
		EXPVAR4 = counter * 2;
		EXPVAR3 = 1 + EXPVAR4;
		EXPVAR2 = 4.0 / EXPVAR3;
		EXPVAR1 = EXPVAR2 * sign;
		EXPTEMPVAR3 = pi + EXPVAR1;
		pi = EXPTEMPVAR3;
		i32 EXPTEMPVAR4;
		i32 EXPVAR5;
		EXPVAR5 = -1;
		EXPTEMPVAR4 = sign * EXPVAR5;
		sign = EXPTEMPVAR4;
		i32 EXPTEMPVAR5;
		EXPTEMPVAR5 = counter + 1;
		counter = EXPTEMPVAR5;
	};
	f32 EXPFUNCTIONARGUMENT0;
	EXPFUNCTIONARGUMENT0 = pi;
	UNKNOWN EXPFUNCTIONRETURN1;
	printf(EXPFUNCTIONARGUMENT0);
	i32 EXPFUNCTIONARGUMENT2;
	EXPFUNCTIONARGUMENT2 = 10;
	UNKNOWN EXPFUNCTIONRETURN3;
	printc(EXPFUNCTIONARGUMENT2);
	i32 EXPFUNCTIONARGUMENT4;
	EXPFUNCTIONARGUMENT4 = 13;
	UNKNOWN EXPFUNCTIONRETURN5;
	printc(EXPFUNCTIONARGUMENT4);
}


int main(){
    cplMain();
    return 0;
}

