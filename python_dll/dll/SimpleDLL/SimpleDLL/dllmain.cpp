// dllmain.cpp : Defines the exported functions for the DLL.
#include "pch.h" // use stdafx.h in Visual Studio 2017 and earlier
#include <utility>
#include <limits.h>
#include "dllmain.h"

int add(
    const int a,
    const int b
)
{
    return a + b;
}

int minus(
    const int a,
    const int b
)
{
    return a - b;
}
