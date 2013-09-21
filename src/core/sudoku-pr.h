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

    sudoku-pr.h
*/

#ifndef _SUDOKU_PRIVATE_H_
#define _SUDOKU_PRIVATE_H_

#include "sudoku-pub.h"
#include "list.h"

#define DIRTY_FLAG    1
#define SOLVED_FLAG   2
#define GUESSED_FLAG  4

typedef struct s_cell * t_cell_p;
typedef struct s_group * t_group_p;

/*typedef enum e_e_state e_state;*/

/*/////////////////////////// */

typedef struct s_cell
{
  /* Topology: */

  char x, y;        /* Coordinates (just for printing) */

  t_group_p * ppGr; /* Groups it belongs to */
  char nGr;         /* Num. of groups it belongs to */
  char * pxGr;      /* Cross reference indexes */

  /* State of solution: */

  int mPV;          /* Mask with possible values */
  char nPV;         /* Num. of possible values (redundant) */
  char FV;          /* Final value (only valid when nPV==1) */
  short nSolPos;    /* Position in solving order */
  short nGss;       /* Num. of guessings when solved */

  /* State during solving progress: */

  char flags;       /* State of the cell */
  int mRPV;         /* Mask of removed poss. values (0 when clean) */
  t_lnode lnode;    /* Node in the clean/dirty cells list */
}
t_cell;

/*/////////////////////////// */

typedef struct s_group
{
  /* Topology: */

  char type;        /* Row, column, block.. (user defined) */

  t_cell ** ppCl;   /* Cells in the group (one per symbol) */
  char nCl;         /* Num. of cells (used only while construction) */

  t_group_p * ppIGr;   /* Intersected groups */
  char nIGr;           /* Num. of intersected groups */
  char * pxIGr;        /* Cross reference indexes */
  int * pmICl;         /* Masks indicating involved cells */
  char * pnICl;        /* Nums. of involved cells */

  /* State of solution: */

  int * pmPC;       /* Masks with possible cells for the values */
  char * pnPC;      /* Nums. of possible cells (redundant) */
  int mDirtyCl;     /* Mask with dirty cells of the group */
  int mDirtySy;     /* Mask with dirty symbols of the group */

  /* State during solving progress: */

  char flags;       /* State of the group */
  t_lnode lnode;    /* Node in the clean/dirty groups list */
  char level;       /* Dirty level */
}
t_group;

/*/////////////////////////// */

typedef struct s_board
{
  /* Topology: */

  t_cell * pCl;     /* Cells (1D array of cells) */
  short nCl;        /* Number of cells */

  t_group * pGr;    /* Groups */
  short nGr;        /* Num. of groups */
  char nSy;         /* Num. of symbols (== size of every group) */
  char maxICl;      /* Max. num. of cells in a group intersection */

  short w, h;       /* Size (width and height for printing) */
  char wb, hb;      /* Size of blocks for printing */
  t_cell *** pppCl; /* Cells (2D array of _pointers_ to cells) */

  /* State of solution: */

  e_state state;    /* skeleton, unsolved, impossible, solved */
  short nSol;       /* Num. of solved cells */
  short errmSy;     /* Symbols with too few/many possible cells */
  short errmCl;     /* Cells with too few/many possible symbols */
  short errGr;      /* Group with error */

  /* State during solving progress: */

  t_list CleanCL;   /* Clean cells list */
  t_list DirtyCL;   /* Dirty cells list */

  t_list CleanGL;   /* Clean groups list */
  t_list * pDirtyGL;/* Dirty groups lists (as many as symbols) */
  char maxLevel;    /* Number of lists used */

  char * pInd;      /* Index array used in ProcessDirtyGroup() */

  short * pnGssCl;  /* Stack of guessed cells */
  int * pmPGss;     /* Stack of masks with values pending to try */
  int nGss;         /* Num. of guessed cells (top of the stack) */
  int nGssTotal;    /* Num. of guess op. (count failures too) */

  char ruleLevel;   /* Level of last rule applied */
  e_rule ruleType;  /* Type of last rule applied */
  short ruleGr;     /* Group of last rule applied */
  short ruleIGr;    /* Intersected group of last rule applied */
  int rulemSy;      /* Involved symbols in last rule applied */
  int rulemCl;      /* Involved cells in last rule applied */

  short nRulesN1;   /* Number of rules with N=1 */
  short nRulesN2;   /* Number of rules with N=2 */
  short nRulesNGt2; /* Number of rules with N>2 */
}
t_board;

/*/////////////////////////// */

#endif
