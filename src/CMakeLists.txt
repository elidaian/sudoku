
function (set_if_unset VARIABLE VALUE)
    if (NOT DEFINED ${${VARIABLE}})
        set(${VARIABLE} ${VALUE} PARENT_SCOPE)
    endif ()
endfunction ()

set_if_unset(BIN_DIR bin)
set_if_unset(LIB_DIR lib)

add_subdirectory(core)
add_subdirectory(python)

