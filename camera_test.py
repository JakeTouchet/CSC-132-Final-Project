# Program that take picture with opencv and outputs the color of the center pixel
import cv2
import numpy as np
import time
import os
import sys



def takePicture():
    # Take picture
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

    # Get color of center pixel
    center = frame[int(frame.shape[0]/2), int(frame.shape[1]/2)]
    return center


def main():
    # Take picture
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Get color of center pixel
    center = frame[int(frame.shape[0]/2), int(frame.shape[1]/2)]

    # Print color
    print(center)

    # Show picture
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()