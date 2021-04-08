#! /usr/bin/env python
import rospy
import message_filters 
from DEP.msg import Goal
from sensor_msgs.msg import Image

class CollectData():
	def __init__(self):	
		self.current_color_img_msg = None
		self.current_depth_img_msg = None
		self.current_waypoint_msg = None
		self.color_received = False
		self.depth_received = False
		self.waypoint_received = False
		self.color_img_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.color_img_cb)
		self.depth_img_sub = rospy.Subscriber("/camera/depth/image_raw", Image, self.depth_img_cb)
		self.waypoint_sub = rospy.Subscriber("goal", Goal, self.waypoint_cb)
		self.collect_data()
		

	def color_img_cb(self, color_img_msg):
		self.current_color_img_msg = color_img_msg
		self.color_received = True

	def depth_img_cb(self, depth_img_msg):
		self.current_depth_img_msg = depth_img_msg
		self.depth_received = True

	def waypoint_cb(self, waypoint_msg):
		self.waypoint_msg = waypoint_msg
		self.waypoint_received = True

	def collect_data(self):
		if (self.color_received == False):
			rospy.loginfo("wait for color image...")

		if (self.depth_received == False):
			rospy.loginfo("wait for depth image...")

		if (self.waypoint_received == False):
			rospy.loginfo("wait for waypoint...")


		all_received = False
		while all_received == False and not rospy.is_shutdown():
			all_received = self.color_received and self.waypoint_received and self.waypoint_received

		rospy.loginfo("Message Ready!")


		while not rospy.is_shutdown():
			pass
			''' TODO
			Check if we obatin a new waypoint
			if we obtain a new waypoint: 
				1. save current color image 
				2. save current depth image
				3. save current waypoint (x, y, z)
			'''

def main():
	rospy.init_node('collect_data', anonymous=False)
	CollectData()
	rospy.spin()

if __name__ == "__main__":
	main()