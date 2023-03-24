#ifndef HEADER_FILE_H
#define HEADER_FILE_H

#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

typedef char string[];

void print_point(Point p);

int add(int x, int y);

#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))

#endif