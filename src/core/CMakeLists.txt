
set (COMMON_SOURCES list.c
                    html-gen.c
                    sudoku-grids.c
                    sudoku-iface.c
                    sudoku-mem.c
                    sudoku-solver.c)
set (COMMON_LIB sudoku)
add_library (${COMMON_LIB} STATIC ${COMMON_SOURCES})

add_executable (creator creator.c)
target_link_libraries (creator ${COMMON_LIB})

add_executable (solver solver.c)
target_link_libraries (solver ${COMMON_LIB})

add_executable (dodeka-solver dodeka-solver.c)
target_link_libraries (dodeka-solver ${COMMON_LIB})

set (EXECUTABLES creator solver dodeka-solver)

set_target_properties(${EXECUTABLES}
                      PROPERTIES
                      RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

install (TARGETS ${EXECUTABLES}
         RUNTIME DESTINATION ${BIN_DIR})