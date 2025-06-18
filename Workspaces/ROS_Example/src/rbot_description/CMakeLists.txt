 
cmake_minimum_required(VERSION 3.28)

project(rbot_description)


#default to C++14
if(NOT CMAKE_CXX_STANDARD)
	set(CMAKE_CXX_STANDARD 14)
endif()

#find dependencies
find_package(ament_cmake REQUIRED)
find_package(ros_gz REQUIRED)


#export package
ament_package()

