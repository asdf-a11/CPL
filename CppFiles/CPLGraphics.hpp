#pragma once
#include <iostream>
#include <chrono>
#include <thread>
#define uint unsigned int
#define ulong unsigned long

#define looph(v,h) for(int v = 0; v < (h); v++)
//#define SAFE true
#ifdef _WIN32
    //#define byte unsigned char
    #undef UNICODE
    #undef _UNICODE
    #include <windows.h>
    #undef min
    #undef max
#else
#define byte unsigned char
//Linux stuff
namespace X11{
    #include <X11/Xlib.h> // Primary Xlib header for X Window System client-side programming
    #include <X11/Xutil.h> // Utility functions for Xlib
    #include <X11/Xos.h>   // For X library 
}
#endif

namespace Graphics{
    #ifdef _WIN32
    //For windows
    LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
        if (msg == WM_DESTROY) PostQuitMessage(0);
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    
    struct Window{
        int width;
        int height;
        const char* title;
        uint frameCounter = 0;

        
        HWND hwnd;
        HDC hdc;
        

        Window(int w, int h, const char* t) : width(w), height(h), title(t) {}

        void Init(){
            
                WNDCLASS wc = {0};
                wc.lpfnWndProc = WndProc;
                wc.hInstance = GetModuleHandle(NULL);
                wc.lpszClassName = "MyWindowClass";
                RegisterClass(&wc);

                hwnd = CreateWindow("MyWindowClass", "Pixel Window", WS_OVERLAPPEDWINDOW,
                                        CW_USEDEFAULT, CW_USEDEFAULT, 
                                        width, height,
                                        NULL, NULL, wc.hInstance, NULL);
                ShowWindow(hwnd, SW_SHOW);

                hdc = GetDC(hwnd);

            
        }
        void Pump(){
            MSG msg = {0};
            GetMessage(&msg, NULL, 0, 0);
            TranslateMessage(&msg);
            DispatchMessage(&msg);

        }
        /*
        void StartLoop(fnptr(void, loopFunction, Window*)){
            MSG msg = {0};
            while (true) { 
                bool bRet = PeekMessage(&msg, NULL, 0, 0, PM_REMOVE);

                if (bRet) {
                    // A message was retrieved
                    if (msg.message == WM_QUIT) {
                        break; // Exit the loop when WM_QUIT is received
                    }

                    TranslateMessage(&msg); // Translate virtual-key messages into character messages
                    DispatchMessage(&msg);
                }
                else{
                    //Pump();
                    loopFunction(this);
                    // Set pixel at (100, 100) to red
                    frameCounter++;
                    if(frameCounter > 1000000)frameCounter = 0;
                }
            }
        }
        */
        void DrawPixel(int x, int y, byte r, byte g, byte b){
            SetPixel(hdc, x, y, RGB((int)(r), (int)(g), (int)(b)));
        }
        bool IsKeyPress(uint keyId){
            std::cerr << "Appoligies but getting key presses on windows is not implimented yet\n";
            return false;
        }
    };
    #else
    //For Linux
    struct Window{
        int width;
        int height;
        const char* title;
        uint frameCounter = 0;

        // Global variables for X11 components
        X11::Display* display;     // Connection to the X server
        X11::Window window;        // The ID of our created window
        X11::GC gc;                // Graphics Context for drawing operations
        ulong redByteMask;
        ulong blueByteMask;
        ulong greenByteMask;

        Window(int w, int h, const char* t) : width(w), height(h), title(t) {}

        // Function to initialize the X11 window
        void Init() {
            using namespace X11;


            // 1. Open a connection to the X server
            // XOpenDisplay(NULL) connects to the default display
            display = XOpenDisplay(NULL);
            if (display == NULL) {
                std::cerr << "Error: Could not open X display." << std::endl;
                //eturn false;
            }
            std::cout << "Connected to X display." << std::endl;

            // Get the default screen number
            int screen_num = DefaultScreen(display);
            // Get the root window of the default screen (the desktop background)
            X11::Window root_window = DefaultRootWindow(display);
            // Get the default color map
            Colormap colormap = DefaultColormap(display, screen_num);

            // 2. Define window attributes
            XSetWindowAttributes window_attributes;
            // Set the background pixel to black
            window_attributes.background_pixel = XBlackPixel(display, screen_num);
            // Set the border pixel to white
            window_attributes.border_pixel = XWhitePixel(display, screen_num);
            // Set event mask to receive exposure events (when window needs redrawing)
            window_attributes.event_mask = ExposureMask | KeyPressMask; // Add KeyPressMask for basic input

            // 3. Create the window
            // XCreateSimpleWindow is a convenient function for basic windows
            window = XCreateSimpleWindow(
                display,            // Display connection
                root_window,        // Parent window (root window in this case)
                100, 100,           // X, Y position (top-left corner)
                width, height,      // Width, Height of the window
                1,                  // Border width
                window_attributes.border_pixel, // Border pixel value
                window_attributes.background_pixel // Background pixel value
            );

            // Set standard properties for the window manager (title, size hints)
            XStoreName(display, window, title); // Set window title

            // 4. Create a Graphics Context (GC)
            // The GC holds all the state for drawing operations (e.g., foreground color, line style)
            XGCValues gc_values;
            gc_values.foreground = XWhitePixel(display, screen_num); // Set foreground color to white by default
            gc_values.background = XBlackPixel(display, screen_num); // Set background color to black
            gc = XCreateGC(display, window, GCForeground | GCBackground, &gc_values);

            // 5. Map the window to the screen (make it visible)
            XMapWindow(display, window);
            // Flush the output buffer to ensure commands are sent to the server immediately
            XFlush(display);

            std::cout << "Window created and mapped." << std::endl;
            X11::XWindowAttributes attr;
            XGetWindowAttributes(display, DefaultRootWindow(display), &attr);
    
            X11::Visual* visual = attr.visual;
            redByteMask = visual->red_mask;
            greenByteMask = visual->green_mask;
            blueByteMask = visual->blue_mask;
            //return true;

            X11::XSelectInput(display, window, KeyPressMask | ExposureMask);
        }
        unsigned long RgbToPixel(X11::Display* display, byte r, byte g, byte b) {
            using namespace X11;
            XWindowAttributes attr;
            XGetWindowAttributes(display, DefaultRootWindow(display), &attr);
            
            Visual* visual = attr.visual;

            return ( ((r * visual->red_mask) / 255) & visual->red_mask ) |
                ( ((g * visual->green_mask) / 255) & visual->green_mask ) |
                ( ((b * visual->blue_mask) / 255) & visual->blue_mask );
        }

