#Last revised by yipingd 20210409

#! /usr/bin/env python
import rospy
import message_filters 
from DEP.msg import Goal
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import shutil
import numpy as np

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

		index = 0

		last_way_point = self.waypoint_msg



		while not rospy.is_shutdown():
			#pass
			''' TODO
			Check if we obatin a new waypoint
			if we obtain a new waypoint: 
				1. save current color image 
				2. save current depth image
				3. save current waypoint (x, y, z)
			'''

			###### INitialization ######
			if index == 0:
				color_image_folder = 'color_image/'
				if not os.path.exists(color_image_folder):
					os.mkdir(color_image_folder)
				shutil.rmtree(color_image_folder)
				os.mkdir(color_image_folder)

				depth_image_folder = 'depth_image/'
				if not os.path.exists(depth_image_folder):
					os.mkdir(depth_image_folder)
				shutil.rmtree(depth_image_folder)
				os.mkdir(depth_image_folder)

				waypoint_folder = 'waypoint/'
				if not os.path.exists(waypoint_folder):
					os.mkdir(waypoint_folder)
				shutil.rmtree(waypoint_folder)
				os.mkdir(waypoint_folder)

				waypoint_file_name = 'waypoint_file.txt'
				with open(waypoint_folder + waypoint_file_name, 'a+') as f:
					f.truncate()
					#my_waypoint_msg = str(index) + ',' + str(self.waypoint_msg.x) + ',' + str(self.waypoint_msg.y) + ',' + str(self.waypoint_msg.z)
					#f.write(my_waypoint_msg)
					#f.write('\n')


			if last_way_point.x != self.waypoint_msg.x or last_way_point.y != self.waypoint_msg.y or last_way_point.z != self.waypoint_msg.z:

				color_image_name = 'color_image' + str(index) + '.png'
				depth_image_name = 'depth_image' + str(index) + '.png'

				bridge = CvBridge()

				cv_image_color = bridge.imgmsg_to_cv2(self.current_color_img_msg, desired_encoding = "passthrough")

				
				cv_image_depth = bridge.imgmsg_to_cv2(self.current_depth_img_msg, desired_encoding = "passthrough")
				img_array = np.array(cv_image_depth, dtype = np.float32)
				cv2.normalize(img_array, img_array, 0, 1, cv2.NORM_MINMAX)

				cv2.imwrite(color_image_folder + color_image_name, cv_image_color)
				cv2.imwrite(depth_image_folder + depth_image_name, img_array*255)

				my_waypoint_msg = str(index) + ',' + str(self.waypoint_msg.x) + ',' + str(self.waypoint_msg.y) + ',' + str(self.waypoint_msg.z)
				f = open(waypoint_folder + waypoint_file_name, 'a')
				f.write(my_waypoint_msg)
				f.write('\n')

				last_way_point = self.waypoint_msg

				index += 1


def main():
	rospy.init_node('collect_data', anonymous=False)
	CollectData()
	rospy.spin()

if __name__ == "__main__":
	main()
