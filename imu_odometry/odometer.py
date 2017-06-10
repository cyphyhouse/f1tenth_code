#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

global pub

# Publishes the current data on the topic curr_pos
def publish_position(pose_data):
	rospy.loginfo(pose_data)
	pub.publish(pose_data)
		

# Subscribes node to the topic /imu which has msgs of type 
# sensor_msgs/Imu messages being published on it via the imu
def get_imu_messages():
	rospy.Subscriber('imu0', Imu, get_position)
	rospy.sleep(0.5)
	rospy.spin()


# Uses the equations of motion to get position of the robot
def get_position(imu_data):
	pose_data = Twist()
	
	# the time difference between receiving two msgs
	rate = 0.5	

	# s = ut + 1/2at^2
	# to get linear velocity, we use linear acceleration
	ux = imu_data.linear_acceleration.x*rate
	uy = imu_data.linear_acceleration.y*rate
	pose_data.linear.x = ux*rate + 0.5*imu_data.linear_acceleration.x*rate*rate
	pose_data.linear.y = uy*rate + 0.5*imu_data.linear_acceleration.y*rate*rate
	pose_data.linear.z = 0
	
	# Magnetometer needs to be incorporated here to measure turn 
      
        pose_data.angular.x = imu_data.angular_velocity.x*rate
      	pose_data.angular.y = imu_data.angular_velocity.y*rate
      	pose_data.angular.z = 0
	
	publish_position(pose_data)
	
	
if __name__ == '__main__':
	try:
		rospy.init_node('imu_only_odometry')
		
		# Initializing the publisher, all the odometry data will be
		# published on the topic curr_pos 
		pub = rospy.Publisher('curr_pos', 
				Twist, queue_size=1000)
		
		get_imu_messages()
	except rospy.ROSInterruptException:
		pass
