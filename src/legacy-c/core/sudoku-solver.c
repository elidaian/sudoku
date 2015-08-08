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

    sudoku-solver.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

#include "sudoku-pr.h"

#ifdef INLINE
#undef INLINE
#endif
#define INLINE

/*///////////////////////////////////////////////////////////////// */

static INLINE int ProcessDirtyCell (t_board * b);
static INLINE int ProcessDirtyGroup (t_board * b);

static INLINE void RemovePossibleValuesFromCell (t_board * b,
                                                 t_cell * c,
                                                 int m);

static INLINE void SearchCandidateCellForGuessing (t_board * b);
static INLINE void TakeNextUnexploredGuess (t_board * b);
static INLINE void RewindGuess (t_board * b);
static INLINE void RecoverPrevStateForGuessing (t_board * b);

/*///////////////////////////////////////////////////////////////// */

int Solve (t_board * b,    /* Puzzle to solve */

           char traplevel, /* 0 == never stop */
                           /* N == stop after first N-level rule */

           char bguess)    /* TRUE  == "guess if needed" */
{                          /* FALSE == "do not guess" */

  if (!b || b->state!=unsolved)
    return 0;                    /* State should be unsolved */

  b->ruleLevel = 0;              /* Reset rule level */

  for (;;)    /* Guessing loop (try solving first, then guess) */
  {
                  /* Solving loop (repeat until solved, */
    do            /*               or impossible or dead point) */
    {
      if (ListGetNum(&b->DirtyCL))        /* Process cells first */
      {
        if (!ProcessDirtyCell(b))         /* If a solution is */
          break;                          /* reached or there's */
      }                                   /* no sol., then stop */
 
      else if (ListGetNum(&b->CleanGL)!=b->nGr)   /* Then groups */
      {
        if (!ProcessDirtyGroup(b))        /* If there's no */
          break;                          /* possible cell for */
                                          /* a value... no sol. */
        if (traplevel>0 &&
            b->ruleLevel>=traplevel)      /* If trap "flag" says */
          return b->nGss;                 /* so, stop */
      }

      else                                /* Nothing more to do.. */
        break;                            /* ...remain unsolved */
    }
    while (b->state!=solved);      /* If solved... success! */


    if (b->state==solved ||        /* Solved...               end */
        !bguess ||                 /* Guess forbidden...      end */
        (b->state==impossible &&   /* Impossible, even */
         b->nGss==0))              /*      before guessing... end */

      return b->nGss;


    if (b->state==impossible)      /* If there's no solution */
    {                              /* after a guess has been */
      RewindGuess (b);             /* made, go back to try */
                                   /* other option(s) */
      if (b->nGss==0)
        return b->nGss;            /* No options remain...    end */

      RecoverPrevStateForGuessing (b);  /* Remove effects of */
                                        /* the wrong guess */
    }
                                   /* If there _might_ be a sol. */
    else  /* state==unsolved          search what to guess */

      SearchCandidateCellForGuessing (b);


    TakeNextUnexploredGuess (b);  /* Finally, guess */

    if (traplevel>0)       /* Guessing happens only when proper */
    {                      /* rules give no clue, so it is */
      b->ruleType = guess; /* somehow a "top" level rule */
      b->ruleLevel = -1;
      return b->nGss;
    }
  }
}

