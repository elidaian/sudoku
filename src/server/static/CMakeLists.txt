
set (JQUERY_FILES jquery-2.1.4.min.js)
set (BOOTSTRAP_FILES bootstrap.min.css
                     bootstrap.min.js
                     bootstrap-theme.min.css)
set (OWN_FILES board.css
               customization.css
               print.css)
set (FILES ${JQUERY_FILES} ${BOOTSTRAP_FILES} ${OWN_FILES})
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach()

install (FILES ${FILES}
         DESTINATION ${PYTHON_SITE_PACKAGES}/sudoku_server/static)