        // Function to draw a single pixel
        void DrawPixel(int x, int y, byte r, byte g, byte b) {
            using namespace X11;
            byte lst[3] = {r,g,b};
            union{
                ulong colour_ul;
                byte byteList[4];
            };
            colour_ul = 0;
            ulong maskList[3] = {redByteMask, greenByteMask, blueByteMask};
            //byte byteList[3];            
            looph(i,3){
                union{
                    byte b[4];
                    ulong a;
                };                
                byte c = lst[i];
                b[0] = c; b[1] = c; b[2] = c; b[3] = c;
                ulong v = (a & maskList[i]);
                colour_ul = colour_ul | v;
            }
            //ulong colour_ul = RgbToPixel(display, byteList[0], byteList[1], byteList[2]);
            // Set the foreground color of the graphics context
            XSetForeground(display, gc, colour_ul);
            // Draw the point (pixel)
            XDrawPoint(display, window, gc, x, y);
        }

       bool keyPressBuffer[256];
        bool IsKeyPressed(uint keyId){
            #if SAFE == true
                if(keyId > 255)
                    std::cerr << "Invalid key \n";
            #endif
            return keyPressBuffer[keyId];
        }
        /*
        void StartLoop(fnptr(void, loopFunction, Window*)){
            using namespace X11;


            X11::XSelectInput(display, window, KeyPressMask | ExposureMask);

            XEvent event;
            while (true) {
                memset(keyPressBuffer, false, sizeof(keyPressBuffer));
                while (XPending(display)) {
                    XNextEvent(display, &event);

                    switch (event.type) {
                        case KeyPress: {
                            char text[255];
                            KeySym keysym;
                            XLookupString(&event.xkey, text, sizeof(text), &keysym, NULL);

                            // Print key for debugging
                            //std::cout << "Key pressed: " << XKeysymToString(keysym) << " (" << keysym << ")" << std::endl;

                            if (keysym == XK_q || keysym == XK_Q) {
                                //std::cout << "Quit key pressed. Exiting." << std::endl;
                                //exit(0);
                            }

                            if(keysym < 256 && keysym >= 0){
                                keyPressBuffer[keysym] = true;
                            }

                            // Example: set a simple flag for this key
                            // You should map keysym to a buffer carefully if you plan to use an array
                            break;
                        }
                    }
                }

                loopFunction(this);

                // Optional: Reset key flags if needed AFTER loopFunction processes them
                // memset(keyPressBuffer, false, sizeof(keyPressBuffer));

                frameCounter++;
            }

 
            // Clean up X11 resources
            XFreeGC(display, gc);        // Free the graphics context
            XDestroyWindow(display, window); // Destroy the window
            XCloseDisplay(display);      // Close the connection to the X server
            std::cout << "X11 resources cleaned up. Program finished." << std::endl;
        }
            */
        void CloseWindow(){
            using namespace X11;
            XFreeGC(display, gc);        // Free the graphics context
            XDestroyWindow(display, window); // Destroy the window
            XCloseDisplay(display);      // Close the connection to the X server
            std::cout << "X11 resources cleaned up. Program finished." << std::endl;
        }
        void Pump(){
            using namespace X11;
            XEvent event;
            memset(keyPressBuffer, false, sizeof(keyPressBuffer));
            while (XPending(display)) {
                XNextEvent(display, &event);

                switch (event.type) {
                    case KeyPress: {
                        char text[255];
                        KeySym keysym;
                        XLookupString(&event.xkey, text, sizeof(text), &keysym, NULL);

                        // Print key for debugging
                        //std::cout << "Key pressed: " << XKeysymToString(keysym) << " (" << keysym << ")" << std::endl;

                        if (keysym == XK_q || keysym == XK_Q) {
                            //std::cout << "Quit key pressed. Exiting." << std::endl;
                            //exit(0);
                        }

                        if(keysym < 256 && keysym >= 0){
                            keyPressBuffer[keysym] = true;
                        }

                        // Example: set a simple flag for this key
                        // You should map keysym to a buffer carefully if you plan to use an array
                        break;
                    }
                }
            }
        }
    };
    #endif
}

Graphics::Window window(600,600,"CPLGRAPHICS");
int graphicsinit(int xsize, int ysize){
    window.height = ysize;
    window.width = xsize;
    window.Init();
    return 0;
}
void graphicspump(){
    window.Pump();
}
int drawpixel(int x, int y, int r, int g, int b){
    window.DrawPixel(x,y,(byte)r,(byte)g,(byte)b);
    return 0;
}
int graphicssleep(int ticks){
    std::this_thread::sleep_for(std::chrono::milliseconds(ticks));
    return 0;
}
int getkeypress(int keyId){
    return window.IsKeyPressed(keyId) ? 1 : 0;
}