# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(WARNING "Invoking generate_messages() without having added any message or service file before.
You should either add add_message_files() and/or add_service_files() calls or remove the invocation of generate_messages().")
message(STATUS "cs431demo: 0 messages, 0 services")

set(MSG_I_FLAGS "-Irace:/home/ubuntu/catkin_ws/src/race/msg;-Isensor_msgs:/opt/ros/indigo/share/sensor_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(cs431demo_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_cpp(cs431demo
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/cs431demo
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(cs431demo_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(cs431demo_generate_messages cs431demo_generate_messages_cpp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(cs431demo_gencpp)
add_dependencies(cs431demo_gencpp cs431demo_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS cs431demo_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_lisp(cs431demo
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/cs431demo
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(cs431demo_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(cs431demo_generate_messages cs431demo_generate_messages_lisp)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(cs431demo_genlisp)
add_dependencies(cs431demo_genlisp cs431demo_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS cs431demo_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages

### Generating Services

### Generating Module File
_generate_module_py(cs431demo
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/cs431demo
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(cs431demo_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(cs431demo_generate_messages cs431demo_generate_messages_py)

# add dependencies to all check dependencies targets

# target for backward compatibility
add_custom_target(cs431demo_genpy)
add_dependencies(cs431demo_genpy cs431demo_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS cs431demo_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/cs431demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/cs431demo
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(cs431demo_generate_messages_cpp race_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/cs431demo)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/cs431demo
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(cs431demo_generate_messages_lisp race_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/cs431demo)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/cs431demo\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/cs431demo
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(cs431demo_generate_messages_py race_generate_messages_py)
