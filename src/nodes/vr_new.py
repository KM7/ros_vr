#!/usr/bin/env python
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from algos import *
import message_filters

class image_converter:

  def __init__(self):
    rospy.init_node('image_converter', anonymous=True)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/stereo/left/image_raw",Image,self.callback_left)
    self.image_sub = rospy.Subscriber("/stereo/right/image_raw",Image,self.callback_right)
    self.left=[]
    self.right=[]

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

  def callback_left(self,data):
    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    self.left=cv_image

  def callback_right(self,data):
    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    self.right=cv_image

  def virtualize(self):
    rate = rospy.Rate(30) # 10hz
    while not rospy.is_shutdown():
	if (self.left!=[] and self.right!=[]):
	    left_frame=self.cropcrop(cv2.flip(self.left,1))
	    right_frame=self.cropcrop(cv2.flip(self.right,1))

	    #put two images together
	    composite_frame = join_images(
		        right_frame,
                        left_frame,
	    )
            composite_frame=cv2.transpose(composite_frame)
            cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
            cv2.imshow("test",composite_frame)
    	    cv2.waitKey(3)
        rate.sleep()



def main(args):
  ic = image_converter()
  ic.virtualize()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