static INLINE int ProcessDirtyCell (t_board * b)
{
  int i, j, val, dirty;
  t_cell * c;
  t_group * g;
  t_lnode * node;

  node = ListGetFirst (&b->DirtyCL);      /* Take the first */
  c = GET_ELEM (t_cell, node, lnode);     /* dirty cell */

  ListExtract (&b->DirtyCL, &c->lnode);
  ListAppend (&b->CleanCL, &c->lnode);    /* Move it to the clean */
                                          /* cells list and */
  c->flags &= ~ DIRTY_FLAG;               /* mark it clean */

  if (c->nPV==0)  /* If there's no possible value at all */
  {
    b->errGr = c->ppGr[0] - b->pGr; /* Save error information */
    b->errmCl = 1 << c->pxGr[0];    /* and give up :-( */
    b->errmSy = 0;
    b->state = impossible;          
    return 0;
  }
                                  /* If there's only one */
  if (c->nPV==1 &&                /* possible value... */
      !(c->flags & SOLVED_FLAG))  /* (do this only once) */
  {
    c->flags |= SOLVED_FLAG; /* This cell is solved */

    c->nSolPos = b->nSol;    /* Save pos. in solving order */
    c->nGss = b->nGss;       /* Save num. of prev. guessings */
    b->nSol ++;              /* Count solved cells */

    if (b->nSol==b->nCl)     /* If all cells are solved... */
    {
      b->state = solved;
      return 0;              /* Happy end! */
    }
  }

  for (i=0; i<c->nGr; i++)   /* For every group where this */
  {                          /* cell is in... */
    g = c->ppGr[i];
    j = c->pxGr[i];    /* Cell's index inside the group */

    for (val=dirty=0; val<b->nSy; val++)  /* Now remove the cell */
      if (((1<<val) & c->mRPV) &&         /* from the masks of the */
          ((1<<j) & g->pmPC[val]))        /* removed possible */
      {                                   /* values */
        g->pmPC[val] &= ~ (1<<j);
        g->pnPC[val] --;
        g->mDirtySy |= 1 << val;

        dirty = 1;       /* Bits channged, so raise the flag */
      }

    if (dirty)
    {
      g->mDirtyCl |= 1 << j;
                                                /* If any bit */
      if (!(g->flags & DIRTY_FLAG) || g->level) /* changed, mark */
      {                                         /* the group dirty */
        ListExtract ((g->flags & DIRTY_FLAG) ?  /* and move it to */
                     &b->pDirtyGL[g->level] :   /* the first dirty */
                     &b->CleanGL,               /* queue (unless */
                     &g->lnode);                /* it is already */
                                                /* there, of */
        ListAppend (b->pDirtyGL, &g->lnode);    /* course) */

        g->level = 0;
        g->flags |= DIRTY_FLAG;
      }
    }
  }

  c->mRPV = 0;   /* Clear the removed bits */

  return 1;
}

