#include<stdio.h>
#include<stdlib.h>
#include<memory.h>
#include "sudoku-pr.h"
t_board *ConstructBasicBoard(int order,char diag)
{
	int n,row,col,cell,block,group;
	t_board *b;
	t_group *g;
	if(order<2||order>5)
		return NULL;
	n=order*order;
	b=AllocateBoardSkeleton(n*n,diag?3*n+2:3*n,n,n,n,order,order);
	if(!b)
		return NULL;
	for(group=0;group<n;group++)
		b->pGr[group].type=GR_BLOCK;
	for (group=n;group<2*n;group++)
		b->pGr[group].type=GR_ROW;
	for (group=2*n;group<3*n;group++)
		b->pGr[group].type=GR_COL;
	if (diag)
		b->pGr[3*n].type=b->pGr[3*n+1].type = GR_DIAG;
	for(row=cell=0;row<n;row++)
		for(col=0;col<n;col++,cell++)
		{
			b->pCl[cell].y=row;
			b->pCl[cell].x=col;
			b->pppCl[row][col]=b->pCl+cell;
			block=row-row%order+col/order;
			g=b->pGr+block;
			g->ppCl[g->nCl++]=b->pCl+cell;
			g=b->pGr+n+row;
			g->ppCl[g->nCl++]=b->pCl+cell;
			g=b->pGr+2*n+col;
			g->ppCl[g->nCl++]=b->pCl+cell;
			if(diag&&row==col)
			{
				g=b->pGr+3*n;
				g->ppCl[g->nCl++]=b->pCl+cell;
			}
			if(diag&&row==n-1-col)
			{
				g=b->pGr+3*n+1;
				g->ppCl[g->nCl++]=b->pCl+cell;
			}
		}
	if(!CompleteBoard(b))
	{
		DestroyBoard(b);
		return NULL;
	}
	return b;
}
t_board *ConstructCustomBoard(char wb,char hb,char diag,int nGrids,int *xg,int *yg)
{
	int n,nCells,nGroups,zero,nGroupsPerGrid;
	int xmin,xmax,ymin,ymax,width,height;
	int i,j,k,x,y;
	int group,cell,row,col,block;
	t_board *b;
	t_group *g;
	n=wb*hb;
	if(wb<1||hb<1||n<4||n>30)
		return NULL;
	if(nGrids<1||!xg||!yg)
	{
		zero=0;
		xg=yg=&zero;
		nGrids=1;
	}
	nGroupsPerGrid=diag?3*n+2:3*n;
	nGroups=nGrids*nGroupsPerGrid;
	nCells=nGrids*n*n;
	xmin=xmax=xg[0];
	ymin=ymax=yg[0];
	for(i=1;i<nGrids;i++)
	{
		if(xg[i]<xmin)
			xmin=xg[i];
		else if(xg[i]>xmax)
			xmax=xg[i];
		if(yg[i]<ymin)
			ymin=yg[i];
		else if(yg[i]>ymax)
			ymax=yg[i];
		for(x=xg[i];x<xg[i]+hb;x++)
			for(y=yg[i];y<yg[i]+wb;y++)
				for(j=0;j<i;j++)
					if(x>= xg[j]&&x<xg[j]+hb&&y>=yg[j]&&y<yg[j]+wb)
					{
						nCells-=hb*wb;
						break;
					}
	}
	width=(xmax-xmin+hb)*wb;
	height=(ymax-ymin+wb)*hb;
	b=AllocateBoardSkeleton(nCells,nGroups,n,width,height,wb,hb);
	if(!b)
		return NULL;
	for(i=group=0;i<nGrids;i++)
	{
		for(j=0;j<n;j++,group++)
			b->pGr[group].type=GR_BLOCK;
		for(j=0;j<n;j++,group++)
			b->pGr[group].type=GR_ROW;
		for (j=0;j<n;j++,group++)
			b->pGr[group].type=GR_COL;
		if (diag)
		{
			b->pGr[group++].type=GR_DIAG;
			b->pGr[group++].type=GR_DIAG;
		}
	}
	for(y=cell=0;y<height;y++)
		for(x=0;x<width;x++)
		{
			for(i=j=0;i<nGrids;i++)
			{
				row=y-(yg[i]-ymin)*hb;
				col=x-(xg[i]-xmin)*wb;
				if(row>=0&&row<n&&col>=0&&col<n)
				{
					j=1;
					block=row-row%hb+col/wb;
					k=i*nGroupsPerGrid;
					g=b->pGr+k+block;
					g->ppCl[g->nCl++]=b->pCl+cell;
					g=b->pGr+k+n+row;
					g->ppCl[g->nCl++]=b->pCl+cell;
					g=b->pGr+k+2*n+col;
					g->ppCl[g->nCl++]=b->pCl+cell;
					if(diag&&row==col)
					{
						g=b->pGr+k+3*n;
						g->ppCl[g->nCl++]=b->pCl+cell;
					}
					if(diag&&row==n-1-col)
					{
						g=b->pGr+k+3*n+1;
						g->ppCl[g->nCl++]=b->pCl+cell;
					}
				}
			}
			if(j)
			{
				b->pCl[cell].y=y;
				b->pCl[cell].x=x;
				b->pppCl[y][x]=b->pCl+cell;
				cell++;
			}
		}
	if(!CompleteBoard(b))
	{
		DestroyBoard(b);
		return NULL;
	}
	return b;
}
t_board *ConstructSamuraiBoard(char wb,char hb,char diag)
{
	int xg[5],yg[5];
	xg[4]=yg[4]=0;
	xg[0]=-(hb-1);
	yg[0]=-(wb-1);
	xg[1]=hb-1;
	yg[1]=-(wb-1);
	xg[2]=-(hb-1);
	yg[2]=wb-1;
	xg[3]=hb-1;
	yg[3]=wb-1;
	return ConstructCustomBoard(wb,hb,diag,5,xg,yg);
}
