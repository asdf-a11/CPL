
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

void cplMain(void)
{
	struct vec2{
		i32 x;
		i32 y;
	};
	auto printVec2 = [](vec2 a)
	{
		i32 EXPFUNCTIONARGUMENT0;
		EXPFUNCTIONARGUMENT0 = a.x;
		UNKNOWN EXPFUNCTIONRETURN1;
		printn(EXPFUNCTIONARGUMENT0);
		i32 EXPFUNCTIONARGUMENT2;
		EXPFUNCTIONARGUMENT2 = 95;
		UNKNOWN EXPFUNCTIONRETURN3;
		printc(EXPFUNCTIONARGUMENT2);
		i32 EXPFUNCTIONARGUMENT4;
		EXPFUNCTIONARGUMENT4 = a.y;
		UNKNOWN EXPFUNCTIONRETURN5;
		printn(EXPFUNCTIONARGUMENT4);
		i32 EXPFUNCTIONARGUMENT6;
		EXPFUNCTIONARGUMENT6 = 10;
		UNKNOWN EXPFUNCTIONRETURN7;
		printc(EXPFUNCTIONARGUMENT6);
		i32 EXPFUNCTIONARGUMENT8;
		EXPFUNCTIONARGUMENT8 = 13;
		UNKNOWN EXPFUNCTIONRETURN9;
		printc(EXPFUNCTIONARGUMENT8);
	};
	i32 counter1;
	i32 EXPTEMPVAR0;
	CPLPtr<i32> EXPTEMPVAR1;
	EXPTEMPVAR0 = counter1;
	EXPTEMPVAR1 = &(counter1);
	i32 EXPTEMPVAR2;
	EXPTEMPVAR2 = 0;
	*(EXPTEMPVAR1) = EXPTEMPVAR2;
	while(1)
	{
		UNKNOWN EXPVAR0;
		EXPVAR0 = counter1 < 2;
		EXPVAR0 = !EXPVAR0;
		if(EXPVAR0)
		{
			break;
		};
		i32 counter2;
		i32 EXPTEMPVAR3;
		CPLPtr<i32> EXPTEMPVAR4;
		EXPTEMPVAR3 = counter2;
		EXPTEMPVAR4 = &(counter2);
		i32 EXPTEMPVAR5;
		EXPTEMPVAR5 = 0;
		*(EXPTEMPVAR4) = EXPTEMPVAR5;
		while(1)
		{
			UNKNOWN EXPVAR1;
			EXPVAR1 = counter2 < 2;
			EXPVAR1 = !EXPVAR1;
			if(EXPVAR1)
			{
				break;
			};
			vec2 g;
			i32 EXPTEMPVAR6;
			CPLPtr<i32> EXPTEMPVAR7;
			EXPTEMPVAR6 = g.x;
			CPLPtr<vec2> IROPT0;
			IROPT0 = &(g);
			EXPTEMPVAR7 = IROPT0 + CPLPtr<char>((void*)(offsetof(vec2,x)));
			i32 EXPTEMPVAR8;
			EXPTEMPVAR8 = counter1;
			*(EXPTEMPVAR7) = EXPTEMPVAR8;
			i32 EXPTEMPVAR9;
			CPLPtr<i32> EXPTEMPVAR10;
			EXPTEMPVAR9 = g.y;
			CPLPtr<vec2> IROPT1;
			IROPT1 = &(g);
			EXPTEMPVAR10 = IROPT1 + CPLPtr<char>((void*)(offsetof(vec2,y)));
			i32 EXPTEMPVAR11;
			EXPTEMPVAR11 = counter2;
			*(EXPTEMPVAR10) = EXPTEMPVAR11;
			vec2 EXPFUNCTIONARGUMENT10;
			EXPFUNCTIONARGUMENT10 = g;
			UNKNOWN EXPFUNCTIONRETURN11;
			printVec2(EXPFUNCTIONARGUMENT10);
			i32 EXPTEMPVAR12;
			CPLPtr<i32> EXPTEMPVAR13;
			EXPTEMPVAR12 = counter2;
			EXPTEMPVAR13 = &(counter2);
			i32 EXPTEMPVAR14;
			EXPTEMPVAR14 = counter2 + 1;
			*(EXPTEMPVAR13) = EXPTEMPVAR14;
		};
		i32 EXPTEMPVAR15;
		CPLPtr<i32> EXPTEMPVAR16;
		EXPTEMPVAR15 = counter1;
		EXPTEMPVAR16 = &(counter1);
		i32 EXPTEMPVAR17;
		EXPTEMPVAR17 = counter1 + 1;
		*(EXPTEMPVAR16) = EXPTEMPVAR17;
	};
}


int main(){
    cplMain();
    return 0;
}

