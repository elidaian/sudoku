
function (set_if_unset VARIABLE VALUE)
    if (NOT DEFINED ${${VARIABLE}})
        set (${VARIABLE} ${VALUE} PARENT_SCOPE)
    endif ()
endfunction ()

set_if_unset (BIN_DIR bin)
set_if_unset (LIB_DIR lib)

add_dependency_dir (${CMAKE_CURRENT_BINARY_DIR}/core)
add_python_dir (${CMAKE_CURRENT_BINARY_DIR}/python)
add_python_dir (${CMAKE_CURRENT_BINARY_DIR})

add_subdirectory (core)
add_subdirectory (python)
add_subdirectory (server)

