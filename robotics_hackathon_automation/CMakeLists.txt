cmake_minimum_required(VERSION 3.0.2)
project(robotics_hackathon_automation)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  message_generation
)

add_message_files(
  FILES
  NextPoint.msg
  PointList.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)





include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
