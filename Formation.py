#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Twist

pub=rospy.Publisher("/r1/cmd_vel",Twist,queue_size=1)
pub2=rospy.Publisher("/r2/cmd_vel",Twist,queue_size=1)
pub3=rospy.Publisher("/r3/cmd_vel",Twist,queue_size=1)
pub4=rospy.Publisher("/r4/cmd_vel",Twist,queue_size=1)

x = 0.0
y = 0.0
goal = Point()
goal.x = 5
goal.y = 0
def callback(data):
	global x
	global y
	move = Twist()
	x = data.pose.pose.position.x
    	y = data.pose.pose.position.y
	if(abs(goal.x - x) > 0.1) and not rospy.is_shutdown():
		move.linear.x = 0.4
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
def subscriber():
	rospy.init_node('subscriber', anonymous=True)
	rospy.Subscriber("/r1/odom", Odometry, callback)
	rospy.Subscriber("/r2/odom", Odometry, robot2)
	rospy.Subscriber("/r3/odom",Odometry,robot3)
	rospy.Subscriber("/r4/odom",Odometry,robot4)
	rospy.spin()
if __name__=='__main__':
	subscriber()

