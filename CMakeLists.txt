# Copyright: 2012 iCub Facility, Istituto Italiano di Tecnologia
# Author: Lorenzo Natale
# CopyPolicy: Released under the terms of the GNU GPL v2.0.
# 

CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
SET(PROJECTNAME SpinnIOTest)
PROJECT(${PROJECTNAME})


FIND_PACKAGE(SpinnIO REQUIRED)


INCLUDE_DIRECTORIES(${SPINNIO_INCLUDE_DIRS})
LINK_LIBRARIES(${SPINNIO_LIB})

LINK_LIBRARIES(pthread)
LINK_LIBRARIES(sqlite3)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")

add_executable(spinnioSendRecv spinnioSendRecv.cpp)
add_executable(spinnioRecvOnly spinnioRecvOnly.cpp)
add_executable(spinnioSendOnly spinnioSendOnly.cpp)



