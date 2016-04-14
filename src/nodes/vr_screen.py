#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from algos import *
import ovrsdk as ovr
import message_filters



class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    left_sub = message_filters.Subscriber('/stereo/left/image', Image)
    right_sub = message_filters.Subscriber('/stereo/right/image', Image)
    ts = message_filters.TimeSynchronizer([left_sub, right_sub], 10)
    ts.registerCallback(self.callback)

  def cropcrop(self,frame):
            par = Parameters
            matrix = create_distortion_matrix(
                par.fxL, par.cxL, par.fyL, par.cyL
            )
            frame = translate(frame, par.xL + par.xo, par.yL + par.yo)
            frame = transform(frame, matrix)
            frame = translate(frame, par.xo2, par.yo2)

            frame = crop(
                frame,
                par.cropXL,
                par.cropXR,
                par.cropYL,
                par.cropYR,
            )
	    return frame


  def callback(self,left,right):
    try:
      left_frame = self.bridge.imgmsg_to_cv2(left, "bgr8")
      right_frame = self.bridge.imgmsg_to_cv2(right, "bgr8")
    except CvBridgeError as e:
      print(e)

    cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)

    left_frame=self.cropcrop(left_frame)
    right_frame=self.cropcrop(right_frame)

    #put two images together
    composite_frame = join_images(
                left_frame,
                right_frame,
    )
    cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
    cv2.imshow("test", composite_frame)
    cv2.waitKey(3)

def main(args):

  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

