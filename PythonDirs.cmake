
set (PYTHON_DIRS)

function (add_python_dir dir)
    get_filename_component (ABS_DIR ${dir} ABSOLUTE)
    list (APPEND PYTHON_DIRS ${ABS_DIR})
    set (PYTHON_DIRS ${PYTHON_DIRS} PARENT_SCOPE)
endfunction()

function (add_python_executable exec source)
    get_filename_component (ABS_SOURCE ${source} ABSOLUTE)
    get_filename_component (EXEC_NAME ${exec} NAME)
    
    # Write the executable script
    set (SCRIPT "${CMAKE_CURRENT_BINARY_DIR}/${EXEC_NAME}")
    file (WRITE  ${SCRIPT} "#!${PYTHON_EXECUTABLE}\n")
    file (APPEND ${SCRIPT} "import sys\n")
    file (APPEND ${SCRIPT} "sys.path.extend('${PYTHON_DIRS}'.split(';'))\n")
    file (APPEND ${SCRIPT} "execfile('${ABS_SOURCE}')\n")

    execute_process (COMMAND chmod 755 ${CMAKE_CURRENT_BINARY_DIR}/${EXEC_NAME})

    if ("${ARGN}" STREQUAL "INSTALL")
        get_filename_component (INST_EXEC_NAME ${exec} NAME_WE)
        install (FILES ${ABS_SOURCE}
                 PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE
                             GROUP_READ GROUP_EXECUTE
                             WORLD_READ WORLD_EXECUTE
                 DESTINATION ${BIN_DIR}
                 RENAME ${INST_EXEC_NAME})
    endif ()
endfunction()

