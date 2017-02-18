#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
from std_msgs.msg import Bool

pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)

# function to map from one range to another, similar to arduino
#def arduino_map(x, in_min, in_max, out_min, out_max):
#	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
def VelocityMap(x, in_min, in_max):
	# PWM absolute min/max
	pwm_min = 9400
	pwm_max = 10160
	# Min output (forward)
	out_min_forward = 10000
	# Max output (forward)
	out_max_forward = 10160
	# Min output (reverse)
	out_min_reverse = 9400
	# Max output (reverse)
	out_max_reverse = 9560
	
	if (x == 0 or x>20 or x<-20):
		return 9780 # Center safe stop value
	if (x > 0):
		return x * (out_max_forward - out_min_forward) // (in_max) + out_min_forward
	if (x < 0):
		return out_max_reverse - x * (out_max_reverse - out_min_reverse) // (in_min) 

def AngleMap(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# callback function on occurance of drive parameters(angle & velocity)
def callback(data):
	#pwm1 = data.velocity
	#pwm2 = data.angle	
	velocity = data.velocity
	angle = data.angle
	print("Velocity: ",velocity,"Angle: ",angle)
	# Do the computation
	#if velocity > 1:
	#	velocity = velocity + 7
	#if velocity < -1:
	#	velocity = velocity - 9
	pwm1 = velocity;
	#pwm1 = VelocityMap(velocity,-20,20);
	pwm2 = AngleMap(angle,-10,10,7180,12380);
	msg = drive_values()
	msg.pwm_drive = pwm1
	msg.pwm_angle = pwm2
	pub.publish(msg)

def talker():
	rospy.init_node('serial_talker', anonymous=True)
	rospy.Subscriber("drive_parameters", drive_param, callback)
	
	rospy.spin()

if __name__ == '__main__':
	print("Serial talker initialized")
	talker()
