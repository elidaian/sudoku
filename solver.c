#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#include "sudoku-pub.h"
#include "html-gen.h"
#include "sudoku-iface.c"
#include "sudoku-mem.c"
#include "sudoku-grids.c"
#include "sudoku-solver.c"
#if SYSTEM==WINDOWS
#define SYSTEM_PAUSE system ("pause")
#else
#define SYSTEM_PAUSE
#endif
int main()
{
	t_board_p b;
	char T[82];
	PrintGPL (stdout);
	b=ConstructBasicBoard (3,FALSE);
	printf("Type raw problem:\n");
	scanf("%s",T);
	if(b)
	{
		SetBoard (b,T,NULL,NULL);
		printf("Problem:\n");
		PrintBoard(b,stdout,NULL,NULL);
		Solve(b,0,FALSE);
		printf("\nSolution:\n");
		PrintBoard(b,stdout,NULL,NULL);
		DestroyBoard(b);
	}
	SYSTEM_PAUSE;
	return 0;
}
