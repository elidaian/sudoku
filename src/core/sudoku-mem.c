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

    sudoku-mem.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#include "sudoku-pr.h"

/*///////////////////////////////////////////////////////////////// */

t_board *AllocateBoardSkeleton(int nCells,int nGroups,int nSymbols,int Width,int Height,int BlockWidth,int BlockHeight)
{
	int i;
	t_board *b;
	t_group *g;
	void **p,**q;
	char ok;

  b = (t_board*) malloc (sizeof(t_board));             /* Board */

  if (!b)
    return NULL;  /* Failure (not enough free memory) */

  ok = TRUE;
  memset (b, 0L, sizeof(t_board));

  b->state = skeleton;

  b->pInd = (char*) malloc (nSymbols*sizeof(char));

  if (!b->pInd)
    ok = FALSE;

  b->nCl = nCells;
  b->pCl = (t_cell*) malloc (b->nCl*sizeof(t_cell));   /* Cells */

  if (b->pCl)
    memset (b->pCl, 0L, b->nCl*sizeof(t_cell));
  else
    ok = FALSE;

  b->nGr = nGroups;
  b->nSy = nSymbols;
  b->pGr = (t_group*) malloc (b->nGr*sizeof(t_group)); /* Groups */

  if (b->pGr)
    memset (b->pGr, 0L, b->nGr*sizeof(t_group));
  else
    ok = FALSE;

  b->pDirtyGL = (t_list*) malloc (b->nSy*sizeof(t_list));

  if (b->pDirtyGL)
    memset (b->pDirtyGL, 0L, b->nSy*sizeof(t_list));
  else
    ok = FALSE;

  b->w = Width;
  b->h = Height;

  b->wb = BlockWidth;
  b->hb = BlockHeight;

  b->pppCl = (t_cell***)                          /* 2D matrix */
             malloc (b->h*sizeof(t_cell**) +      /* for easy */
                     b->h*b->w*sizeof(t_cell*));  /* printing */
                                                  /* (and fast) */
  if (b->pppCl)
  {                            /* One single block is used */
    p = (void**) b->pppCl;     /* for the array of pointers to */
    q = p + b->h;              /* the rows, and the rows */

    memset (q, 0L, b->h*b->w*sizeof(t_cell*));

    for (i=0; i<b->h; i++, p++, q+=b->w)
      *p = q;
  }
  else
    ok = FALSE;

  for (i=0, g=b->pGr; ok && i<b->nGr; i++, g++) /* Every group has */
  {
    g->ppCl = (t_cell**) malloc (b->nSy*           /* pointers */
                                 sizeof(t_cell*)); /* to its cells */

    if (g->ppCl)
      memset (g->ppCl, 0L, b->nSy*
                           sizeof(t_cell*));
    else
      ok = FALSE;

    g->pmPC = (int*) malloc (b->nSy*         /* a mask with */
                             sizeof(int));   /* possible cells */
                                             /* for every symbol */
    if (g->pmPC)
      memset (g->pmPC, 0L, b->nSy*
                           sizeof(int));
    else
      ok = FALSE;

    g->pnPC = (char*) malloc (b->nSy*        /* a number of */
                              sizeof(char)); /* possible cells */
                                             /* for every symbol */
    if (g->pnPC)
      memset (g->pnPC, 0L, b->nSy*
                           sizeof(char));
    else
      ok = FALSE;
  }

  b->pnGssCl = (short*) malloc (b->nCl*sizeof(short));
  b->pmPGss = (int*) malloc (b->nCl*sizeof(int));

  if (!b->pnGssCl || !b->pmPGss)
    ok = FALSE;

  if (!ok)           /* If something was wrong, roll back */
  {
    if (b->pGr)
      for (i=0, g=b->pGr; i<b->nGr; i++, g++)
      {
        free (g->ppCl);
        free (g->pmPC);
        free (g->pnPC);
      }

    free (b->pInd);
    free (b->pCl);
    free (b->pGr);
    free (b->pDirtyGL);
    free (b->pppCl);
    free (b->pnGssCl);
    free (b->pmPGss);
    free (b);

    return NULL;  /* Failure (not enough free memory) */
  }

  return b;       /* Success */
}

/*///////////////////////////////////////////////////////////////// */

