
set (PYTHON_DIRS)

function (add_python_dir dir)
    get_filename_component (ABS_DIR ${dir} ABSOLUTE)
    list (APPEND PYTHON_DIRS ${ABS_DIR})
    set (PYTHON_DIRS ${PYTHON_DIRS} PARENT_SCOPE)
endfunction()

function (add_python_executable exec source)
    get_filename_component (ABS_SOURCE ${source} ABSOLUTE)
    get_filename_component (EXEC_NAME ${exec} NAME)
    file (WRITE ${CMAKE_CURRENT_BINARY_DIR}/${EXEC_NAME}
          "#!${PYTHON_EXECUTABLE}\nimport sys\nsys.path.extend('${PYTHON_DIRS}'.split(';'))\nexecfile('${ABS_SOURCE}')\n")
    execute_process (COMMAND chmod 755 ${CMAKE_CURRENT_BINARY_DIR}/${EXEC_NAME})
endfunction()

