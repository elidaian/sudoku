/*
-------------------------------------------------------------------
SUDOKU SENSEI 1.03: a Sudoku Explainer Engine
Copyright (C) 2005  Martin Knoblauch

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA  02110-1301, USA.

Contact the author: comocomocomo AT users.sourceforge.net
Latest versions: http://sourceforge.net/projects/sudoku-sensei
-------------------------------------------------------------------

    sudoku-iface.c
*/
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "sudoku-pr.h"
//#include "html-gen.h"
void PrintGPL(FILE *pf)
{
	fprintf(pf,"-------------------------------------------------------------------\nSUDOKU SENSEI 1.03: a Sudoku Explainer Engine\nCopyright (C) 2005  Martin Knoblauch\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston,\nMA  02110-1301, USA.\n\nContact the author: comocomocomo AT users.sourceforge.net\nLatest versions: http://sourceforge.net/projects/sudoku-sensei\n-------------------------------------------------------------------\n\n");
}
int GetNumCells(t_board *b)
{
	return b->nCl;
}
int GetCellY(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].y;
}
int GetCellX(t_board * b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].x;
}
int GetCellNumber(t_board *b,int x,int y)
{
	if(x<0||y<0||x>=b->w||y>=b->h||!b->pppCl[y][x])		/* If the coords, are wrong or there's a hole there... */
		return -1;										/* ...invalid number */
	return b->pppCl[y][x]-b->pCl;						/* Otherwise, calculate index */
}														/* using pointer arithmetic */
int CellWasChangedByLastRule(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return (b->pCl[cell].flags&DIRTY_FLAG)?1:0;
}
int GetNumPossValuesOfCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].nPV;
}
int GetPossValuesOfCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].mPV;
}
int GetLastRemovedPossValuesOfCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].mRPV;
}
int GetSymbolOfCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].nPV==1?b->pCl[cell].FV:-1;
}
void RemovePossValuesFromCell(t_board *b,int mask,int cell)
{
	int i,n,sy;
	t_cell *c;
	if(!b||cell<0||cell>=b->nCl||!mask)
		return;
	c=b->pCl+cell;
	c->mRPV|=mask&c->mPV;					/* Backup ones to be removed */
	c->mPV&=~mask;							/* and then remove them */
	for(i=n=0,sy=-1;i<b->nSy;i++)
		if(c->mPV&(1<<i))
		{
			n ++;							/* Count remaining possible values */
			sy=i;							/* and remember one of them */
		}
	c->nPV=n;
	if(n==1)								/* If only one symbol is possible now, */
		c->FV=sy;							/* save it */
	if(!(c->flags&DIRTY_FLAG))				/* If the cell */
	{										/* is clean, */
		ListExtract(&b->CleanCL,&c->lnode);	/* move it to the dirty cells list */
		ListInsert(&b->DirtyCL,&c->lnode);
		c->flags|=DIRTY_FLAG;
	}
}
int SetSymbolInCell(t_board *b,int val,int cell)
{
	int i,j;
	t_cell *c;
	t_group *g;
	if(!b||cell<0||cell>=b->nCl||val<0||val>=b->nSy)
		return 0;
	c=b->pCl+cell;
	if(!b||b->state!=unsolved ||!b->pCl ||cell<0||cell>=b->nCl||val<0||val>=b->nSy||!((1<<val)&c->mPV))
																/* If any parameter is wrong or the value is not possible... */
		return 0;												/* ...error */
	if(ListGetNum(&b->DirtyCL))									/* If there are already dirty */
		for(i=0;i<c->nGr;i++)									/* cells, check further... */
		{
			g=c->ppGr[i];
																/* If any other cell in */
			for(j=0;j<b->nSy;j++)								/* one of the groups of */
				if(g->ppCl[j]!=c&&g->ppCl[j]->mPV==(1<<val))	/* this cell, can only have this value... */
					return 0;									/* ...error */
		}
																/* If there are no dirty cells, we can trust the */
																/* "possible values" stored in the cell (already checked) */
	RemovePossValuesFromCell(b,~(1<<val),c-b->pCl);
	if(!(c->flags&SOLVED_FLAG))									/* Only if not solved */
	{
		c->flags|=SOLVED_FLAG;									/* This cell is solved */
		c->nSolPos=b->nSol;										/* Save pos. in solving order */
		c->nGss=b->nGss;										/* Save num. of prev. guessings */
		b->nSol++;												/* Count solved cells */
		if(b->nSol==b->nCl)										/* If all cells are solved... */
			b->state=solved;									/* ...happy end! */
	}
	return 1;													/* Success */
}
int GetLastNCellsSolved(t_board *b,int num,int *cells)
{
	int i,j;
	if(num<=0||num>b->nSol)
		num=b->nSol;
	for(i=0;i<b->nCl;i++)
		if(b->pCl[i].flags&SOLVED_FLAG)
		{
			j=b->pCl[i].nSolPos-b->nSol+num;
			if(j>0)
				cells[j] = i;
		}
	return num;
}
int GetNumGroupsOfCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nCl)
		return -1;
	return b->pCl[cell].nGr;
}
int GetGroupOfCell(t_board *b,int group,int cell)
{
	if(cell<0||cell>=b->nCl||group<0||group>b->pCl[cell].nGr)
		return -1;
	return b->pCl[cell].ppGr[group]-b->pGr;
}
int GetNumGroups(t_board *b)
{
	return b->nGr;
}
int GetCellOfGroup(t_board *b,int cell,int group)
{
	if(group<0||group>=b->nGr||cell<0||cell>=b->pGr[group].nCl)
		return -1;
	return b->pGr[group].ppCl[cell]-b->pCl;
}
int GetGroupType(t_board *b,int group)
{
	if(group<0||group>=b->nGr)
		return -1;
	return b->pGr[group].type;
}
e_state GetState(t_board *b)
{
	return b->state;
}
int GetNumSolvedCells(t_board *b)
{
	return b->nSol;
}
int GetNumSymbols(t_board *b)
{
	return b->nSy;
}
int GetErrSymbolMask(t_board *b)
{
	return b->errmSy;
}
int GetErrCellMask(t_board *b)
{
	return b->errmCl;
}
int GetErrGroup(t_board *b)
{
	return b->errGr;
}
int GetNumGuessedCells(t_board *b)
{
	return b->nGss;
}
int GetTotalGuessings(t_board *b)
{
	return b->nGssTotal;
}
int GetGuessedCell(t_board *b,int cell)
{
	if(cell<0||cell>=b->nGss)
		return -1;
	return b->pnGssCl[cell];
}
int GetLastRuleLevel(t_board *b)
{
	return b->ruleLevel;
}
e_rule GetLastRuleType(t_board *b)
{
	return b->ruleLevel!=0?b->ruleType:norule;
}
int GetLastRuleGroup(t_board *b)
{
	return b->ruleGr;
}
int GetLastRuleIntersectedGroup(t_board *b)
{
	return b->ruleIGr;
}
int GetLastRuleCellsMask(t_board *b)
{
	return b->rulemCl;
}
int GetLastRuleSymbolsMask(t_board *b)
{
	return b->rulemSy;
}
int GetNumRulesN1(t_board *b)
{
	return b->nRulesN1;
}
int GetNumRulesN2(t_board *b)
{
	return b->nRulesN2;
}
int GetNumRulesNGt2(t_board *b)
{
	return b->nRulesNGt2;
}
int GetNumRulesNGt1(t_board *b)
{
	return b->nRulesN2+b->nRulesNGt2;
}
void PrintBoard(t_board *b,FILE *pf,const char *symbols,const char *empty)
{
	int x,y;
	t_cell *c;
	if(!symbols||!*symbols)
		symbols=b->nSy<=9?"123456789" :b->nSy<=30?"0123456789ABCDEFHJKLMNPRTUVWYZ":NULL;
	if(!empty||!*empty||!empty[1])
		empty=".X";
	if(!b||b->state==skeleton||!pf||!symbols)
		return;
	for(y=0;y<b->h;y++)
	{
		if(y&&b->hb>0&&!(y%b->hb))
			fputc('\n',pf);
		for(x=0;x<b->w;x++)
		{
			c=b->pppCl[y][x];
			if(x&&b->wb>0&&!(x%b->wb))
				fputc(' ', pf);
			if(!c)
				fprintf(pf,"  ");
			else if(c->nPV>1)
				fprintf(pf," %c",empty[0]);
			else if(c->nPV==0)
				fprintf(pf," %c", empty[1]);
			else
				fprintf(pf," %c",symbols[c->FV]);
		}
		fputc('\n',pf);
	}
}
void PrintHTMLBoard(t_board *b,FILE *pf,const char *symbols,const char *empty)
{
	int x[2],y[2];
	t_cell *c;
	if(!symbols||!*symbols)
		symbols=b->nSy<=9?"123456789" :b->nSy<=30?"0123456789ABCDEFHJKLMNPRTUVWYZ":NULL;
	if(!empty||!*empty||!empty[1])
		empty=".X";
	if(!b||b->state==skeleton||!pf||!symbols)
		return;
	openMainTable(pf,b->w,b->h);
	for(y[0]=0;y[0]<b->wb;y[0]++)
	{
		openMainLine(pf,b->wb);
		for(x[0]=0;x[0]<b->hb;x[0]++)
		{
			openMainRow(pf,b->hb);
			for(y[1]=0;y[1]<b->hb;y[1]++)
			{
				openLine(pf,b->hb);
				for(x[1]=0;x[1]<b->wb;x[1]++)
				{
					openRow(pf,b->wb);
					c=b->pppCl[b->hb*y[0]+y[1]][b->wb*x[0]+x[1]];
					if(!c)
						fprintf(pf,"&nbsp;");
					else if(c->nPV>1)
						fprintf(pf,"&nbsp;");
					else if(c->nPV==0)
						fprintf(pf,"%c", empty[1]);
					else
						fprintf(pf,"%c",symbols[c->FV]);
					closeRow(pf);
				}
				closeLine(pf);
			}
			closeMainRow(pf);
		}
		closeMainLine(pf);
	}
	closeMainTable(pf);
}
void PrintBoardPV (t_board * b,
                   FILE * pf,
                   const char * symbols,
                   const char * empty)
{
  int x, y, w, h, xc, yc, s;
  t_cell * c;

  if (!symbols || !*symbols)
    symbols = b->nSy<=9 ? "123456789" :
              b->nSy<=30 ? "0123456789ABCDEFHJKLMNPRTUVWYZ" :
              NULL;

  if (!empty || !*empty || !empty[1] || !empty[2])
    empty = ".X*";

  if (!b || b->state==skeleton || !pf || !symbols)
    return;

  for (h=2; (h+1)*(h+1)<=b->nSy; h++)
    {}

  w = (b->nSy+h-1) / h;

  for (y=0; y<b->h; y++)
  {
    if (y && b->hb>0 && !(y%b->hb))
      fputc ('\n', pf);

    for (yc=0; yc<h; yc++)
    {
      for (x=0; x<b->w; x++)
      {
        c = b->pppCl[y][x];

        if (x && b->wb>0 && !(x%b->wb))
          fprintf (pf, "   ");

        for (xc=0, s=yc*w; xc<w; xc++, s++)
          if (c && s<b->nSy)
          {
            if (c->nPV==0)
              fputc (empty[1], pf);
            else if (c->nPV==1)
            {
              if (xc==w/2 && yc==h/2)
                fputc (symbols[c->FV], pf);
              else
                fputc (' ', pf);
            }
            else if ((1<<s) & c->mPV)
              fputc (symbols[s], pf);
            else if ((1<<s) & c->mRPV)
              fputc (empty[2], pf);
            else
              fputc (empty[0], pf);
          }
          else
            fputc (' ', pf);

        fputc (' ', pf);
      }

      fputc ('\n', pf);
    }

    fputc ('\n', pf);
  }
}

