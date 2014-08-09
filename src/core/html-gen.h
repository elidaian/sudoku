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

    html-gen.h
*/
#include<stdio.h>

void printHead(FILE *f,char *str);
void printFoot(FILE *f);
void openMainTable(FILE *f,int w,int h);
void closeMainTable(FILE *f);
void openMainLine(FILE *f,int wb);
void closeMainLine(FILE *f);
void openMainRow(FILE *f,int hb);
void closeMainRow(FILE *f);
void openLine(FILE *f,int hb);
void closeLine(FILE *f);
void openRow(FILE *f,int wb);
void closeRow(FILE *f);