int CompleteBoard (t_board *b)
{
  int cell, group, Igroup, n, ng, i, j, k, m;
  t_cell * c;
  t_group * g;

  if (!b)
    return 0;

  n = b->nSy;

  for (cell=0; cell<b->nCl; cell++)  /* For every cell, fill its */
  {                                  /* array of pointers to the */
    c = b->pCl + cell;               /* groups it belongs to */

    free (c->ppGr);     /* Reset group arrays */
    free (c->pxGr);     /* just in case */
    c->ppGr = NULL;
    c->pxGr = NULL;
    c->nGr = 0;

    for (group=ng=0; group<b->nGr; group++)  /* For every group */
      for (i=0; i<n; i++)
        if (b->pGr[group].ppCl[i]==c)        /* If the cell is */
        {                                    /* in it, count */
          ng ++;                             /* and skip to next */
          break;                             /* group */
        }
           /* Now ng is the number of groups that contain this cell */
           /* Allocate space enough for the array... */

    c->ppGr = (t_group**) malloc (ng*sizeof(t_group*));
    c->pxGr = (char*) malloc (ng*sizeof(char));

    if (!c->ppGr || !c->pxGr)
      return 0;

    for (group=0; group<b->nGr; group++)     /* Repeat search */
      for (i=0; i<n; i++)                    /* and now store */
        if (b->pGr[group].ppCl[i]==c)        /* ptrs. to groups */
        {
          c->ppGr[c->nGr] = b->pGr + group;
          c->pxGr[c->nGr] = i;
          c->nGr ++;
          break;
        }
  }

  for (group=0; group<b->nGr; group++)  /* For every group, reset */
  {                                     /* its arrays of */
    g = b->pGr + group;                 /* intersected groups */

    free (g->ppIGr);    /* Reset arrays */
    free (g->pxIGr);    /* just in case */
    free (g->pmICl);
    free (g->pnICl);
    g->ppIGr = NULL;
    g->pxIGr = NULL;
    g->pmICl = NULL;
    g->pnICl = NULL;
    g->nIGr = 0;
  }

  for (group=0; group<b->nGr; group++)            /* Count */
    for (Igroup=group+1; Igroup<b->nGr; Igroup++) /* intersections */
    {
      for (i=0; i<n; i++)               /* For every pair of groups */
      {                                 /* compare their cells */
        for (j=0; j<n; j++)             /* (don't repeat pairs) */
          if (b->pGr[group].ppCl[i] ==
              b->pGr[Igroup].ppCl[j])   /* If they have one common */
            break;                      /* cell, stop searching: */
                                        /* they intersect */
        if (j<n)                        /* (account this only once) */
          break;
      }

      if (i<n)
      {
        b->pGr[group].nIGr ++;   /* Increase both */
        b->pGr[Igroup].nIGr ++;  /* intersection counters */
      }
    }

  for (group=0; group<b->nGr; group++)  /* For every group, */
  {                                     /* allocate arrays of */
    g = b->pGr + group;                 /* intersected groups */

    if (!g->nIGr)
      continue;
          
    g->ppIGr = (t_group**) malloc (g->nIGr*sizeof(t_group*));
    g->pxIGr = (char*) malloc (g->nIGr*sizeof(char));
    g->pmICl = (int*) malloc (g->nIGr*sizeof(int));
    g->pnICl = (char*) malloc (g->nIGr*sizeof(char));

    if (!g->ppIGr || !g->pxIGr || !g->pmICl || !g->pnICl)
      return 0;

    memset (g->ppIGr, 0L, g->nIGr*sizeof(t_group*));
    memset (g->pxIGr, 0L, g->nIGr*sizeof(char));
    memset (g->pmICl, 0L, g->nIGr*sizeof(int));
    memset (g->pnICl, 0L, g->nIGr*sizeof(char));
  }

  b->maxICl = 0;   /* Reset max num of involved cells */

  for (group=0, g=b->pGr;      /* For every group */
       group<b->nGr;           /* k: index {0..nIGr-1} */
       group++, g++)           /* m: flag "intersection found, */
                               /*          so increase k" */
    for (Igroup=k=0;           /* Search all its */
         Igroup<b->nGr;        /* intersections */
         Igroup++)             /* (repeat pairs) */
    {
      if (group==Igroup)       /* (don't test any */
        continue;              /* group with itself) */

      for (i=m=0; i<n; i++)            /* Search common cells */
        for (j=0; j<n; j++)            /* Account only in the */
          if (g->ppCl[i] ==            /* first group of the */
              b->pGr[Igroup].ppCl[j])  /* pair */
          {
            g->ppIGr[k] = b->pGr + Igroup; /* (may be repeated) */
            g->pmICl[k] |= 1 << i;         /* Raise cell bit */
            g->pnICl[k] ++;                /* Count cells */

            m = 1;  /* Raise flag "k will have to be increased */
          }         /*             before passing to the next */
                    /*             Igroup because the current */
                    /*             Igroup intersects with group" */

      if (m)
      {                             /* Remember the max number */
        if (g->pnICl[k]>b->maxICl)  /* of cells involved in an */
          b->maxICl = g->pnICl[k];  /* intersection */

        k ++;       /* Next intersection... */
      }
    }

  for (group=0; group<b->nGr; group++)  /* For every group, fill */
  {                                     /* its cross ref. index */
    g = b->pGr + group;                 /* That is, the pos. it */
                                         /* has in the inters. */
    for (i=0; i<g->nIGr; i++)             /* arrays of other */
      for (j=0; j<g->ppIGr[i]->nIGr; j++)  /* groups */
        if (g->ppIGr[i]->ppIGr[j]==g)
        {
          g->pxIGr[i] = j;
          break;
        }
  }
                                        /* Maximum dirty level */
  b->maxLevel = b->maxICl > b->nSy/2 ?  /* for groups (num. of */
                b->maxICl : b->nSy/2;   /* dirty group lists) */

  b->state = unsolved;    /* Initial state */
  CleanBoard (b);         /* Clean it for the first time */
  return 1;               /* Success */
}

