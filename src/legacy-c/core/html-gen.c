/*
 * html-gen.c
 *
 *  Created on: 9 באוג 2013
 *      Author: eli
 */

#include "html-gen.h"

void printHead(FILE *f,char *str)
{
	fprintf(f,"<HTML>\n\t<HEAD>\n\t\t<TITLE>Sudoku%s</TITLE>\n\t\t<STYLE type=\"text/css\">\n\t\t\tTABLE.main { border-collapse: collapse; border: 4pt solid black }\n\t\t\tTABLE.lower { border-collapse: collapse; border: 2pt solid black }\n\t\t\tTD { border: 1pt solid black; padding: 0pt 0pt 0pt 0pt; font-size: 20pt }\n\t\t\tDIV.head { font-size: 20pt; font-weigth: bold }\n\t\t</STYLE>\n\t</HEAD>\n\t<BODY>\n\t<CENTER>\n\t\t<DIV CLASS=\"head\">Eli Daian\'s Sudoku%s</DIV>\n\t</CENTER>\n",str,str);
}
void printFoot(FILE *f)
{
	fprintf(f,"\t</BODY>\n</HTML>\n");
}
void openMainTable(FILE *f,int w,int h)
{
	fprintf(f,"\t\t<CENTER>\n\t\t\t<TABLE WIDTH=%d HEIGHT=%d CLASS=\"main\">\n",35*w,35*h);
}
void closeMainTable(FILE *f)
{
	fprintf(f,"\t\t\t</TABLE>\n\t\t</CENTER>\n");
}
void openMainLine(FILE *f,int wb)
{
	fprintf(f,"\t\t\t\t<TR HIEGHT=%d%%>\n",wb);
}
void closeMainLine(FILE *f)
{
	fprintf(f,"\t\t\t\t</TR>\n");
}
void openMainRow(FILE *f,int hb)
{
	fprintf(f,"\t\t\t\t\t<TD WIDTH=%d%%>\n\t\t\t\t\t\t<TABLE WIDTH=100%% HEIGHT=100%% CLASS=\"lower\">\n",100/hb);
}
void closeMainRow(FILE *f)
{
	fprintf(f,"\t\t\t\t\t\t</TABLE>\n\t\t\t\t\t</TD>\n");
}
void openLine(FILE *f,int hb)
{
	fprintf(f,"\t\t\t\t\t\t\t<TR HEIGHT=%d%%>\n",100/hb);
}
void closeLine(FILE *f)
{
	fprintf(f,"\t\t\t\t\t\t\t</TR>\n");
}
void openRow(FILE *f,int wb)
{
	fprintf(f,"\t\t\t\t\t\t\t\t<TD WIDTH=%d%% ALIGN=CENTER>\n\t\t\t\t\t\t\t\t",100/wb);
}
void closeRow(FILE *f)
{
	fprintf(f,"\n\t\t\t\t\t\t\t\t</TD>\n");
}
