
set (FILES layout.html
           login.html
           main_page.html
           register.html)
foreach (file ${FILES})
    configure_file (${file} ${file} COPYONLY)
endforeach()
