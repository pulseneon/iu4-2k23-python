#ifndef HEADER_FILE_H
#define HEADER_FILE_H

#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

typedef char[] string; // 1 что должно найти

void print_point(Point p); // 2

int add(int x, int y); // 3

#define PI 3.14159 // 4 
#define MAX(a, b) ((a) > (b) ? (a) : (b))

#endif