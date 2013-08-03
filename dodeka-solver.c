#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#include<ctype.h>
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
	char fname[100],T[145];
	FILE *pf;
	int c,i=0;
	PrintGPL(stdout);
	b=ConstructCustomBoard(4,3,FALSE,0,NULL,NULL);
	printf("Type raw problem filename:\n");
	scanf("%s",fname);
	if((pf=fopen(fname,"rt"))==NULL)
	{
		perror(fname);
		return -1;
	}
	while((c=getc(pf))!=EOF)
	{
		if(!isspace(c))
			T[i++]=c;
	}
	fclose(pf);
	T[i]='\0';
	if(b)
	{
		SetBoard(b,T,NULL,NULL);
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
