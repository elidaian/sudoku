

set (FILES glyphicons-halflings-regular.eot
           glyphicons-halflings-regular.svg
           glyphicons-halflings-regular.ttf
           glyphicons-halflings-regular.woff
           glyphicons-halflings-regular.woff2)
foreach (file ${FILES})
    configure_file (${CMAKE_CURRENT_SOURCE_DIR}/${file}
                    ${CMAKE_CURRENT_BINARY_DIR}/${file}
                    COPYONLY)
endforeach()

install (FILES ${FILES}
         DESTINATION ${PYTHON_SITE_PACKAGES}/sudoku_server/fonts)