/*///////////////////////////////////////////////////////////////// */

void CleanBoard (t_board * b)
{
  int i, j;
  t_cell * c;
  t_group * g;

  if (!b || b->state==skeleton)
    return;

  b->nSol = 0;                   /* No solved cells */
  b->state = unsolved;           /* Initial state */
  b->errmSy = 0;                 /* No error symbols */
  b->errmCl = 0;                 /* No error cells */
  b->errGr = -1;                 /* No error group */
  b->nGss = 0;                   /* No guessings */
  b->nGssTotal = 0;

  b->nRulesN1 = 0;
  b->nRulesN2 = 0;               /* Reset dificulty */
  b->nRulesNGt2 = 0;             /* counters */

  ListReset (&b->CleanCL);       /* Reset every list */
  ListReset (&b->DirtyCL);
  ListReset (&b->CleanGL);

  for (i=0; i<b->nSy; i++)
    ListReset (b->pDirtyGL+i);

  for (i=0, c=b->pCl; i<b->nCl; i++, c++) /* For every cell */
  {
        /* State of solution: */

    c->mPV = ~ (~0UL << b->nSy); /* All values are possible */
    c->nPV = b->nSy;

    c->FV = -1;       /* Final value: undefined */
    c->nSolPos = -1;  /* No solve order (still unsolved) */

        /* State during solving progress: */

    c->flags = 0;     /* Not dirty, not solved */
    c->mRPV = 0;      /* No removed possition values */

    ListAppend (&b->CleanCL, &c->lnode);  /* Clean cells list */
  }

  for (i=0, g=b->pGr; i<b->nGr; i++, g++)
  {
        /* State of solution: */

    for (j=0; j<b->nSy; j++)
    {
      g->pmPC[j] = ~ (~0UL << b->nSy); /* All cells are possible */
      g->pnPC[j] = b->nSy;
    }

        /* State during solving progress: */

    g->flags = 0;    /* Not dirty, not solved */
    g->mDirtyCl = 0; /* No dirty cells */
    g->mDirtySy = 0; /* No dirty symbols */

    ListAppend (&b->CleanGL, &g->lnode);  /* Clean groups list */
  }
}

/*///////////////////////////////////////////////////////////////// */

void DestroyBoard (t_board * b)
{
  int i;
  t_group * g;

  if (!b)
    return;
                                  /* Just free everything */
  if (b->pCl)                     /* carefully (any subset */
    for (i=0; i<b->nCl; i++)      /* of pointers might be NULL) */
    {
      free (b->pCl[i].ppGr);
      free (b->pCl[i].pxGr);
    }

  if (b->pGr)
    for (i=0, g=b->pGr; i<b->nGr; i++, g++)
    {
      free (g->ppCl);

      free (g->pmPC);
      free (g->pnPC);

      free (g->ppIGr);
      free (g->pxIGr);
      free (g->pmICl);
      free (g->pnICl);
    }

  free (b->pInd);
  free (b->pCl);
  free (b->pGr);
  free (b->pppCl);
  free (b->pDirtyGL);
  free (b->pnGssCl);
  free (b->pmPGss);

  free (b);
}

/*///////////////////////////////////////////////////////////////// */
