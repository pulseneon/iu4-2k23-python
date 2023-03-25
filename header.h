#ifndef HEADER_FILE_H
#define HEADER_FILE_H

#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

typedef char[] string;
typedef int my_int;

void print_point(Point p);

int add(int x, int y);

my_int calc(int a, int b, int c);


#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))

#endif
