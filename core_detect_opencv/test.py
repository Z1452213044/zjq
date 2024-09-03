import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import*
import cv2
import numpy as np
def manual_image_binarization(image, low_threshold=140, high_threshold=300, threshold_mode='in_range'):
    if threshold_mode == 'in_range':
        _, binarized_image = cv2.threshold(image, low_threshold, 255, cv2.THRESH_BINARY)
    elif threshold_mode == 'out_of_range':
        _, binarized_image = cv2.threshold(image, low_threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        raise ValueError("无效的阈值模式。请选择 'in_range' 或 'out_of_range'")
    return binarized_image

img = cv2.imread(r'C:\Users\zjq\Desktop\train_3.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
binarized_image = manual_image_binarization(img)



cv2.imshow('binarized_image', binarized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
