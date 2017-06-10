#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseWithCovarianceStamped


# Publishes the current data on the topic curr_pos
def publish_position(pose_data):
	rospy.loginfo(pose_data)
	pub.publish(pose_data)
		

# Subscribes node to the topic /imu which has msgs of type 
# sensor_msgs/Imu messages being published on it via the imu
def get_imu_messages():
	rospy.Subscriber('imu', sensor_msgs.msgs.Imu, get_position)
	rospy.sleep(0.5)
	rospy.spin()


# Uses the equations of motion to get position of the robot
def get_position():
	pose_data = geometry_msgs.msgs.PoseWithCovarianceStamped()
	
	# s = ut + 1/2at^2
	# to get linear velocity, we use linear acceleration
	ux = Imu.linear_acceleration_covariance[0]*rate
	uy = Imu.linear_acceleration_covariance[1]*rate
	pose_data[0] = ux*rate + 0.5*Imu.linear_acceleration_covariance[0]*rate*rate
	pose_data[1] = uy*rate + 0.5*Imu.linear_acceleration_covariance[1]*rate*rate
	pose_data[2] = 0
	
	# Magnetometer needs to be incorporated here to measure turn 
      
        pose_data[3] = Imu.angular_velocity[0]*rate
      	pose_data[4] = Imu.angular_velocity[1]*rate
      	pose_data[5] = 0
	
	publish_position(pose_data)
	
	
if __name__ == '__main__':
	try:
		rospy.init_node('imu_only_odometry')
		
		# Initializing the publisher, all the odometry data will be
		# published on the topic curr_pos 
		global pub = rospy.Publisher('curr_pos', 
				geometry_msgs.msgs.PoseWithCovarianceStamped, queue_size=1000)
		
		get_imu_messages()
	except rospy.ROSInterruptException:
		pass
