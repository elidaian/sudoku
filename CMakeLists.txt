cmake_minimum_required (VERSION 2.6)
project (sudoku)

set (COMMON_SOURCES list.c
                    sudoku-grids.c
                    sudoku-iface.c
                    sudoku-mem.c)
set (COMMON_LIB sudoku)
add_library (${COMMON_LIB} STATIC ${COMMON_SOURCES})

add_executable (creator creator.c)
target_link_libraries (creator ${COMMON_LIB})

add_executable (solver solver.c)
target_link_libraries (solver ${COMMON_LIB})

add_executable (dodeka-solver dodeka-solver.c)
target_link_libraries (dodeka-solver ${COMMON_LIB})

