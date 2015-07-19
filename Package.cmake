
function (make_rpm MAJOR_VERSION MINOR_VERSION)
    # parse arguments
    set (SPEC_FILE ${PROJECT_NAME}.spec)
    foreach (arg ${ARGN})
        set (SPEC_FILE ${arg})
    endforeach ()

    # add SVN information
    execute_process (COMMAND svn info ${CMAKE_SOURCE_DIR}
                     COMMAND grep URL
                     COMMAND cut "-d " -f2-
                     OUTPUT_VARIABLE TEAM_LOCATION
                     OUTPUT_STRIP_TRAILING_WHITESPACE
                     ERROR_QUIET)
    if ("${TEAM_LOCATION}" STREQUAL "")
        message (WARNING " No team information found, disabling packing support")
    else ()
        execute_process (COMMAND svn info ${TEAM_LOCATION}
                         COMMAND grep Revision 
                         COMMAND cut "-d " -f2
                         OUTPUT_VARIABLE TEAM_VERSION
                         OUTPUT_STRIP_TRAILING_WHITESPACE)
        set (PROJECT_VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${TEAM_VERSION})

        # set some variables
        set (PACKAGE_FULL_NAME ${PROJECT_NAME}-${PROJECT_VERSION})
        set (TARBALL_NAME ${PACKAGE_FULL_NAME}.tar.gz)
        set (PACKING_DIRECTORY ${CMAKE_BINARY_DIR}/packing)
        file (MAKE_DIRECTORY ${PACKING_DIRECTORY})

        # configure the SPEC file
        configure_file (${SPEC_FILE}.in ${PACKING_DIRECTORY}/${SPEC_FILE})

        # add the tarball target
        add_custom_command (OUTPUT ${PACKING_DIRECTORY}/${TARBALL_NAME}
                            COMMAND svn export ${TEAM_LOCATION} ${PACKAGE_FULL_NAME} > /dev/null
                            COMMAND tar czf ${TARBALL_NAME} ${PACKAGE_FULL_NAME}
                            WORKING_DIRECTORY ${PACKING_DIRECTORY}
                            COMMENT "Creating fresh source checkout tarball")
        add_custom_target (tarball
                           DEPENDS ${PACKING_DIRECTORY}/${TARBALL_NAME})

        # determine the RPM build root
        execute_process (COMMAND rpm -E "%{_topdir}"
                         OUTPUT_VARIABLE RPM_TOPDIR
                         OUTPUT_STRIP_TRAILING_WHITESPACE)

        # add the rpm target
        add_custom_target (rpm
                           COMMAND cp ${TARBALL_NAME} ${RPM_TOPDIR}/SOURCES
                           COMMAND rpmbuild -ba ${SPEC_FILE}
                           WORKING_DIRECTORY ${PACKING_DIRECTORY}
                           DEPENDS ${PACKING_DIRECTORY}/${TARBALL_NAME}
                           COMMENT "Creating RPM package")
    endif ()

endfunction ()
