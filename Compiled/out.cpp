
#define SAFE true
#include <iostream>
#include <vector>
#include <cstddef>
#include "../CppFiles/CplCppList.hpp"
#include "../CppFiles/CplPtr.hpp"
#include "../CppFiles/CPLGraphics.hpp"

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
	UNKNOWN EXPFUNCTIONRETURN10;
	graphicsinit();
	while(1)
	{
		i32 EXPVAR0;
		EXPVAR0 = 1;
		EXPVAR0 = !EXPVAR0;
		if(EXPVAR0)
		{
			break;
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
			UNKNOWN EXPVAR1;
			EXPVAR1 = counter1 < 10;
			EXPVAR1 = !EXPVAR1;
			if(EXPVAR1)
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
				UNKNOWN EXPVAR2;
				EXPVAR2 = counter2 < 10;
				EXPVAR2 = !EXPVAR2;
				if(EXPVAR2)
				{
					break;
				};
				i32 EXPFUNCTIONARGUMENT11;
				EXPFUNCTIONARGUMENT11 = counter1;
				i32 EXPFUNCTIONARGUMENT12;
				EXPFUNCTIONARGUMENT12 = counter2;
				i32 EXPFUNCTIONARGUMENT13;
				EXPFUNCTIONARGUMENT13 = 255;
				i32 EXPFUNCTIONARGUMENT14;
				EXPFUNCTIONARGUMENT14 = 0;
				i32 EXPFUNCTIONARGUMENT15;
				EXPFUNCTIONARGUMENT15 = 0;
				UNKNOWN EXPFUNCTIONRETURN16;
				drawpixel(EXPFUNCTIONARGUMENT11, EXPFUNCTIONARGUMENT12, EXPFUNCTIONARGUMENT13, EXPFUNCTIONARGUMENT14, EXPFUNCTIONARGUMENT15);
				i32 EXPTEMPVAR6;
				CPLPtr<i32> EXPTEMPVAR7;
				EXPTEMPVAR6 = counter2;
				EXPTEMPVAR7 = &(counter2);
				i32 EXPTEMPVAR8;
				EXPTEMPVAR8 = counter2 + 1;
				*(EXPTEMPVAR7) = EXPTEMPVAR8;
			};
			i32 EXPTEMPVAR9;
			CPLPtr<i32> EXPTEMPVAR10;
			EXPTEMPVAR9 = counter1;
			EXPTEMPVAR10 = &(counter1);
			i32 EXPTEMPVAR11;
			EXPTEMPVAR11 = counter1 + 1;
			*(EXPTEMPVAR10) = EXPTEMPVAR11;
		};
		i32 EXPFUNCTIONARGUMENT17;
		EXPFUNCTIONARGUMENT17 = 10;
		UNKNOWN EXPFUNCTIONRETURN18;
		graphicssleep(EXPFUNCTIONARGUMENT17);
	};
	while(1)
	{
		i32 EXPVAR3;
		EXPVAR3 = 1;
		EXPVAR3 = !EXPVAR3;
		if(EXPVAR3)
		{
			break;
		};
	};
}


int main(){
    cplMain();
    return 0;
}

