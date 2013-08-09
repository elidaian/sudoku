
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

set_target_properties(creator solver dodeka-solver
                      PROPERTIES
                      RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

