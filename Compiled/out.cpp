
#define SAFE true
#include <iostream>
#include <vector>
#include <cstddef>
#include <cmath>
#include "../CppFiles/CplCppList.hpp"
#include "../CppFiles/CplPtr.hpp"
#include "../CppFiles/CPLGraphics.hpp"

using std::vector;

#define i32 int
#define i16 short
#define i8 signed char
#define f32 float
#define UNKNOWN int
#define byte unsigned char
//#define ui8 byte
#define ui8 i32
#define type char

//#define or ||
//#define and &&

#define arctan std::atan

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
CPLPtr<ui8> shalloc(i32 size){
    CPLPtr<ui8> o;
    o.ptr = (char*)new ui8 [size];
    return o;
}
using std::cos;
using std::sin;
using std::tan;
using std::sqrt;

void cplMain(void)
{
	i32 SCREENX;
	i32 EXPTEMPVAR0;
	CPLPtr<i32> EXPTEMPVAR1;
	EXPTEMPVAR0 = SCREENX;
	EXPTEMPVAR1 = &(SCREENX);
	i32 EXPTEMPVAR2;
	EXPTEMPVAR2 = 600;
	SCREENX = 600;
	i32 SCREENY;
	i32 EXPTEMPVAR3;
	CPLPtr<i32> EXPTEMPVAR4;
	EXPTEMPVAR3 = SCREENY;
	EXPTEMPVAR4 = &(SCREENY);
	i32 EXPTEMPVAR5;
	EXPTEMPVAR5 = 600;
	SCREENY = 600;
	i32 PLAYERSIZEX;
	i32 EXPTEMPVAR6;
	CPLPtr<i32> EXPTEMPVAR7;
	EXPTEMPVAR6 = PLAYERSIZEX;
	EXPTEMPVAR7 = &(PLAYERSIZEX);
	i32 EXPTEMPVAR8;
	EXPTEMPVAR8 = 20;
	PLAYERSIZEX = 20;
	i32 PLAYERSIZEY;
	i32 EXPTEMPVAR9;
	CPLPtr<i32> EXPTEMPVAR10;
	EXPTEMPVAR9 = PLAYERSIZEY;
	EXPTEMPVAR10 = &(PLAYERSIZEY);
	i32 EXPTEMPVAR11;
	EXPTEMPVAR11 = 20;
	PLAYERSIZEY = 20;
	i32 EXPVAR0;
	EXPVAR0 = SCREENX;
	i32 EXPVAR1;
	EXPVAR1 = SCREENY;
	 EXPVAR2;
	EXPVAR2 = graphicsinit(EXPVAR0, EXPVAR1);
	i32 playerPosX;
	i32 EXPTEMPVAR12;
	CPLPtr<i32> EXPTEMPVAR13;
	EXPTEMPVAR12 = playerPosX;
	EXPTEMPVAR13 = &(playerPosX);
	i32 EXPTEMPVAR14;
	EXPTEMPVAR14 = SCREENX / 2;
	playerPosX = EXPTEMPVAR14;
	i32 playerPosY;
	i32 EXPTEMPVAR15;
	CPLPtr<i32> EXPTEMPVAR16;
	EXPTEMPVAR15 = playerPosY;
	EXPTEMPVAR16 = &(playerPosY);
	i32 EXPTEMPVAR17;
	i32 EXPVAR3;
	i32 EXPVAR4;
	i32 EXPVAR5;
	i32 EXPVAR6;
	EXPVAR6 = SCREENY + 0;
	EXPVAR5 = EXPVAR6 + 0;
	EXPVAR4 = EXPVAR5 - PLAYERSIZEY;
	EXPVAR3 = EXPVAR4 + 0;
	EXPTEMPVAR17 = EXPVAR3 - 5;
	playerPosY = EXPTEMPVAR17;
	i32 playerSpeed;
	i32 EXPTEMPVAR18;
	CPLPtr<i32> EXPTEMPVAR19;
	EXPTEMPVAR18 = playerSpeed;
	EXPTEMPVAR19 = &(playerSpeed);
	i32 EXPTEMPVAR20;
	EXPTEMPVAR20 = 30;
	playerSpeed = 30;
	CPLPtr<ui8> screenBuffer;
	CPLPtr<ui8> EXPTEMPVAR21;
	CPLPtr<CPLPtr<ui8>> EXPTEMPVAR22;
	EXPTEMPVAR21 = screenBuffer;
	EXPTEMPVAR22 = &(screenBuffer);
	CPLPtr<i32> EXPTEMPVAR23;
	i32 EXPVAR7;
	i32 EXPVAR8;
	EXPVAR8 = SCREENX * SCREENY;
	EXPVAR7 = EXPVAR8 * 3;
	CPLPtr<i32> EXPVAR9;
	EXPVAR9 = shalloc(EXPVAR7);
	EXPTEMPVAR23 = EXPVAR9;
	screenBuffer = EXPTEMPVAR23;
	i32 enemySpeed;
	i32 EXPTEMPVAR24;
	CPLPtr<i32> EXPTEMPVAR25;
	EXPTEMPVAR24 = enemySpeed;
	EXPTEMPVAR25 = &(enemySpeed);
	i32 EXPTEMPVAR26;
	EXPTEMPVAR26 = 20;
	enemySpeed = 20;
	i32 enemyCount;
	i32 EXPTEMPVAR27;
	CPLPtr<i32> EXPTEMPVAR28;
	EXPTEMPVAR27 = enemyCount;
	EXPTEMPVAR28 = &(enemyCount);
	i32 EXPTEMPVAR29;
	EXPTEMPVAR29 = 10;
	enemyCount = 10;
	i32 EXPTEMPVAR30;
	EXPTEMPVAR30 = enemyCount;
	vector<i32> enemyXList;
	enemyXList.resize(EXPTEMPVAR30);
	i32 EXPTEMPVAR31;
	EXPTEMPVAR31 = enemyCount;
	vector<i32> enemyYList;
	enemyYList.resize(EXPTEMPVAR31);
	i32 enemySizeX;
	i32 EXPTEMPVAR32;
	CPLPtr<i32> EXPTEMPVAR33;
	EXPTEMPVAR32 = enemySizeX;
	EXPTEMPVAR33 = &(enemySizeX);
	i32 EXPTEMPVAR34;
	EXPTEMPVAR34 = 20;
	enemySizeX = 20;
	i32 enemySizeY;
	i32 EXPTEMPVAR35;
	CPLPtr<i32> EXPTEMPVAR36;
	EXPTEMPVAR35 = enemySizeY;
	EXPTEMPVAR36 = &(enemySizeY);
	i32 EXPTEMPVAR37;
	EXPTEMPVAR37 = 20;
	enemySizeY = 20;
	auto initEnemies = [&](void)
	{
		i32 counter;
		i32 EXPTEMPVAR38;
		CPLPtr<i32> EXPTEMPVAR39;
		EXPTEMPVAR38 = counter;
		EXPTEMPVAR39 = &(counter);
		i32 EXPTEMPVAR40;
		EXPTEMPVAR40 = 0;
		counter = 0;
		while(1)
		{
			ui8 EXPVAR10;
			EXPVAR10 = counter < enemyCount;
			EXPVAR10 = !EXPVAR10;
			if(EXPVAR10)
			{
				break;
			}
			i32 EXPTEMPVAR41;
			EXPTEMPVAR41 = counter;
			UNKNOWN EXPTEMPVAR42;
			i32 EXPTEMPVAR43;
			i32 EXPVAR11;
			EXPVAR11 = counter;
			UNKNOWN EXPVAR12;
			EXPVAR12 = enemyXList[EXPVAR11];
			EXPTEMPVAR42 = EXPVAR12;
			i32 IROPT0;
			type IROPT3;
			UNKNOWN IROPT2;
			IROPT3 = declindtype(enemyXList);
			IROPT2 = sizeof(IROPT3);
			IROPT0 = EXPVAR11 * IROPT2;
			CPLPtr<vector<i32>> IROPT1;
			IROPT1 = &(enemyXList);
			EXPTEMPVAR43 = IROPT0 + &enemyXList;
			i32 EXPTEMPVAR44;
			i32 EXPVAR13;
			EXPVAR13 = counter * 30;
			EXPTEMPVAR44 = EXPVAR13 + 10;
			*(EXPTEMPVAR43) = EXPTEMPVAR44;
			i32 EXPTEMPVAR45;
			EXPTEMPVAR45 = counter;
			UNKNOWN EXPTEMPVAR46;
			i32 EXPTEMPVAR47;
			i32 EXPVAR14;
			EXPVAR14 = counter;
			UNKNOWN EXPVAR15;
			EXPVAR15 = enemyYList[EXPVAR14];
			EXPTEMPVAR46 = EXPVAR15;
			i32 IROPT4;
			type IROPT7;
			UNKNOWN IROPT6;
			IROPT7 = declindtype(enemyYList);
			IROPT6 = sizeof(IROPT7);
			IROPT4 = EXPVAR14 * IROPT6;
			CPLPtr<vector<i32>> IROPT5;
			IROPT5 = &(enemyYList);
			EXPTEMPVAR47 = IROPT4 + &enemyYList;
			i32 EXPTEMPVAR48;
			EXPTEMPVAR48 = counter * 10;
			*(EXPTEMPVAR47) = EXPTEMPVAR48;
			i32 EXPTEMPVAR49;
			CPLPtr<i32> EXPTEMPVAR50;
			EXPTEMPVAR49 = counter;
			EXPTEMPVAR50 = &(counter);
			i32 EXPTEMPVAR51;
			EXPTEMPVAR51 = counter + 1;
			counter = EXPTEMPVAR51;
		}
	};
	auto drawScreenBuffer = [&](void)
	{
		i32 x;
		i32 EXPTEMPVAR52;
		CPLPtr<i32> EXPTEMPVAR53;
		EXPTEMPVAR52 = x;
		EXPTEMPVAR53 = &(x);
		i32 EXPTEMPVAR54;
		EXPTEMPVAR54 = 0;
		x = 0;
		i32 counter;
		i32 EXPTEMPVAR55;
		CPLPtr<i32> EXPTEMPVAR56;
		EXPTEMPVAR55 = counter;
		EXPTEMPVAR56 = &(counter);
		i32 EXPTEMPVAR57;
		EXPTEMPVAR57 = 0;
		counter = 0;
		while(1)
		{
			ui8 EXPVAR16;
			EXPVAR16 = x < SCREENX;
			EXPVAR16 = !EXPVAR16;
			if(EXPVAR16)
			{
				break;
			}
			i32 y;
			i32 EXPTEMPVAR58;
			CPLPtr<i32> EXPTEMPVAR59;
			EXPTEMPVAR58 = y;
			EXPTEMPVAR59 = &(y);
			i32 EXPTEMPVAR60;
			EXPTEMPVAR60 = 0;
			y = 0;
			while(1)
			{
				ui8 EXPVAR17;
				EXPVAR17 = y < SCREENY;
				EXPVAR17 = !EXPVAR17;
				if(EXPVAR17)
				{
					break;
				}
				i32 EXPVAR18;
				EXPVAR18 = x;
				i32 EXPVAR19;
				EXPVAR19 = y;
				CPLPtr<ui8> EXPVAR20;
				CPLPtr<ui8> EXPVAR21;
				EXPVAR21 = screenBuffer + counter;
				EXPVAR20 = *(EXPVAR21);
				CPLPtr<ui8> EXPVAR22;
				CPLPtr<ui8> EXPVAR23;
				CPLPtr<ui8> EXPVAR24;
				EXPVAR24 = screenBuffer + counter;
				EXPVAR23 = EXPVAR24 + 1;
				EXPVAR22 = *(EXPVAR23);
				CPLPtr<ui8> EXPVAR25;
				CPLPtr<ui8> EXPVAR26;
				CPLPtr<ui8> EXPVAR27;
				EXPVAR27 = screenBuffer + counter;
				EXPVAR26 = EXPVAR27 + 2;
				EXPVAR25 = *(EXPVAR26);
				 EXPVAR28;
				EXPVAR28 = drawpixel(EXPVAR18, EXPVAR19, EXPVAR20, EXPVAR22, EXPVAR25);
				i32 EXPTEMPVAR61;
				CPLPtr<i32> EXPTEMPVAR62;
				EXPTEMPVAR61 = counter;
				EXPTEMPVAR62 = &(counter);
				i32 EXPTEMPVAR63;
				EXPTEMPVAR63 = counter + 3;
				counter = EXPTEMPVAR63;
				i32 EXPTEMPVAR64;
				CPLPtr<i32> EXPTEMPVAR65;
				EXPTEMPVAR64 = y;
				EXPTEMPVAR65 = &(y);
				i32 EXPTEMPVAR66;
				EXPTEMPVAR66 = y + 1;
				y = EXPTEMPVAR66;
			}
			i32 EXPTEMPVAR67;
			CPLPtr<i32> EXPTEMPVAR68;
			EXPTEMPVAR67 = x;
			EXPTEMPVAR68 = &(x);
			i32 EXPTEMPVAR69;
			EXPTEMPVAR69 = x + 1;
			x = EXPTEMPVAR69;
		}
	};
	auto drawRect = [&](i32 xPos, i32 yPos, i32 sx, i32 sy)
	{
		i32 x;
		i32 EXPTEMPVAR70;
		CPLPtr<i32> EXPTEMPVAR71;
		EXPTEMPVAR70 = x;
		EXPTEMPVAR71 = &(x);
		i32 EXPTEMPVAR72;
		EXPTEMPVAR72 = 0;
		x = 0;
		while(1)
		{
			ui8 EXPVAR29;
			EXPVAR29 = x < sx;
			EXPVAR29 = !EXPVAR29;
			if(EXPVAR29)
			{
				break;
			}
			i32 y;
			i32 EXPTEMPVAR73;
			CPLPtr<i32> EXPTEMPVAR74;
			EXPTEMPVAR73 = y;
			EXPTEMPVAR74 = &(y);
			i32 EXPTEMPVAR75;
			EXPTEMPVAR75 = 0;
			y = 0;
			while(1)
			{
				ui8 EXPVAR30;
				EXPVAR30 = y < sy;
				EXPVAR30 = !EXPVAR30;
				if(EXPVAR30)
				{
					break;
				}
				i32 screenPos;
				i32 EXPTEMPVAR76;
				CPLPtr<i32> EXPTEMPVAR77;
				EXPTEMPVAR76 = screenPos;
				EXPTEMPVAR77 = &(screenPos);
				i32 EXPTEMPVAR78;
				i32 EXPVAR31;
				i32 EXPVAR32;
				i32 EXPVAR33;
				EXPVAR33 = xPos + x;
				EXPVAR32 = EXPVAR33 * SCREENX;
				i32 EXPVAR34;
				EXPVAR34 = yPos + y;
				EXPVAR31 = EXPVAR32 + EXPVAR34;
				EXPTEMPVAR78 = EXPVAR31 * 3;
				screenPos = EXPTEMPVAR78;
				ui8 EXPVAR35;
				ui8 EXPVAR36;
				i32 EXPVAR37;
				i32 EXPVAR38;
				i32 EXPVAR39;
				i32 EXPVAR40;
				i32 EXPVAR41;
				EXPVAR41 = SCREENX * SCREENY;
				EXPVAR40 = EXPVAR41 * 3;
				EXPVAR39 = EXPVAR40 + 0;
				EXPVAR38 = EXPVAR39 + 0;
				EXPVAR37 = EXPVAR38 - 3;
				EXPVAR36 = screenPos < EXPVAR37;
				ui8 EXPVAR42;
				EXPVAR42 = screenPos < 0;
				EXPVAR35 = EXPVAR36 or EXPVAR42;
				if(EXPVAR35)
				{
					CPLPtr<ui8> EXPTEMPVAR79;
					CPLPtr<ui8> EXPTEMPVAR80;
					CPLPtr<ui8> EXPVAR43;
					EXPVAR43 = screenBuffer + screenPos;
					EXPTEMPVAR79 = *(EXPVAR43);
					EXPTEMPVAR80 = EXPVAR43;
					i32 EXPTEMPVAR81;
					EXPTEMPVAR81 = 255;
					*(EXPTEMPVAR80) = EXPTEMPVAR81;
					CPLPtr<ui8> EXPTEMPVAR82;
					CPLPtr<ui8> EXPTEMPVAR83;
					CPLPtr<ui8> EXPVAR44;
					CPLPtr<ui8> EXPVAR45;
					EXPVAR45 = screenBuffer + screenPos;
					EXPVAR44 = EXPVAR45 + 1;
					EXPTEMPVAR82 = *(EXPVAR44);
					EXPTEMPVAR83 = EXPVAR44;
					i32 EXPTEMPVAR84;
					EXPTEMPVAR84 = 0;
					*(EXPTEMPVAR83) = EXPTEMPVAR84;
					CPLPtr<ui8> EXPTEMPVAR85;
					CPLPtr<ui8> EXPTEMPVAR86;
					CPLPtr<ui8> EXPVAR46;
					CPLPtr<ui8> EXPVAR47;
					EXPVAR47 = screenBuffer + screenPos;
					EXPVAR46 = EXPVAR47 + 2;
					EXPTEMPVAR85 = *(EXPVAR46);
					EXPTEMPVAR86 = EXPVAR46;
					i32 EXPTEMPVAR87;
					EXPTEMPVAR87 = 30;
					*(EXPTEMPVAR86) = EXPTEMPVAR87;
				}
				i32 EXPTEMPVAR88;
				CPLPtr<i32> EXPTEMPVAR89;
				EXPTEMPVAR88 = y;
				EXPTEMPVAR89 = &(y);
				i32 EXPTEMPVAR90;
				EXPTEMPVAR90 = y + 1;
				y = EXPTEMPVAR90;
			}
			i32 EXPTEMPVAR91;
			CPLPtr<i32> EXPTEMPVAR92;
			EXPTEMPVAR91 = x;
			EXPTEMPVAR92 = &(x);
			i32 EXPTEMPVAR93;
			EXPTEMPVAR93 = x + 1;
			x = EXPTEMPVAR93;
		}
	};
	auto drawPlayer = [&](void)
	{
		i32 EXPVAR48;
		EXPVAR48 = playerPosX;
		i32 EXPVAR49;
		EXPVAR49 = playerPosY;
		i32 EXPVAR50;
		EXPVAR50 = PLAYERSIZEY;
		i32 EXPVAR51;
		EXPVAR51 = PLAYERSIZEX;
		EXPVAR52 = drawRect(EXPVAR48, EXPVAR49, EXPVAR50, EXPVAR51);
	};
	auto drawEnemies = [&](void)
	{
		i32 counter;
		i32 EXPTEMPVAR94;
		CPLPtr<i32> EXPTEMPVAR95;
		EXPTEMPVAR94 = counter;
		EXPTEMPVAR95 = &(counter);
		i32 EXPTEMPVAR96;
		EXPTEMPVAR96 = 0;
		counter = 0;
		while(1)
		{
			ui8 EXPVAR53;
			EXPVAR53 = counter < enemyCount;
			EXPVAR53 = !EXPVAR53;
			if(EXPVAR53)
			{
				break;
			}
			UNKNOWN EXPVAR54;
			i32 EXPVAR55;
			EXPVAR55 = counter;
			UNKNOWN EXPVAR56;
			EXPVAR56 = enemyXList[EXPVAR55];
			EXPVAR54 = EXPVAR56;
			UNKNOWN EXPVAR57;
			i32 EXPVAR58;
			EXPVAR58 = counter;
			UNKNOWN EXPVAR59;
			EXPVAR59 = enemyYList[EXPVAR58];
			EXPVAR57 = EXPVAR59;
			i32 EXPVAR60;
			EXPVAR60 = enemySizeX;
			i32 EXPVAR61;
			EXPVAR61 = enemySizeY;
			EXPVAR62 = drawRect(EXPVAR54, EXPVAR57, EXPVAR60, EXPVAR61);
			i32 EXPTEMPVAR97;
			CPLPtr<i32> EXPTEMPVAR98;
			EXPTEMPVAR97 = counter;
			EXPTEMPVAR98 = &(counter);
			i32 EXPTEMPVAR99;
			EXPTEMPVAR99 = counter + 1;
			counter = EXPTEMPVAR99;
		}
	};
	auto clearScreen = [&](void)
	{
		i32 counter;
		i32 EXPTEMPVAR100;
		CPLPtr<i32> EXPTEMPVAR101;
		EXPTEMPVAR100 = counter;
		EXPTEMPVAR101 = &(counter);
		i32 EXPTEMPVAR102;
		EXPTEMPVAR102 = 0;
		counter = 0;
		while(1)
		{
			ui8 EXPVAR63;
			i32 EXPVAR64;
			i32 EXPVAR65;
			EXPVAR65 = SCREENX * SCREENY;
			EXPVAR64 = EXPVAR65 * 3;
			EXPVAR63 = counter < EXPVAR64;
			EXPVAR63 = !EXPVAR63;
			if(EXPVAR63)
			{
				break;
			}
			CPLPtr<ui8> EXPTEMPVAR103;
			CPLPtr<ui8> EXPTEMPVAR104;
			CPLPtr<ui8> EXPVAR66;
			EXPVAR66 = screenBuffer + counter;
			EXPTEMPVAR103 = *(EXPVAR66);
			EXPTEMPVAR104 = EXPVAR66;
			i32 EXPTEMPVAR105;
			EXPTEMPVAR105 = 0;
			*(EXPTEMPVAR104) = EXPTEMPVAR105;
			i32 EXPTEMPVAR106;
			CPLPtr<i32> EXPTEMPVAR107;
			EXPTEMPVAR106 = counter;
			EXPTEMPVAR107 = &(counter);
			i32 EXPTEMPVAR108;
			EXPTEMPVAR108 = counter + 1;
			counter = EXPTEMPVAR108;
		}
	};
	auto updateEnemies = [&](void)
	{
		i32 counter;
		i32 EXPTEMPVAR109;
		CPLPtr<i32> EXPTEMPVAR110;
		EXPTEMPVAR109 = counter;
		EXPTEMPVAR110 = &(counter);
		i32 EXPTEMPVAR111;
		EXPTEMPVAR111 = 0;
		counter = 0;
		while(1)
		{
			ui8 EXPVAR67;
			EXPVAR67 = counter < enemyCount;
			EXPVAR67 = !EXPVAR67;
			if(EXPVAR67)
			{
				break;
			}
			i32 EXPTEMPVAR112;
			EXPTEMPVAR112 = counter;
			UNKNOWN EXPTEMPVAR113;
			i32 EXPTEMPVAR114;
			i32 EXPVAR68;
			EXPVAR68 = counter;
			UNKNOWN EXPVAR69;
			EXPVAR69 = enemyYList[EXPVAR68];
			EXPTEMPVAR113 = EXPVAR69;
			i32 IROPT16;
			type IROPT19;
			UNKNOWN IROPT18;
			IROPT19 = declindtype(enemyYList);
			IROPT18 = sizeof(IROPT19);
			IROPT16 = EXPVAR68 * IROPT18;
			CPLPtr<vector<i32>> IROPT17;
			IROPT17 = &(enemyYList);
			EXPTEMPVAR114 = IROPT16 + &enemyYList;
			UNKNOWN EXPTEMPVAR115;
			i32 EXPVAR70;
			EXPVAR70 = counter;
			UNKNOWN EXPVAR71;
			EXPVAR71 = enemyYList[EXPVAR70];
			EXPTEMPVAR115 = EXPVAR71 + enemySpeed;
			*(EXPTEMPVAR114) = EXPTEMPVAR115;
			ui8 EXPVAR72;
			i32 EXPVAR73;
			EXPVAR73 = counter;
			UNKNOWN EXPVAR74;
			EXPVAR74 = enemyYList[EXPVAR73];
			EXPVAR72 = EXPVAR74 > 600;
			if(EXPVAR72)
			{
				i32 EXPTEMPVAR116;
				EXPTEMPVAR116 = counter;
				UNKNOWN EXPTEMPVAR117;
				i32 EXPTEMPVAR118;
				i32 EXPVAR75;
				EXPVAR75 = counter;
				UNKNOWN EXPVAR76;
				EXPVAR76 = enemyYList[EXPVAR75];
				EXPTEMPVAR117 = EXPVAR76;
				i32 IROPT28;
				type IROPT31;
				UNKNOWN IROPT30;
				IROPT31 = declindtype(enemyYList);
				IROPT30 = sizeof(IROPT31);
				IROPT28 = EXPVAR75 * IROPT30;
				CPLPtr<vector<i32>> IROPT29;
				IROPT29 = &(enemyYList);
				EXPTEMPVAR118 = IROPT28 + &enemyYList;
				i32 EXPTEMPVAR119;
				EXPTEMPVAR119 = 0;
				*(EXPTEMPVAR118) = EXPTEMPVAR119;
			}
			i32 EXPTEMPVAR120;
			CPLPtr<i32> EXPTEMPVAR121;
			EXPTEMPVAR120 = counter;
			EXPTEMPVAR121 = &(counter);
			i32 EXPTEMPVAR122;
			EXPTEMPVAR122 = counter + 1;
			counter = EXPTEMPVAR122;
		}
	};
	auto updatePlayer = [&](void)
	{
		ui8 EXPVAR77;
		i32 EXPVAR78;
		EXPVAR78 = 97;
		i32 EXPVAR79;
		EXPVAR79 = getkeypress(97);
		ui8 EXPVAR80;
		EXPVAR80 = EXPVAR79 == 1;
		EXPVAR77 = EXPVAR80;
		if(EXPVAR77)
		{
			i32 EXPTEMPVAR123;
			CPLPtr<i32> EXPTEMPVAR124;
			EXPTEMPVAR123 = playerPosX;
			EXPTEMPVAR124 = &(playerPosX);
			i32 EXPTEMPVAR125;
			i32 EXPVAR81;
			EXPVAR81 = playerPosX + 0;
			EXPTEMPVAR125 = EXPVAR81 - playerSpeed;
			playerPosX = EXPTEMPVAR125;
		}
		ui8 EXPVAR82;
		i32 EXPVAR83;
		EXPVAR83 = 100;
		i32 EXPVAR84;
		EXPVAR84 = getkeypress(100);
		ui8 EXPVAR85;
		EXPVAR85 = EXPVAR84 == 1;
		EXPVAR82 = EXPVAR85;
		if(EXPVAR82)
		{
			i32 EXPTEMPVAR126;
			CPLPtr<i32> EXPTEMPVAR127;
			EXPTEMPVAR126 = playerPosX;
			EXPTEMPVAR127 = &(playerPosX);
			i32 EXPTEMPVAR128;
			EXPTEMPVAR128 = playerPosX + playerSpeed;
			playerPosX = EXPTEMPVAR128;
		}
	};
	auto println = [&](void)
	{
		i32 EXPVAR86;
		EXPVAR86 = 10;
		 EXPVAR87;
		EXPVAR87 = printc(10);
		i32 EXPVAR88;
		EXPVAR88 = 13;
		 EXPVAR89;
		EXPVAR89 = printc(13);
	};
	while(1)
	{
		i32 EXPVAR90;
		EXPVAR90 = 1;
		EXPVAR90 = !1;
		if(EXPVAR90)
		{
			break;
		}
	}
	EXPVAR91 = initEnemies();
	while(1)
	{
		i32 EXPVAR92;
		EXPVAR92 = 1;
		EXPVAR92 = !1;
		if(EXPVAR92)
		{
			break;
		}
		 EXPVAR93;
		EXPVAR93 = graphicspump();
		EXPVAR94 = updatePlayer();
		EXPVAR95 = updateEnemies();
		EXPVAR96 = drawPlayer();
		EXPVAR97 = drawEnemies();
		EXPVAR98 = drawScreenBuffer();
		i32 EXPVAR99;
		EXPVAR99 = 50;
		 EXPVAR100;
		EXPVAR100 = graphicssleep(50);
		EXPVAR101 = clearScreen();
	}
	while(1)
	{
		i32 EXPVAR102;
		EXPVAR102 = 1;
		EXPVAR102 = !1;
		if(EXPVAR102)
		{
			break;
		}
	}
}


int main(){
    cplMain();
    return 0;
}

