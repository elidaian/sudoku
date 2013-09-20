
set (FILES create_board.html
           html_board.html
           layout.html
           login.html
           main_page.html
           manage.html
           pdf_board.tex
           print_board.html
           register.html
           view_board.html)
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach()

install (FILES ${FILES}
         DESTINATION ${PYTHON_SITE_PACKAGES}/sudoku_server/templates)

