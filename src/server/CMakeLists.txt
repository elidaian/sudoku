
add_python_executable (server ${CMAKE_CURRENT_BINARY_DIR}/server.py)
add_python_executable (configure-server ${CMAKE_CURRENT_BINARY_DIR}/configure_server.py)

add_subdirectory (static)
add_subdirectory (templates)

set (FILES config.py
           configure_server.py
           db.py
           pdf_renderer.py
           schema.sql
           server.py
           users.py
           util.py)
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach ()

add_custom_target (configure-server
                   ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/configure-server
                   DEPENDS _pysudoku
                   COMMENT "Configuring server")

add_custom_target (run-server
                   ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/server
                   DEPENDS _pysudoku
                   COMMENT "Setting up server")

install (FILES ${FILES}
         DESTINATION ${PYTHON_SITE_PACKAGES}/sudoku_server)

