cmake_minimum_required(VERSION 3.16)
project(livox_ros_driver2)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
add_compile_definitions(BUILDING_ROS2)
include(cmake/version.cmake)
find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()
find_package(PCL REQUIRED COMPONENTS common io)
find_package(PkgConfig REQUIRED)
pkg_check_modules(APR REQUIRED apr-1)
find_package(Threads REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)

# Build the Agras SDK as part of this ROS package, for the current architecture.
# No global /usr/local SDK installation or prebuilt architecture library is used.
add_subdirectory(third_party/Livox-SDK2/sdk_core)
target_link_libraries(livox_lidar_sdk_shared PRIVATE Threads::Threads)

rosidl_generate_interfaces(livox_interfaces2
  "msg/CustomPoint.msg" "msg/CustomMsg.msg"
  DEPENDENCIES builtin_interfaces std_msgs
  LIBRARY_NAME ${PROJECT_NAME})

ament_auto_add_library(${PROJECT_NAME} SHARED
    src/livox_ros_driver2.cpp
    src/lddc.cpp
    src/driver_node.cpp
    src/lds.cpp
    src/lds_lidar.cpp

    src/ext_imu_bridge.cpp

    src/comm/comm.cpp
    src/comm/ldq.cpp
    src/comm/semaphore.cpp
    src/comm/lidar_imu_data_queue.cpp
    src/comm/cache_index.cpp
    src/comm/pub_handler.cpp

    src/parse_cfg_file/parse_cfg_file.cpp
    src/parse_cfg_file/parse_livox_lidar_cfg.cpp

    src/call_back/lidar_common_callback.cpp
    src/call_back/livox_lidar_callback.cpp
)
target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra -Wno-unused-parameter)
target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${PCL_INCLUDE_DIRS} ${APR_INCLUDE_DIRS})
target_include_directories(${PROJECT_NAME} PRIVATE 3rdparty src)
rosidl_get_typesupport_target(cpp_typesupport_target livox_interfaces2 rosidl_typesupport_cpp)
target_link_libraries(${PROJECT_NAME}
  ${cpp_typesupport_target} livox_lidar_sdk_shared
  ${PCL_LIBRARIES} ${APR_LIBRARIES} Threads::Threads)
rclcpp_components_register_node(${PROJECT_NAME}
  PLUGIN "livox_ros::DriverNode" EXECUTABLE ${PROJECT_NAME}_node)
ament_auto_package(INSTALL_TO_SHARE config launch)
