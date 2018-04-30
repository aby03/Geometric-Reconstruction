import numpy as np
import imutils
import cv2

def rotateImage(image, angle):
    rotated = imutils.rotate(image, angle)

    return rotated