int ReadBoard (t_board * b,
               FILE * pf,
               const char * symbols,
               const char * empty)
{
  int x, y, i, j, k, s;
  t_cell * c;

  if (!symbols || !*symbols)
    symbols = b->nSy<=9 ? "123456789" :
              b->nSy<=30 ? "0123456789ABCDEFHJKLMNPRTUVWYZ" :
              NULL;

  if (!empty || !*empty)
    empty = ".X0";

  if (!b || b->state==skeleton || !symbols)
    return 0;

  CleanBoard (b);

  if (!pf)
    return 0;

  clearerr (pf);

  for (y=i=0; y<b->h; y++)
    for (x=0; x<b->w; x++)
    {
      c = b->pppCl[y][x];

      if (!c)
        continue;

      for (;;)
      {
        s = fgetc (pf);

        if (s==EOF || ferror(pf))
          return 0;

        for (j=0; symbols[j] &&
                  symbols[j]!=s; j++)
          {}

        if (symbols[j])
          break;

        for (k=0; empty[k] &&
                  empty[k]!=s; k++)
          {}

        if (empty[k])
          break;

        i ++;
      }

      if (symbols[j])
        SetSymbolInCell (b, j, c-b->pCl);

      i ++;
    }

  return 1;
}

/*///////////////////////////////////////////////////////////////// */