static INLINE int ProcessDirtyGroup (t_board * b)
{
  int i, j, k, m, n, o, p, mc, ms;
  char level, sy, N, dirty;
  char * pInd;
  t_group * g, * Ig;
  t_cell * c;
  t_lnode * node;

  for (level=0; level<b->nSy; level++)  /* Search for the lowest */
    if (ListGetNum(b->pDirtyGL+level))  /* dirty groups list */
      break;                            /* containing groups */

  node = ListGetFirst (&b->pDirtyGL[level]);  /* Take the first */
  g = GET_ELEM (t_group, node, lnode);        /* dirty group */

  b->ruleLevel = level + 1;
  b->ruleGr = g - b->pGr;
  b->ruleIGr = -1;
  b->rulemSy = 0;


  /* ------------------ FIRST RULE ------------------ */
  /* */
  /* Part A: */
  /*   N symbols are possible in only N cells, so */
  /*   no other symbol can be possible in these cells */
  /* */
  /* Part B: */
  /*   N cells have only a set of N different possible */
  /*   symbols, so these are impossible in other cells */


  N = level + 1;   /* Just store these values in local vars */
  pInd = b->pInd;  /* so that the code bellow is more readable */

  dirty = 0;

  /* Part A: (N symbols appear in only N cells..) */

  if (level<b->nSy/2 && g->mDirtySy)
  {
    b->ruleType = symbols;

    for (i=n=0; i<b->nSy; i++)      /* Count the number of symbols */
      if (g->pnPC[i]<=N &&          /* that can appear in N (or */
          ((1<<i) & g->mDirtySy) && /* less) different cells of */
          (N==1 || g->pnPC[i]>1))   /* the group and make an index */
      {
        pInd[n] = i;
        n ++;                     /* Take first the symbols that */
      }                           /* have been recently declared */
                                  /* impossible in dirty cells */
    for (i=0, p=n; i<b->nSy; i++) /* (dirty symbols) */
      if (g->pnPC[i]<=N &&
          !((1<<i) & g->mDirtySy) &&
          g->pnPC[i]>1)
      {
        pInd[n] = i;              /* (p: number of dirty symbols) */
        n ++;
      }

    if (n>=N)         /* If there are at least N such symbols */
    {
      m = 1;      /* (m: mask with subset of symbol indexes) */
      o = 1;      /* (o: number of ones in m) */
      k = 0;      /* (k: position in the mask == MSB) */

      for (;;)
      {
        for (i=mc=0; i<n; i++)       /* (mc: mask indicating */
          if (m & (1<<i))            /*      subset of cells of */
            mc |= g->pmPC[pInd[i]];  /*      the group where the */
                                     /*      symbols are possible) */
        for (j=0, i=mc; i; i>>=1)
          if (i & 1)                 /* (j: number of cells) */
            j ++;
                           /* N symbols that can appear in */
        if (o==N && j<=N)  /* only N (or less) cells... */
        {
          for (i=ms=0; i<n; i++)     /* (ms: mask with N symbols) */
            if (m & (1<<i))
              ms |= 1 << pInd[i];

          if (j<N)                   /* If N symbols can only be */
          {                          /* in _less_ than N cells, */
            b->errGr = g - b->pGr;   /* at least one of them */
            b->errmCl = mc;          /* can't be anywhere */
            b->errmSy = ms;       
            b->state = impossible;   /* There's no solution */
            return 0;                /* Stop solving */
          }
          else
          {                          /* These N symbols will fill */
            for (i=0; i<b->nSy; i++) /* the N cells, so no other */
            {                        /* symbol will be possible */
              c = g->ppCl[i];        /* in these cells */

              if (((1<<i) & mc)  &&    /* If the possible symbols */
                  (~ms & c->mPV)    )  /* mask of the cell */
              {                        /* includes other symbols */

                RemovePossibleValuesFromCell (b, c, ~ms);

                if (c->nPV==0)         /* No possible symbol... */
                {
                  b->errGr = g - b->pGr;
                  b->errmCl = 1 << i;
                  b->errmSy = 0;
                  b->state = impossible; /* There's no solution */
                  return 0;              /* Stop solving */
                }

                dirty = 1;
              }
            }
          }

          if (dirty)    /* If there are dirty cells now, */
          {
            g->mDirtySy &= ~ ms;

            b->rulemSy = ms;   /* Store symbols mask and */
            b->rulemCl = mc;   /* cells mask for the user */

            switch (N)
            {                                    /* Count number of */
              case 1:  b->nRulesN1 ++;   break;  /* rules applied */
              case 2:  b->nRulesN2 ++;   break;
              default: b->nRulesNGt2 ++;
            }

            return 1;   /* process dirty cells before going on */
          }             /* with groups */
        }
                                   /* Next subset: */
        if (o==N || j>N || k==n-1) /* If there are already N */
        {                          /* symbols, or they might be */
          m &= ~ (1<<k);           /* in more than N cells, or the */
          o --;                    /* last added is the last we */
                                   /* have... remove it */
          if (k==n-1)                 
          {                        /* If there are not more... */
            if (!o)
              break;               /* Empty hands... end */

            do k--; while (!(m & (1<<k))); /* Go back to the */
                                           /* previous symbol */
            m &= ~ (1<<k);                 /* and remove it */
            o --;
          }
        }
                      /* Move left and add the next symbol */
        k ++;
        m |= 1 << k;  /* Don't wait to have N symbols: go up */
        o ++;         /* and count the cells... (it saves time) */

        if (!(m & ((1<<p)-1)) ||     /* If there's no hope to have */
            !(m & ((1<<(n-N+1))-1))) /* a subset of N symbols with */
          break;                     /* at least one dirty symbol, */
      }                              /* stop */
    }
  }

    /* Part B (N cells can only have N symbols..) */

  if (level<b->nSy/2 && g->mDirtyCl)
  {
    b->ruleType = cells;

    for (i=n=0; i<b->nSy; i++)      /* Count the number of cells */
      if (g->ppCl[i]->nPV<=N &&     /* of the group where N (or */
          ((1<<i) & g->mDirtyCl) && /* less) different symbols */
          (N==1 ||                  /* can be and make an index */
           g->ppCl[i]->nPV>1))
      {
        pInd[n] = i;
        n ++;
      }                           /* Take first the cells that */
                                  /* have heen dirty since last */
    for (i=0, p=n; i<b->nSy; i++) /* visit to this group */
      if (g->ppCl[i]->nPV<=N &&
          !((1<<i) & g->mDirtyCl) &&
          g->ppCl[i]->nPV>1)
      {
        pInd[n] = i;
        n ++;
      }

    if (n>=N)         /* If there are at least N such cells... */
    {
      m = 1;      /* (m: mask with subset of cell indexes) */
      o = 1;      /* (o: number of ones in m) */
      k = 0;      /* (k: position in the mask == MSB) */

      for (;;)
      {
        for (i=ms=0; i<n; i++)       /* (ms: mask indicating */
          if (m & (1<<i))            /*      subset of symbols */
            ms |= g->                /*      possible in the */
                 ppCl[pInd[i]]->mPV; /*      chosen cells) */

        for (j=0, i=ms; i; i>>=1)
          if (i & 1)                 /* (j: number of symbols) */
            j ++;
                             /* N cells that can have only N */
        if (o==N && j<=N)    /* (or less) different symbols... */
        {
          for (i=mc=0; i<n; i++)     /* (ms: mask with N cells) */
            if (m & (1<<i))
              mc |= 1 << pInd[i];

          if (j<N)                   /* If the number of possible */
          {                          /* symbols in N cells is */
            b->errGr = g - b->pGr;   /* _less_ than N, some cell */
            b->errmCl = mc;          /* can't have any symbol */
            b->errmSy = ms;       
            b->state = impossible;   /* There's no solution */
            return 0;                /* Stop solving */
          }
          else
          {                          /* These N symbols will fill */
            for (i=0; i<b->nSy; i++) /* the N cells, so they will */
            {                        /* not be possible in any */
              c = g->ppCl[i];        /* other cells of the group */

              if (!((1<<i) & mc) &&    /* If the possible symbols */
                  (ms & c->mPV)     )  /* mask of the cell */
              {                        /* includes any one of */
                                       /* these N symbols */

                RemovePossibleValuesFromCell (b, c, ms);

                if (c->nPV==0)         /* No possible symbol... */
                {
                  b->errGr = g - b->pGr;
                  b->errmCl = 1 << i;
                  b->errmSy = 0;
                  b->state = impossible; /* There's no solution */
                  return 0;              /* Stop solving */
                }

                dirty = 1;
              }
            }
          }

          if (dirty)    /* If there are dirty cells now, */
          {
            g->mDirtyCl &= ~ mc;

            b->rulemSy = ms;   /* Store symbols mask and */
            b->rulemCl = mc;   /* cells mask for the user */

            switch (N)
            {                                    /* Count number of */
              case 1:  b->nRulesN1 ++;   break;  /* rules applied */
              case 2:  b->nRulesN2 ++;   break;
              default: b->nRulesNGt2 ++;
            }

            return 1;   /* process dirty cells before going on */
          }             /* with groups */
        }
                                   /* Next subset: */
        if (o==N || j>N || k==n-1) /* If there are already N */
        {                          /* cells, or they might have */
          m &= ~ (1<<k);           /* more than N symbols, or the */
          o --;                    /* last added is the last we */
                                   /* have... remove it */
          if (k==n-1)
          {                        /* If there are not more... */
            if (!o)
              break;               /* Empty hands... end */

            do k--; while (!(m & (1<<k))); /* Go back to the */
                                           /* previous cell */
            m &= ~ (1<<k);                 /* and remove it */
            o --;
          }
        }
                      /* Move left and add the next cell */
        k ++;
        m |= 1 << k;  /* Don't wait to have N cells: go up */
        o ++;         /* and count the symbols... (it saves time) */

        if (!(m & ((1<<p)-1)) ||     /* If there's no hope to have */
            !(m & ((1<<(n-N+1))-1))) /* a subset of N cells with */
          break;                     /* at least one dirty cell, */
      }                              /* stop */
    }
  }


  /* ------------------ SECOND RULE ------------------ */
  /* */
  /*   A symbol is only possible N cells, and they all */
  /*   belong to the intersection with another group, */
  /*   so it will not appear anywhere else in that */
  /*   other group */


  b->ruleType = inters;
                         /* Check only sets of cells that can be */
  if (level<b->maxICl && /* all involved in the same intersection */
      level>0)           /* Case N==1 will be detected by rule 1 */

                                 /* For every symbol that */
    for (sy=0; sy<b->nSy; sy++)  /* can be in exactly */
      if (g->pnPC[sy]==level+1)  /* level+1 cells in g... */

        for (i=0; i<g->nIGr; i++)  /* For every intersected group */
          if ((~g->pmICl[i] &      /* if all those cells of g are */
               g->pmPC[sy]   )==0) /* involved, then the symbol */
          {                        /* can not appear anywhere */
            Ig = g->ppIGr[i];      /* else in the intersected */
            j = g->pxIGr[i];       /* but in those involved cells */

            if (~Ig->pmICl[j] &         /* So, if it's */
                Ig->pmPC[sy]   )        /* marked possible... */
            {
              for (k=mc=0; k<b->nSy; k++)         /* For those */
                if ( (Ig->pmPC[sy] & (1<<k)) &&   /* cells not */
                    !(Ig->pmICl[j] & (1<<k))   )  /* involved... */
                {
                  c = Ig->ppCl[k];

                  if (c->mPV & (1<<sy))   /* If the cell has that */
                  {                       /* symbol as possible.. */

                    RemovePossibleValuesFromCell (b, c, 1<<sy);

                    mc = 1 << k;

                    if (c->nPV==0)         /* No possible symbol */
                    {
                      b->errGr = Ig - b->pGr;
                      b->errmCl = 1 << k;
                      b->errmSy = 0;
                      b->state = impossible; /* There's no sol. */
                      return 0;              /* Stop solving */
                    }
                  }
                }

              if (!Ig->pmPC[sy])             /* If the symbol is */
              {                              /* impossible now in */
                b->errGr = Ig - b->pGr;      /* the group Ig, */
                b->errmCl = 0;               /* stop */
                b->errmSy = 0;
                b->state = impossible; /* There's no solution */
                return 0;              /* Stop solving */
              }

              switch (N)
              {                                   /* Count number */
                case 1:  b->nRulesN1 ++;   break; /* of rules */
                case 2:  b->nRulesN2 ++;   break; /* applied */
                default: b->nRulesNGt2 ++;
              }
                                        /* Store rule information */
              b->ruleIGr = Ig - b->pGr; /* for the user: masks */
              b->rulemSy = 1 << sy;     /* and intersected group */
              b->rulemCl = mc;          /* (mc refers to it) */

              return 1;   /* Go out (there are dirty cells now..) */
            }
          }


  /* ------------ NO MORE RULES */
                                        /* Nothing changed, so */
                                        /* the group is "clean" */
  ListExtract (b->pDirtyGL+level,       /* (at this level) */
               &g->lnode);
                                        /* Extract it from this */
  g->level ++;                          /* dirty groups list */
                                        /* and append it to the */
  if (g->level<b->maxLevel)             /* next level list, or */
    ListAppend (b->pDirtyGL+g->level,   /* the clean groups list */
                &g->lnode);
  else
  {
    ListAppend (&b->CleanGL, &g->lnode);
    g->flags &= ~ DIRTY_FLAG;
    g->mDirtyCl = 0;
    g->mDirtySy = 0;
  }

  b->ruleLevel = 0;  /* Rules had no effects */

  return 1;
}

