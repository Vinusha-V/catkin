#!/usr/bin/env python3
import rospy

if __name__=="__main__":
    rospy.init_node("testNode")
    rospy.loginfo("Hello")

    

    while not rospy.is_shutdown():
        rospy.loginfo("World")
        rospy.sleep(1)