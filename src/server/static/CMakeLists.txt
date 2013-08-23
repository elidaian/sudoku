
set (FILES style.css)
foreach (file ${FILES})
    configure_file (${file} ${file} COPYONLY)
endforeach()