static INLINE void RemovePossibleValuesFromCell (t_board * b,
                                                 t_cell * c,
                                                 int m)
{
  int i, n, sy;

  c->mRPV |= m & c->mPV;         /* Backup ones to be removed */
  c->mPV &= ~m;                  /* and then remove them */

  for (i=n=0, sy=-1; i<b->nSy; i++)
    if (c->mPV & (1<<i))
    {
      n ++;        /* Count remaining possible values */
      sy = i;      /* and remember one of them */
    }

  c->nPV = n;

  if (n==1)        /* If only one symbol is possible now, */
    c->FV = sy;    /* save it */

  if ( ! (c->flags & DIRTY_FLAG)) /* If the cell */
  {                               /* is clean, */
    ListExtract (&b->CleanCL,     /* move it to */
                 &c->lnode);      /* the dirty */
                                  /* cells list */
    ListInsert (&b->DirtyCL,
                &c->lnode);

    c->flags |= DIRTY_FLAG;
  }
}

static INLINE void SearchCandidateCellForGuessing (t_board * b)
{
  char min;
  t_cell * c, * cand;

  for (c=cand=b->pCl, min=b->nSy+1; c<b->pCl+b->nCl; c++)
    if (c->nPV==2)
    {                          /* Search for the cell with less */
      cand = c;                /* possible values above 1 */
      break;                   /* (2 PV is perfect) */
    }
    else if (c->nPV>1 && c->nPV<min)
    {
      cand = c;
      min = c->nPV;
    }

  cand->flags |= GUESSED_FLAG;   /* Mark the chosen cell guessed */

  b->pnGssCl[b->nGss] = cand - b->pCl; /* Cell number */
  b->pmPGss[b->nGss] = cand->mPV;      /* Possible values to */
                                       /* explore */
  b->nGss ++;    /* Push */
}

