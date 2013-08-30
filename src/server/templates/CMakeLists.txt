
set (FILES create_board.html
           html_board.html
           layout.html
           login.html
           main_page.html
           print_board.html
           register.html
           view_board.html)
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach()
