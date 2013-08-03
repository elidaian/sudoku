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
#define MAX_GRIDS 100
#define MAX_DIST 1000
#define MAX_NUM 10000
#define MAX_TRIALS 10
int my_random (int num);
typedef struct s_params
{
	int blockWidth,blockHeight,nGrids,*offsetsX,* offsetsY;
	char samurai,diagonals;
	int num,restrictinters;
}
t_params;
int ParseParams(t_params *p,int argc,char *argv[]);
void FreeParams(t_params *p);
int CreateProblems(t_board_p b,t_params *p,int *cells,int *symbols,char *given,int serial);
int main(int argc,char *argv[])
{
	t_params par;
	t_board_p b;
	int n,nCl,serial;
	int *cells,*symbols;
	char *given;
	FILE *pf;
	srand((unsigned)time(NULL));
	PrintGPL(stdout);
	if(ParseParams(&par,argc,argv)!=0)
	{
		SYSTEM_PAUSE;
		return -1;
	}
	printf("Run \"demo4-creator -h\" for help.\n");
	printf("Creating %d problems...\n",par.num);
	if(par.samurai)
		b=ConstructSamuraiBoard(par.blockWidth,par.blockHeight,par.diagonals);
	else
		b=ConstructCustomBoard(par.blockWidth,par.blockHeight,par.diagonals,par.nGrids,par.offsetsX,par.offsetsY);
	if(!b)
		fprintf(stderr,"ERROR: Not enough free memory available\n");
	else
	{
		nCl=GetNumCells(b);
		cells=(int*)malloc(nCl*sizeof(int));
		symbols=(int*)malloc(nCl*sizeof(int));
		given=(char*)malloc((nCl+1)*sizeof(char));
		if(!cells||!symbols||!given)
			fprintf(stderr,"ERROR: Not enough free memory available\n");
		else
		{
			serial=0;
			if((pf=fopen("serial.txt","rt")))
			{
				fscanf(pf,"%d",&serial);
				fclose(pf);
				if(serial<0||serial>=MAX_NUM)
					serial=0;
			}
			if((pf=fopen("serial.txt","wt")))
			{
				fprintf(pf,"%d\n",serial+par.num);
				fclose(pf);
			}
			n=CreateProblems(b,&par,cells,symbols,given,serial);
			printf("%d problems created.\n",n);
		}
		free(cells);
		free(symbols);
		free(given);
		DestroyBoard(b);
	}
	FreeParams(&par);
	SYSTEM_PAUSE;
	return 0;
}
int CreateProblems(t_board_p b,t_params *p,int *cells,int *symbols,char *given,int serial)
{
	int np,trials,nSy,nCl,i,j,k,n,c,s;
	e_state state;
	char name[4][50];
	FILE *pf,*raw;
	nSy=GetNumSymbols(b);
	nCl=GetNumCells(b);
	for(np=0;np<p->num;np++)
	{
		CleanBoard(b);
		n=trials=0;
			do
			{
				do
					c=my_random(nCl);
				while(GetNumPossValuesOfCell(b,c)==1||(p->restrictinters&&GetNumGroupsOfCell(b,c)>=p->restrictinters));
				s=my_random(GetNumPossValuesOfCell(b,c));
				for(i=j=0;i<nSy;i++)
					if((1<<i)&GetPossValuesOfCell(b,c))
					{
						if(j==s)
							break;
						else
							j++;
					}
				s=i;
				SetSymbolInCell(b,s,c);
				Solve(b,0,FALSE);
				state=GetState(b);
				if(state==impossible)
				{
					CleanBoard(b);
					if(trials<MAX_TRIALS)
					{
						for(i=0;i<n;i++)
							SetSymbolInCell(b,symbols[i],cells[i]);
						trials++;
					}
					else
						n=trials = 0;
					continue;
				}
				symbols[n]=s;
				cells[n]=c;
				n++;
			}
			while (state!=solved);
			for (j=0;j<n;)
			{
				CleanBoard(b);
				for(i=0;i<n;i++)
					if(i!=j)
						SetSymbolInCell(b,symbols[i],cells[i]);
					Solve(b,0,FALSE);
					if(GetState(b)==solved)
					{
						n--;
						s=1;
						for(i=j;i<n;i++)
						{
							symbols[i]=symbols[i+1];
							cells[i]=cells[i+1];
						}
					}
					else
						j++;
			}
			CleanBoard (b);
			for(i=0;i<n;i++)
				SetSymbolInCell(b,symbols[i],cells[i]);
			Solve(b,0,FALSE);
			if(!GetNumRulesNGt1(b))
			{
				k=nCl/5+my_random(nCl/2-nCl/5);
				for(i=0;i<nCl;i++)
					given[i]=0;
				for(i=0;i<n;i++)
					given[cells[i]]=1;
				if(n<k)
					do
					{
						do
							c=my_random(nCl);
						while(given[c]);
						symbols[n]=GetSymbolOfCell(b,c);
						cells[n]=c;
						given[c]=1;
						n++;
					}
					while(n<k);
			}
			CleanBoard(b);
			for(i=0;i<n;i++)
				SetSymbolInCell(b,symbols[i],cells[i]);
			Solve(b,0,FALSE);
			if(GetNumRulesNGt2(b))
			{
				sprintf(name[0],"%sN3x%02d-N2x%02d-%03d-%05d.html",p->diagonals?"D-":"",GetNumRulesNGt2(b),GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[1],"%sN3x%02d-N2x%02d-%03d-%05d-raw.txt",p->diagonals?"D-":"",GetNumRulesNGt2(b),GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[2],"%sN3x%02d-N2x%02d-%03d-%05d-solution.html",p->diagonals?"D-":"",GetNumRulesNGt2(b),GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[3],"%sN3x%02d-N2x%02d-%03d-%05d",p->diagonals?"D-":"",GetNumRulesNGt2(b),GetNumRulesN2(b),nCl-n, np+serial);
			}
			else if(GetNumRulesN2(b))
			{
				sprintf(name[0],"%sN2x%02d-%03d-%05d.html",p->diagonals?"D-":"",GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[1],"%sN2x%02d-%03d-%05d-raw.txt",p->diagonals?"D-":"",GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[2],"%sN2x%02d-%03d-%05d-solution.html",p->diagonals?"D-":"",GetNumRulesN2(b),nCl-n, np+serial);
				sprintf(name[3],"%sN2x%02d-%03d-%05d",p->diagonals?"D-":"",GetNumRulesN2(b),nCl-n, np+serial);
			}
			else
			{
				sprintf(name[0],"%sN1-%03d-%05d.html",p->diagonals?"D-":"",nCl-n,np+serial);
				sprintf(name[1],"%sN1-%03d-%05d-raw.txt",p->diagonals?"D-":"",nCl-n,np+serial);
				sprintf(name[2],"%sN1-%03d-%05d-solution.html",p->diagonals?"D-":"",nCl-n,np+serial);
				sprintf(name[3],"%sN1-%03d-%05d",p->diagonals?"D-":"",nCl-n,np+serial);
			}
			pf=fopen(name[0],"wb");
			if(!pf)
			{
				perror(name[0]);
				break;
			}
			raw=fopen(name[1],"wb");
			if(!raw)
			{
				fclose(pf);
				perror(name[1]);
				break;
			}
			CleanBoard(b);
			for(i=0;i<n;i++)
				SetSymbolInCell(b,symbols[i],cells[i]);
			printHead(pf,"");
			PrintHTMLBoard(b,pf, NULL,NULL);
			GetBoardRaw(b,given,NULL,NULL);
			fprintf(raw,"%d\n%s\n#\n%s\n",n,name[1],given);
			fprintf(pf,"\t<CENTER>\n\t\t<I>%s</I>\n\t</CENTER>\n",name[3]);
			printFoot(pf);
			fclose(pf);
			pf=fopen(name[2],"wb");
			if(!pf)
			{
				fclose(raw);
				perror(name[2]);
			}
			printHead(pf," Solution");
			Solve(b,0,FALSE);
			PrintHTMLBoard(b,pf,NULL,NULL);
			GetBoardRaw(b,given,NULL,NULL);
			fprintf(raw,"\n@\n%s\n",given);
			fclose(raw);
			fprintf(pf,"\t<CENTER>\n\t\t<I>%s</I>\n\t</CENTER>\n",name[3]);
			printFoot(pf);
			fclose(pf);
			serial++;
			if(serial>=MAX_NUM)
				serial=MAX_NUM;
	}
	return np;
}
int ParseParams(t_params *p,int argc,char *argv[])
{
	int i,j;
	char ok,wrong,incompatible,nomem;
	p->blockWidth=p->blockHeight=3;
	p->nGrids=0;
	p->offsetsX=p->offsetsY=NULL;
	p->samurai=p->diagonals=FALSE;
	p->num=1;
	p->restrictinters=0;
	ok=TRUE;
	wrong=incompatible=nomem=FALSE;
	for(i=1;i<argc&&ok;i++)
		if(!strcmp(argv[i],"-samurai"))
		{
			if(p->nGrids)
			{
				ok=FALSE;
				incompatible=TRUE;
				break;
			}
			p->samurai=TRUE;
		}
		else if(!strcmp(argv[i],"-grids"))
		{
			if(p->samurai)
			{
				ok=FALSE;
				incompatible=TRUE;
				break;
			}
			i++;
			if(i>=argc)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			p->nGrids=-1;
			p->nGrids=atoi (argv[i]);
			if(p->nGrids<2||p->nGrids>MAX_GRIDS)
			{
				p->nGrids=0;
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			p->offsetsX=(int*)malloc(p->nGrids*sizeof(int));
			p->offsetsY=(int*)malloc(p->nGrids*sizeof(int));
			if(!p->offsetsX||!p->offsetsY)
			{
				ok=FALSE;
				nomem=TRUE;
				break;
			}
			for(j=0;j<p->nGrids;j++,i+=2)
			{
				if (i+2>=argc)
				{
					ok=FALSE;
					wrong=TRUE;
					break;
				}
				p->offsetsX[j]=p->offsetsY[j]=MAX_DIST+1;
				p->offsetsX[j]=atoi(argv[i+1]);
				p->offsetsY[j]=atoi(argv[i+2]);
				if(p->offsetsX[j]<-MAX_DIST||p->offsetsX[j]>MAX_DIST||p->offsetsY[j]<-MAX_DIST||p->offsetsY[j]>MAX_DIST)
				{
					ok=FALSE;
					wrong=TRUE;
					break;
				}
			}
			if(!ok)
				break;
		}
		else if(!strcmp(argv[i],"-blocksize"))
		{
			i++;
			if(i+1>=argc)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			p->blockWidth=p->blockHeight=-1;
			p->blockWidth=atoi(argv[i]);
			p->blockHeight=atoi(argv[i+1]);
			if(p->blockWidth<2||p->blockHeight<2||p->blockWidth*p->blockHeight>30)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			i++;
		}
		else if(!strcmp(argv[i],"-num"))
		{
			i++;
			if(i>=argc)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			p->num=-1;
			p->num=atoi(argv[i]);
			if(p->num<1||p->num>MAX_NUM)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
		}
		else if(!strcmp(argv[i],"-restrictinters"))
		{
			i++;
			if(i>=argc)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
			p->restrictinters=-1;
			p->restrictinters=atoi(argv[i]);
			if(p->restrictinters<0)
			{
				ok=FALSE;
				wrong=TRUE;
				break;
			}
		}
		else if(!strcmp(argv[i],"-diagonals"))
		{
			p->diagonals=TRUE;
		}
		else if(!strcmp(argv[i],"-h"))
		{
			printf("\n\tUSAGE:\n\tdemo4-creator [parameters]\n\n\tPOSSIBLE PARAMETERS:\n\t  -h\t(show this help)\n\t  -samurai\n\t  -grids n x1 y1 x2 y2... xn yn\n\t  -blocksize width height\n\t  -diagonals\n\t  -num n\n\t  -restrictinters numinters\n\n");
			FreeParams(p);
			return -1;
		}
		else
		{
			ok=FALSE;
			wrong=TRUE;
		}
	if(ok)
		return 0;
	if(wrong)
		fprintf(stderr,"ERROR: Wrong parameters\n");
	else if(incompatible)
		fprintf(stderr,"ERROR: Incompatible parameters\n");
	else if(nomem)
		fprintf(stderr,"ERROR: Not enough free memory available\n");
	FreeParams(p);
	return -1;
}
void FreeParams(t_params *p)
{
	if(p->offsetsX)
	{
		free(p->offsetsX);
		p->offsetsX=NULL;
	}
	if(p->offsetsY)
	{
		free(p->offsetsY);
		p->offsetsY=NULL;
	}
}
int my_random(int num)
{
	double d;
	int r;
	d=rand()/(double)RAND_MAX;
	r=(int)(d*num);
	return r<0?0:r>=num?num-1:r;
}
