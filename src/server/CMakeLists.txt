
add_python_executable (server ${CMAKE_CURRENT_BINARY_DIR}/server.py)
add_python_executable (configure-server ${CMAKE_CURRENT_BINARY_DIR}/configure_server.py
                       INSTALL)

add_subdirectory (static)
add_subdirectory (templates)

set(DB_FILE "${CMAKE_CURRENT_BINARY_DIR}/sudoku.db")
set(APPLICATION_ROOT None)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.py.in
               ${CMAKE_CURRENT_BINARY_DIR}/config.py)

set(DB_FILE "${STATE_DIR}/www/sudoku/sudoku.db")
set(APPLICATION_ROOT "\"/sudoku\"")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.py.in
               ${CMAKE_CURRENT_BINARY_DIR}/sudoku.conf)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/sudoku-httpd.conf.in
               ${CMAKE_CURRENT_BINARY_DIR}/sudoku-httpd.conf)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/sudoku.wsgi.in
               ${CMAKE_CURRENT_BINARY_DIR}/sudoku.wsgi)

set (FILES configure_server.py
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
                   env SUDOKU_SERVER_CONF_FILE=${CMAKE_CURRENT_BINARY_DIR}/config.py
                       ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/configure-server
                   DEPENDS _pysudoku
                   COMMENT "Configuring server")

add_custom_target (run-server
                   env SUDOKU_SERVER_CONF_FILE=${CMAKE_CURRENT_BINARY_DIR}/config.py
                       ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/server
                   DEPENDS _pysudoku
                   COMMENT "Setting up server")

install (FILES ${FILES} ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
         DESTINATION ${PYTHON_SITE_PACKAGES}/sudoku_server)
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/sudoku.conf
         DESTINATION ${CONF_DIR})
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/sudoku-httpd.conf
         DESTINATION ${CONF_DIR}/httpd/conf.d)
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/sudoku.wsgi
         DESTINATION ${STATE_DIR}/www/sudoku)

