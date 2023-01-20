#include<stdio.h>
#include <string.h>

int main()
{
    char str[15];
    char *secret="You don't get to see this";
    puts("I will repeat whatever you say");
    scanf("%s",str);
    strcat(str, "\n");
    printf(str);
    return 0;
}

// b *(main+100)