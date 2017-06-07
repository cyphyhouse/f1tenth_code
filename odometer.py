#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseWithCovarianceStamped

# Use pandas to read rosbag and rviz data

def talker():
  pub = rospy.Publisher('movements', PoseWithCovarianceStamped, queue_size=10)
  rospy.init_node('imu_odometry', anonymous=True)
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():

      # Not using Kalman filter, not using magnetometer
      
      ux = Imu.linear_acceleration_covariance[0]*rate
      odometer_msg[0] = ux*rate + (0.5)*Imu.linear_acceleration_covariance[0]*rate*rate
      uy = Imu.linear_acceleration_covariance[1]*rate
      odometer_msg[1] = uy*rate + (0.5)*Imu.linear_acceleration_covariance[1]*rate*rate
      odometer_msg[2] = 0

      # Magnetometer needs to be incorporated here to measure turn 
      
      odometer_msg[3] = Imu.angular_velocity[0]*rate
      odometer_msg[4] = Imu.angular_velocity[1]*rate
      odometer_msg[5] = 0
      
      rospy.loginfo(odometer_msg)
      pub.publish(odometer_msg)
      rate.sleep()

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass
