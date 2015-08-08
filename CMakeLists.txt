cmake_minimum_required (VERSION 2.6)
project (sudoku)

# Force use of Python 2.x
set(Python_ADDITIONAL_VERSIONS 2.7 2.6 2.5 2.4)

find_package (SWIG REQUIRED)
include (${SWIG_USE_FILE})

find_package (PythonLibs REQUIRED)
include_directories (${PYTHON_INCLUDE_PATH})

find_package (PythonInterp REQUIRED)
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
                OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
                OUTPUT_STRIP_TRAILING_WHITESPACE)

include (Package.cmake)
make_rpm (1 5)
 
include (PythonDirs.cmake)

function (set_if_unset name value)
    if (NOT DEFINED ${name})
        set (${name} ${value} PARENT_SCOPE)
    endif ()
endfunction ()

set_if_unset (STATE_DIR "/var")
set_if_unset (CONF_DIR "/etc")

add_subdirectory (src)

