
include_directories (${CMAKE_SOURCE_DIR}/src/core ${CMAKE_CURRENT_SOURCE_DIR})
set_source_files_properties (wrap.i PROPERTIES CPLUSPLUS ON)
swig_add_module (pysudoku python wrap.i wrap.cc)
swig_link_libraries (pysudoku ${PYTHON_LIBRARIES} sudoku)

install (TARGETS ${SWIG_MODULE_pysudoku_REAL_NAME}
         LIBRARY DESTINATION ${LIB_DIR})
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/pysudoku.py
         DESTINATION ${PYTHON_SITE_PACKAGES})