static INLINE void TakeNextUnexploredGuess (t_board * b)
{
  int i;
  t_cell * c;

  for (i=0; i<b->nSy; i++)              /* Search for the next */
    if (b->pmPGss[b->nGss-1] & (1<<i))  /* value to guess */
      break;
                                        /* Remove it from the */
  b->pmPGss[b->nGss-1] &= ~ (1<<i);     /* pending values mask */

  c = b->pCl + b->pnGssCl[b->nGss-1];   /* Take the cell, and */
                                         /* guess the chosen */
  RemovePossibleValuesFromCell (b, c,     /* value (remove the */
                                ~(1<<i));  /* rest of values) */

  b->nGssTotal ++;
}

static INLINE void RewindGuess (t_board * b)
{
  t_cell * c;
                                  /* Go back through last guess */
  while (b->nGss>0 &&             /* operations searching for an */
         !b->pmPGss[b->nGss-1])   /* unexplored option */
  {
    b->nGss --;                        /* Pop last guess */

    c = b->pCl + b->pnGssCl[b->nGss];  /* Remvove the guessed */
    c->flags &= ~ GUESSED_FLAG;        /* mark from the cell */
  }
}

static INLINE void RecoverPrevStateForGuessing (t_board * b)
{
  int i, n, mv;
  t_cell * c, * gc;
  t_group * g;

  n = b->nSy;           /* Number of symbols */
  mv = ~ (~0UL << n);   /* Mask with all of them */

  gc = b->pCl + b->pnGssCl[b->nGss-1];  /* Current guessed cell */

  b->state = unsolved;  /* Restore state */

  for (c=b->pCl; c<b->pCl+b->nCl; c++)  /* For every cell */
  {
    c->mPV = mv;                    /* First, add all symbols */
    c->nPV = n;                     /* as possible values */
    c->mRPV = 0;

    if (c!=gc &&                /* For all the cells guessed */
        (c->flags &             /* or solved _before_ current */
         SOLVED_FLAG) &&        /* guess, set their original */
        ((c->flags &            /* value, marking them dirty */
          GUESSED_FLAG) ||      
         c->nGss<b->nGss))    

      RemovePossibleValuesFromCell (b, c, ~(1<<c->FV));

    else if (c->flags & SOLVED_FLAG)
    {
      c->flags &= ~ SOLVED_FLAG;
      b->nSol --;
    }
  }

  for (g=b->pGr; g<b->pGr+b->nGr; g++)  /* For every group */
    for (i=0; i<n; i++)                 /* and every value */
    {
      g->pmPC[i] = mv;    /* Mark all the cells of the group */
      g->pnPC[i] = n;     /* as possible */

      g->mDirtyCl = 0;
      g->mDirtySy = 0;
    }
}
