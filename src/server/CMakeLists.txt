
add_python_executable (server ${CMAKE_CURRENT_BINARY_DIR}/server.py)

add_subdirectory (static)
add_subdirectory (templates)

set (FILES config.py
           db.py
           schema.sql
           server.py
           users.py)
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach ()

add_custom_target (run-server
                   ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/server
                   DEPENDS _pysudoku
                   COMMENT "Setting up server")

