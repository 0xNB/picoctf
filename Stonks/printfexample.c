#include <stdio.h>

int main(int argc, char **argv) {
	if (argc != 2) {
		printf("usage: %s <name>\n", argv[0]);
		exit(1);
	}

	// correct version without vulnerability
	printf("my name is: %s\n", "niklas");

	// vulnerable version 
	printf("my name is: ");
	printf(argv[1]);
}
