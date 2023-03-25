#ifndef HEADER_FILE_H
#define HEADER_FILE_H
#define N 100

#include <stdio.h>

struct User{
    char username;
    int password;
};

typedef struct User User;

typedef struct {
    int x;
    int y;
} Point;

typedef char string;
typedef int my_int;

void print_point(Point p);

int add(int x, int y);

my_int calc(int a, int b, int c);

User addUser(string name, int pass);


#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))

#endif
