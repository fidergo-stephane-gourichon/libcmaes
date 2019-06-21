
include_directories (${PROJECT_SOURCE_DIR}/src)
include_directories (${PROJECT_BINARY_DIR}/src)

macro (cmaes_add_test name link_libraries)
  add_executable (t_${name} ${name}.cc)
  target_link_libraries (t_${name} cmaes ${link_libraries})
  add_test (NAME ${name} COMMAND t_${name})
  if (WIN32)
    set_tests_properties (${name} PROPERTIES ENVIRONMENT "PATH=${PROJECT_BINARY_DIR}\\src\\${CMAKE_BUILD_TYPE};$ENV{PATH}")  # to load dll
  endif ()
endmacro ()

cmaes_add_test (simple-test "")
cmaes_add_test (edm "")



get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()


if (GFLAGS_FOUND)
  cmaes_add_test (test-functions gflags)
else()
  message(WARNING "Not building tests that depend on gflags, consider re-running CMake after doing this: git submodule update --init")
endif()
