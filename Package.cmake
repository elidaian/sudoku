
function (make_rpm MAJOR_VERSION MINOR_VERSION)
    # parse arguments
    set (SPEC_FILE ${PROJECT_NAME}.spec)
    foreach (arg ${ARGN})
        set (SPEC_FILE ${arg})
    endforeach ()

    # try SVN information
    extract_svn_revision ()
    if ("${TEAM_FOUND}" STREQUAL "FALSE")
        # try git information
        extract_git_revision ()
        if ("${TEAM_FOUND}" STREQUAL "FALSE")
            # Nothing found
            message (WARNING " No team information found, disabling packing support")
        endif ()
    endif ()

endfunction ()

function (extract_svn_revision)
    execute_process (COMMAND svn info ${CMAKE_SOURCE_DIR}
                     COMMAND grep URL
                     COMMAND cut "-d " -f2-
                     OUTPUT_VARIABLE TEAM_LOCATION
                     OUTPUT_STRIP_TRAILING_WHITESPACE
                     ERROR_QUIET)

    if (NOT "${TEAM_LOCATION}" STREQUAL "")
        # It is an SVN project
        set (TEAM_FOUND TRUE PARENT_SCOPE)

        execute_process (COMMAND svn info ${TEAM_LOCATION}
                         COMMAND grep Revision 
                         COMMAND cut "-d " -f2
                         OUTPUT_VARIABLE TEAM_VERSION
                         OUTPUT_STRIP_TRAILING_WHITESPACE)
        set (PROJECT_VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${TEAM_VERSION})

        message (STATUS "Found SVN, project version is ${PROJECT_VERSION}")

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
    else ()
        # It is not an SVN project
        set (TEAM_FOUND FALSE PARENT_SCOPE)
    endif ()
endfunction ()
 
function (extract_git_revision)
    execute_process (COMMAND git log --pretty=oneline
                     COMMAND wc -l
                     OUTPUT_VARIABLE NUM_COMMITS
                     OUTPUT_STRIP_TRAILING_WHITESPACE
                     ERROR_QUIET
                     RESULT_VARIABLE RC)

    if (${RC} EQUAL 0)
        # It is a git project
        set (TEAM_FOUND TRUE PARENT_SCOPE)

        execute_process (COMMAND git log --abbrev-commit --pretty=oneline
                         COMMAND head -n1
                         COMMAND cut -f1 -d\ 
                         OUTPUT_VARIABLE HASH
                         OUTPUT_STRIP_TRAILING_WHITESPACE
                         ERROR_QUIET)
        set (PROJECT_VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${NUM_COMMITS}.${HASH})

        message (STATUS "Found git, project version is ${PROJECT_VERSION}")

        # set some variables
        set (PACKAGE_FULL_NAME ${PROJECT_NAME}-${PROJECT_VERSION})
        set (TARBALL_NAME ${PACKAGE_FULL_NAME}.tar.gz)
        set (PACKING_DIRECTORY ${CMAKE_BINARY_DIR}/packing)
        file (MAKE_DIRECTORY ${PACKING_DIRECTORY})

        # configure the SPEC file
        configure_file (${SPEC_FILE}.in ${PACKING_DIRECTORY}/${SPEC_FILE})

        # add the tarball target
        add_custom_command (OUTPUT ${PACKING_DIRECTORY}/${TARBALL_NAME}
                            COMMAND git archive --prefix=${PACKAGE_FULL_NAME}/
                                                --format=tar ${HASH} |
                                                gzip > ${PACKING_DIRECTORY}/${TARBALL_NAME}
                            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
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
    else ()
        # It is not a git project
        set (TEAM_FOUND FALSE PARENT_SCOPE)
    endif ()
endfunction ()

 
