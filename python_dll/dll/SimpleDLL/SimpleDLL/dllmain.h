// DLLMAIN.h - Contains declarations of math functions
#pragma once

#ifdef DLLMAIN_EXPORTS
#define DLLMAIN_API __declspec(dllexport)
#else
#define DLLMAIN_API __declspec(dllimport)
#endif

extern "C" DLLMAIN_API int add(const int a, const int b);

extern "C" DLLMAIN_API int minus(const int a, const int b);
