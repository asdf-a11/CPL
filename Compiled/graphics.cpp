#define IS_INCLUDE
#ifdef IS_INCLUDE
    #pragma once
#endif
#ifndef SAFE
    #define SAFE true
#endif
#include <string>
#include <iostream>
#include <Windows.h>

const int screenx = 120;//important number
const int screeny = 40;//doesnt work with other dims

char* screen;
HANDLE hConsole;
DWORD dwBytesWritten = 0;

const char* brightnessList = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ";
int brightnessListLength;

char ColourToAscii(int r, int g, int b){
    float brightness = r + g + b;
    brightness /= 3.f * 255.f;
    brightness = 1.f - brightness;
    int index = brightness * (float)brightnessListLength;
    return brightnessList[index];
}

void DrawPixel(
    int x, int y, int r, int g, int b
)
{
    #if SAFE
        bool validArgs = true;
        validArgs = (r >= 0 && r <= 255) * validArgs;
        validArgs = (g >= 0 && g <= 255) * validArgs;
        validArgs = (b >= 0 && b <= 255) * validArgs;
        validArgs = (x >= 0 && x <= screenx) * validArgs;        validArgs = (y >= 0 && y <= screeny) * validArgs;
        if(validArgs == false){
            fprintf(stderr, 
                "Invalid args to draw pixel function "
                "%d %d %d %d %d"
            ,x,y,r,g,b);
            exit(1);
        }
    #endif
    char character = ColourToAscii(r,g,b);
    screen[x + y * screenx] = character;
}

void DisplayUpdate(){
    WriteConsoleOutputCharacter(hConsole, screen, screenx * screeny, { 0,0 }, &dwBytesWritten);
}

void GraphicsInit(){
    screen = new char[screenx * screeny];
    hConsole = CreateConsoleScreenBuffer(GENERIC_READ | GENERIC_WRITE, 0, NULL, CONSOLE_TEXTMODE_BUFFER, NULL);
    SetConsoleActiveScreenBuffer(hConsole);
    brightnessListLength = strlen(brightnessList);

    memset(screen, ' ', screenx * screeny);
    screen[screenx * screeny - 1] = '\0';
}

#ifndef IS_INCLUDE
int main(){
    GraphicsInit();
    int counter = 0;
    while(1){
        int r,g,b;
        r = counter;
        g = r; b = r;
        DrawPixel(2,2,r,g,b);
        DrawPixel(0,0,r,g,b);
        DrawPixel(10,0,r,g,b);
        DisplayUpdate();
        counter++;
        Sleep(10);
        if(counter > 255) counter = 0;
    }

    return 0;
}
#endif
