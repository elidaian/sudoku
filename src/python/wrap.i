/* 
 * wrap.i
 * 
 *  Created on: 9 באוג 2013
 *      Author: eli
 */

%define DOCSTRING
"Sudoku for Python by Eli Daian.
Allows generating standard and custom sudoku board using the Python interpreter."
%enddef

%module(docstring=DOCSTRING) pysudoku

%{
#include "wrap.h"
%}

%feature("autodoc", "1");

%include "std_string.i"
%include "std_vector.i"
%include "wrap.h"
 
