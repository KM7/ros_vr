#!/usr/bin/env python
import cv2
import numpy as np

img = np.zeros((900, 1600)) #my aspect ratio is 16x9
cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
cv2.imshow("test",img)
cv2.waitKey(0)
