import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel


def array_to_pixmap(image_array):
    # 假设图像数组的形状为 (height, width, channels)
    height, width, channels = image_array.shape
    if channels == 3:
        # RGB 图像
        img = plt.imshow(image_array)
        img.set_cmap('viridis')
        plt.axis('off')
        plt.draw()
        fig = plt.gcf()
        fig.canvas.draw()
        data = fig.canvas.tostring_rgb()
        qimage = QImage(data, width, height, QImage.Format_RGB888)
    elif channels == 1:
        # 灰度图像
        img = plt.imshow(image_array, cmap='gray')
        plt.axis('off')
        plt.draw()
        fig = plt.gcf()
        fig.canvas.draw()
        data = fig.canvas.tostring_rgb()
        qimage = QImage(data, width, height, QImage.Format_Grayscale8)
    else:
        raise ValueError(f"不支持的图像通道数：{channels}")
    pixmap = QPixmap.fromImage(qimage)
    return pixmap