void GetBoardRaw (t_board * b,
                  char * raw,
                  const char * symbols,
                  const char * empty)
{
  int x, y, i;
  t_cell * c;

  if (!symbols || !*symbols)
    symbols = b->nSy<=9 ? "123456789" :
              b->nSy<=30 ? "0123456789ABCDEFHJKLMNPRTUVWYZ" :
              NULL;

  if (!empty || !*empty || !empty[1])
    empty = ".X";

  if (!b || b->state==skeleton || !raw || !symbols)
    return;

  for (y=i=0; y<b->h; y++)
    for (x=0; x<b->w; x++)
    {
      c = b->pppCl[y][x];

      if (c)
        raw[i++] = c->nPV>1  ? empty[0] :
                   c->nPV==0 ? empty[1] :
                               symbols[c->FV];
    }

  raw[i] = '\0';
}

/*//////////////////////////////////////////////////////////// */

int SetBoard (t_board * b,
              const char * str,
              const char * symbols,
              const char * empty)
{
  int x, y, i, j, k;
  t_cell * c;

  if (!symbols || !*symbols)
    symbols = b->nSy<=9 ? "123456789" :
              b->nSy<=30 ? "0123456789ABCDEFHJKLMNPRTUVWYZ" :
              NULL;

  if (!empty || !*empty)
    empty = ".X0";

  if (!b || b->state==skeleton || !symbols)
    return 0;

  CleanBoard (b);

  if (!str || !*str)
    return 0;

  for (y=i=0; y<b->h; y++)
    for (x=0; x<b->w; x++)
    {
      c = b->pppCl[y][x];

      if (!c)
        continue;

      for (;;)
      {
        if (!str[i])
          return 0;

        for (j=0; symbols[j] &&
                  symbols[j]!=str[i]; j++)
          {}

        if (symbols[j])
          break;

        for (k=0; empty[k] &&
                  empty[k]!=str[i]; k++)
          {}

        if (empty[k])
          break;

        i ++;
      }

      if (symbols[j])
        SetSymbolInCell (b, j, c-b->pCl);

      i ++;
    }

  return 1;
}

/*//////////////////////////////////////////////////////////// */

