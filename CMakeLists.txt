cmake_minimum_required(VERSION 3.10)

project(Homework3 VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
elseif(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2 /DNDEBUG")
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_executable(edge_cover main.cpp)

file(WRITE ${CMAKE_BINARY_DIR}/input.txt "6 7\n0 1\n0 2\n1 3\n2 3\n2 4\n3 5\n4 5\n")

add_custom_target(run
        COMMAND edge_cover
        DEPENDS edge_cover
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running edge_cover program..."
)

add_custom_target(run-save
        COMMAND edge_cover > output.txt
        DEPENDS edge_cover
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running edge_cover and saving output to output.txt..."
)

find_package(Python3 COMPONENTS Interpreter)
if(Python3_FOUND)
    add_custom_target(verify
            COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/verify.py
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
            COMMENT "Running Python verification via NetworkX..."
    )

    add_custom_target(test
            COMMAND edge_cover
            COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/verify.py
            DEPENDS edge_cover
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            COMMENT "Running full test suite..."
    )
else()
    message(WARNING "Python3 not found. 'verify' and 'test' targets will not be available.")
endif()

if(UNIX AND NOT APPLE)
    find_program(VALGRIND valgrind)
    if(VALGRIND)
        add_custom_target(memcheck
                COMMAND ${VALGRIND} --leak-check=full --show-leak-kinds=all
                --track-origins=yes --verbose
                $<TARGET_FILE:edge_cover>
                DEPENDS edge_cover
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
                COMMENT "Running Valgrind memory check..."
        )
    else()
        message(STATUS "Valgrind not found. 'memcheck' target will not be available.")
    endif()
endif()

add_custom_target(submit
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/submission
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/main.cpp ${CMAKE_BINARY_DIR}/submission/
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/verify_edge_cover.py ${CMAKE_BINARY_DIR}/submission/
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/CMakeLists.txt ${CMAKE_BINARY_DIR}/submission/
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_SOURCE_DIR}/report.md ${CMAKE_BINARY_DIR}/submission/
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_SOURCE_DIR}/README.md ${CMAKE_BINARY_DIR}/submission/
        COMMAND ${CMAKE_COMMAND} -E tar czf ${CMAKE_BINARY_DIR}/submission.tar.gz ${CMAKE_BINARY_DIR}/submission
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/submission
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Creating submission archive..."
)

install(TARGETS edge_cover
        RUNTIME DESTINATION bin
)

install(FILES
        ${CMAKE_SOURCE_DIR}/verify.py
        ${CMAKE_SOURCE_DIR}/README.md
        DESTINATION share/edge_cover
        OPTIONAL
)

message(STATUS "")
message(STATUS "=== Minimum Edge Cover Configuration ===")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "C++ Standard: C++${CMAKE_CXX_STANDARD}")
message(STATUS "Install prefix: ${CMAKE_INSTALL_PREFIX}")
if(Python3_FOUND)
    message(STATUS "Python3: ${Python3_EXECUTABLE}")
endif()
if(VALGRIND)
    message(STATUS "Valgrind: ${VALGRIND}")
endif()
message(STATUS "========================================")
message(STATUS "")