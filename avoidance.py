#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from sensor_msgs.msg import LaserScan 
from math import atan2

pub2=rospy.Publisher("/r2/cmd_vel",Twist,queue_size=1)
pub3=rospy.Publisher("/r3/cmd_vel",Twist,queue_size=1)
pub4=rospy.Publisher("/r4/cmd_vel",Twist,queue_size=1)

x = 0.0
y = 0.0
theta = 0.0
goal = Point()
goal.x = 5
goal.y = 0
def callback(msg):
    	global x
    	global y
    	global theta 
    	x = msg.pose.pose.position.x
    	y = msg.pose.pose.position.y
    	rot_q = msg.pose.pose.orientation
    	(roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    	inc_x = goal.x -x
    	inc_y = goal.y -y
 
    	angle_to_goal = atan2(inc_y, inc_x)
 
    	if(abs(goal.x - x) > 0.1):
		move.linear.x = 0.4
		print("linear motion")
    	if((angle_to_goal - theta) > 1):
		move.linear.x = 0.1
		move.angular.z = -0.4
		print("theta causing trouble: ",(angle_to_goal - theta))
	if((angle_to_goal - theta) < -1):
		move.linear.x = 0.2
		move.angular.z = 0.6
		print("correction theta : ", (angle_to_goal - theta))
	if(x > 5):
		move.linear.x = 0
		move.angular.z = 0
	pub.publish(move)

def Lasercall(data):
	obstacle_position = x + data.ranges[342]
	print("obstacle_position : ", obstacle_position)
	print("laser values : ", data.ranges[337:342])
	if(obstacle_position < goal.x):
		for i in (data.ranges[342:352]):
			if(i < 2.5):
				move.linear.x = 0.2	
				move.angular.z = 0.4
				print(" has to turn right")
		for i in (data.ranges[332:342]):
			if(i < 2.5):
				move.linear.x = 0.2	
				move.angular.z = -0.4
				print(" has to turn left")
		print("laser detected obstacle to tackle")
	pub.publish(move)

def robot2(data):
	move = Twist()
	x2 = data.pose.pose.position.x
    	y2 = data.pose.pose.position.y
	if(abs(x - x2) >= 1) and not rospy.is_shutdown():
		move.linear.x = 0.4
	pub2.publish(move)
def robot3(data):
	move = Twist()
	x3 = data.pose.pose.position.x
    	y3 = data.pose.pose.position.y
	if(abs(x - x3) >= 2) and not rospy.is_shutdown():
		move.linear.x = 0.4
	pub3.publish(move)
def robot4(data):
	move = Twist()
	x4 = data.pose.pose.position.x
    	y4 = data.pose.pose.position.y
	if(abs(x - x4) >= 3) and not rospy.is_shutdown():
		move.linear.x = 0.4
	pub4.publish(move)

if __name__=='__main__':
	rospy.init_node('subscriber', anonymous=True)
	rospy.Subscriber("/r1/odom", Odometry, callback)
	rospy.Subscriber("/r1/front_laser/scan",LaserScan,Lasercall)
	rospy.Subscriber("/r2/odom", Odometry, robot2)
	rospy.Subscriber("/r3/odom",Odometry,robot3)
	rospy.Subscriber("/r4/odom",Odometry,robot4)
	pub=rospy.Publisher("/r1/cmd_vel",Twist,queue_size=1)
	move = Twist()
	rospy.spin()

