#!/usr/bin/env python
import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0 
kd = 0.09 
servo_offset = 0
prev_error = 0.0
vel_input = 9780

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)




def control(data):
	global prev_error
	global vel_input
	global kp
	global kd
	global kp
	global kd

	msg = drive_param()
	msg.velocity = vel_input

	## Your code goes here
	# 1. Scale the error
	# 2. Apply the PID equation on error
	# 3. Make sure the error is within bounds
	## END
	'''
	error = data.pid_error
	V_theta = kp * error + kd(error - prev_error)


	if V_theta > 100:
		V_theta = 100
	elif V_theta < -100:
		V_theta = -100

	prev_error = error

	angle = V_theta

	'''


	pid_error = data.pid_error
        error = pid_error * kp
        errordot = kd * (pid_error - prev_error)

        angle = error + errordot

        if angle > 100:
            angle = 100
        elif angle < -100:
            angle = -100

        prev_error = pid_error


	msg.angle = angle

	print(msg.angle)
	print("             ")
	print(msg.velocity)
	pub.publish(msg)

if __name__ == '__main__':
	#global kp
	#global kd
	#global vel_input
	print("Listening to error for PID")
	#kp = input("Enter Kp Value: ")
	#kd = input("Enter Kd Value: ")
	#vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()
