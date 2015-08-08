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

    sudoku-pub.h
*/

#ifndef _SUDOKU_PUBLIC_H_
#define _SUDOKU_PUBLIC_H_

#include <stdio.h>

/*/////////////////////////////////////////////////////////////// */

#define TRUE   1
#define FALSE  0

typedef struct s_board * t_board_p;

typedef enum e_e_state  /* Possible states for a sudoku board */
{
  skeleton,    /* Still under construction */
  unsolved,    /* No solution has been found */
  impossible,  /* There is no solution at all */
  solved       /* A solution has been found (if no guess has been */
}              /*                            made, it is unique; */
e_state;       /*                            otherwise who knows) */

typedef enum   /* Types of logical rules */
{              /* For every group (row, column or block)... */

            /* FIRST RULE (part A): */
  symbols,  /* N symbols are possible in only N cells, so */
            /* no other symbol can be possible in these cells */

            /* FIRST RULE (part B): */
  cells,    /* N cells have only a set of N different possible */
            /* symbols, so these are impossible in other cells */

            /* SECOND RULE: */
  inters,   /* A symbol is only possible in N cells, and they */
            /* all belong to the intersection with another */
            /* group, so it will not appear anywhere else in */
            /* that other group */

  guess,    /* A guess has been made (this is no proper rule) */

  norule    /* No rule could be applied */
}
e_rule;


#ifdef __cplusplus
extern "C" {
#endif

/*/////////////////////////////////////////////////////////////// */
/* sudoku-mem.c */
/* Construct, complete, reset, destruct */
/*/////////////////////////////////////////////////////////////// */

t_board_p AllocateBoardSkeleton (int nCells,
                                 int nGroups,
                                 int nSymbols,
                                 int Width,
                                 int Height,
                                 int BlockWidth,
                                 int BlockHeight);

int CompleteBoard (t_board_p b);

void CleanBoard (t_board_p b);

void DestroyBoard (t_board_p b);

/*/////////////////////////////////////////////////////////////// */
/* sudoku-iface.c */
/* Trivial functions to access data */
/*/////////////////////////////////////////////////////////////// */

void PrintGPL (FILE * pf);

/* Cell data */

int GetNumCells (t_board_p b);

int GetCellY (t_board_p b, int cell);
int GetCellX (t_board_p b, int cell);
int GetCellNumber (t_board_p b, int x, int y);
int CellWasChangedByLastRule (t_board_p b, int cell);

int GetNumPossValuesOfCell (t_board_p b, int cell);
int GetPossValuesOfCell (t_board_p b, int cell);
int GetLastRemovedPossValuesOfCell (t_board_p b, int cell);
int GetSymbolOfCell (t_board_p b, int cell);

void RemovePossValuesFromCell (t_board_p b,
                               int mask,
                               int cell);

int SetSymbolInCell (t_board_p b,
                     int val,
                     int cell);

int GetLastNCellsSolved (t_board_p b,
                         int num,
                         int * cells);

int GetNumGroupsOfCell (t_board_p b, int cell);
int GetGroupOfCell (t_board_p b, int group, int cell);

/* Group data */

int GetNumGroups (t_board_p b);
int GetCellOfGroup (t_board_p b, int cell, int group);
int GetGroupType (t_board_p b, int group);

/* Board data */

e_state GetState (t_board_p b);
int GetNumSolvedCells (t_board_p b);
int GetNumSymbols (t_board_p b);

int GetErrSymbolMask (t_board_p b);
int GetErrCellMask (t_board_p b);
int GetErrGroup (t_board_p b);

int GetNumGuessedCells (t_board_p b);
int GetTotalGuessings (t_board_p b);
int GetGuessedCell (t_board_p b, int cell);

int GetLastRuleLevel (t_board_p b);
e_rule GetLastRuleType (t_board_p b);
int GetLastRuleGroup (t_board_p b);
int GetLastRuleIntersectedGroup (t_board_p b);
int GetLastRuleCellsMask (t_board_p b);
int GetLastRuleSymbolsMask (t_board_p b);

int GetNumRulesN1 (t_board_p b);
int GetNumRulesNGt1 (t_board_p b);
int GetNumRulesN2 (t_board_p b);
int GetNumRulesNGt2 (t_board_p b);

/* Printing(writing)/reading */

void PrintBoard (t_board_p b,
                 FILE * pf,
                 const char * symbols,
                 const char * empty);

void PrintBoardPV (t_board_p b,
                   FILE * pf,
                   const char * symbols,
                   const char * empty);

int ReadBoard (t_board_p b,
               FILE * pf,
               const char * symbols,
               const char * empty);

/* Raw string get/set */

void GetBoardRaw (t_board_p b,
                  char * raw,
                  const char * symbols,
                  const char * empty);

int SetBoard (t_board_p b,
              const char * str,
              const char * symbols,
              const char * empty);

/*/////////////////////////////////////////////////////////////// */
/* sudoku-solver.c */
/* Core of solving engine */
/*/////////////////////////////////////////////////////////////// */

int Solve (t_board_p b,    /* Puzzle to solve */

           char traplevel, /* 0 == never stop */
                           /* N == stop after first N-level rule */

           char bguess);   /* TRUE  == "guess if needed" */
                           /* FALSE == "do not guess" */

/*/////////////////////////////////////////////////////////////// */
/* sudoku-grids.c */
/* Functions for building boards */
/*/////////////////////////////////////////////////////////////// */

#define GR_BLOCK   0
#define GR_ROW     1
#define GR_COL     2
#define GR_DIAG    3

t_board_p ConstructBasicBoard (int order,  /* Typical: 3 */
                               char diag); /* TRUE == diagonals */

t_board_p ConstructCustomBoard (
                             char wb,     /* Block width */
                             char hb,     /* Block height */
                             char diag,   /* TRUE == diagonals */
                             int nGrids,  /* Num. composed grids */
                             int * xg,    /* Coordinates of */
                             int * yg);   /* grids (in blocks) */

t_board_p ConstructSamuraiBoard (
                             char wb,     /* Block width */
                             char hb,     /* Block height */
                             char diag);  /* TRUE == diagonals */


#ifdef __cplusplus
}
#endif

#endif
