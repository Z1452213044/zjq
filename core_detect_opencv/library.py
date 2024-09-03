import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel
import cv2

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

def cv2_to_pixmap(image):
    if len(image.shape) == 2:
        height, width = image.shape
        bytes_per_line = width
        qimg = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    else:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width if channel == 3 else width
        qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    return pixmap

def find_circle_blob(img):

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(gray_image)

    _, binary_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)

    blurred_image = cv2.GaussianBlur(binary_image, (3, 3), 0)

    edges = cv2.Canny(blurred_image, 30, 80)
    params = cv2.SimpleBlobDetector_Params()

    params.filterByColor = True
    params.blobColor = 255

    params.minThreshold = 10
    params.maxThreshold = 200

    params.filterByArea = True
    params.minArea = 5000
    params.maxArea = 15000

    params.filterByCircularity = True
    params.minCircularity = 0.1

    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    params.filterByConvexity = True
    params.minConvexity = 0.87

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(enhanced_image)
    circle_info = []
    print(f"找到{len(keypoints)}个圆形")

    for kp in keypoints:
        x, y = kp.pt
        x, y = int(x), int(y)
        radius = kp.size / 2
        radius = int(radius)

        circle_info.append((x, y, radius))
        circle_info.sort(key=lambda x:x[0])

    return len(keypoints), circle_info


class CircleCropper:
    def __init__(self, image):
        self.image = image
        if self.image is None:
            raise ValueError(f"Error: Unable to load image ")
        self.cropped_image = None

    def crop_circle(self, center, radius):
        mask = np.zeros_like(self.image, dtype=np.uint8)


        cv2.circle(mask, center, radius, (255, 255, 255), thickness=-1)

        self.cropped_image = cv2.bitwise_and(self.image, mask)

        background_mask = np.ones_like(self.image, dtype=np.uint8) * 255
        background_mask = cv2.bitwise_and(background_mask, cv2.bitwise_not(mask))
        self.cropped_image = cv2.add(self.cropped_image, background_mask)
        return self.cropped_image

    def show_cropped_image(self, title='Cropped Image'):
        if self.cropped_image is None:
            raise ValueError("No cropped image available. Please call crop_circle() first.")

        plt.figure(figsize=(8, 8), dpi=600)
        plt.imshow(cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.show()


class Preprocessing:
    @staticmethod
    def color_binarize_image(img, lower_thresh=[0, 0, 0], upper_thresh=[128, 128, 128], gray_value=1):

        result = []
        # 检查阈值的长度
        assert len(lower_thresh) == 3 and len(upper_thresh) == 3, "阈值长度应为3"

        # 创建掩膜
        for i in range(len(img)):
            image = img[i]
            mask = cv2.inRange(image, np.array(lower_thresh), np.array(upper_thresh))

            # 创建一个全白的图像用于输出
            binary_image = np.full(image.shape[:2], 255, dtype=np.uint8)

            # 应用掩膜，将掩膜内的像素设为对应的灰度值
            binary_image[mask != 0] = gray_value

            # 反转此时的黑白两色
            inverted_image = cv2.bitwise_not(binary_image)
            result.append(inverted_image)

        return result

    @staticmethod
    def extract_channel(images, channel):  # 将其他通道的值改为指定通道的值，而不是将提取当前通道的值
        assert channel in [0, 1, 2], "通道编号应为0（R）、1（G）或2（B）"

        extracted_images = []
        for image in images:
            # 提取指定通道
            channel_image = image[:, :, channel]

            # 创建一个新的图像，所有通道的值都设置为提取的通道值
            extracted_image = np.stack([channel_image, channel_image, channel_image], axis=-1)

            extracted_images.append(extracted_image)

        return extracted_images

    @staticmethod
    def adjust_brightness_contrast_gamma(images, brightness=128, contrast=50, gamma=1.0):  # 亮度、对比度、伽马值的调整
        adjusted_images = []

        for image in images:
            # 调整亮度和对比度
            new_image = cv2.convertScaleAbs(image, alpha=contrast / 50.0, beta=brightness - 128)

            # 调整伽马值
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            new_image = cv2.LUT(new_image, table)

            adjusted_images.append(new_image)

        return adjusted_images

    @staticmethod
    def kernel_init(kernel_shape, kernel_size):
        # 定义形态核形状
        if kernel_shape == 0:
            shape = cv2.MORPH_RECT
        elif kernel_shape == 1:
            shape = cv2.MORPH_CROSS
        elif kernel_shape == 2:
            shape = cv2.MORPH_ELLIPSE
        else:
            raise ValueError("kernel_shape must be 0 (RECT), 1 (CROSS), or 2 (ELLIPSE)")

        # 创建形态核
        kernel = cv2.getStructuringElement(shape, (kernel_size, kernel_size))
        return kernel

    @staticmethod
    def erode_images(images, iterations=1, kernel_size=3, kernel_shape=0):
        kernel = Preprocessing.kernel_init(kernel_shape, kernel_size)
        eroded_images = []
        for image in images:
            # 腐蚀操作
            eroded_image = cv2.erode(image, kernel, iterations=iterations)
            eroded_images.append(eroded_image)

        return eroded_images

    @staticmethod
    def dilate_images(images, iterations=1, kernel_size=3, kernel_shape=0):
        kernel = Preprocessing.kernel_init(kernel_shape, kernel_size)
        dilated_images = []
        for image in images:
            # 膨胀操作
            dilated_image = cv2.dilate(image, kernel, iterations=iterations)
            dilated_images.append(dilated_image)

        return dilated_images

    @staticmethod
    def rotate_and_translate_images(images, x_shift, y_shift, angle):  # 图像列表，x轴y轴平移量， 旋转角度
        processed_images = []
        for image in images:
            # 获取图像中心
            center = (image.shape[1] // 2, image.shape[0] // 2)

            # 计算旋转矩阵
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

            # 添加平移到旋转矩阵
            rotation_matrix[0, 2] += x_shift
            rotation_matrix[1, 2] += y_shift

            # 应用仿射变换
            rotated_translated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
            processed_images.append(rotated_translated_image)

        return processed_images

    @staticmethod
    def open_operation(images, iterations=1, kernel_size=3, kernel_shape=0):
        kernel = Preprocessing.kernel_init(kernel_shape, kernel_size)
        opened_images = []
        for image in images:
            # 开运算操作
            opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=iterations)
            opened_images.append(opened_image)

        return opened_images

    @staticmethod
    def close_operation(images, iterations=1, kernel_size=3, kernel_shape=0):
        kernel = Preprocessing.kernel_init(kernel_shape, kernel_size)
        closed_images = []
        for image in images:
            # 闭运算操作
            closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
            closed_images.append(closed_image)

        return closed_images

    ### blur part

    @staticmethod
    def gaussian_blur(images, kernel_size=(5, 5)):
        blurred_images = []
        for image in images:
            blurred_image = cv2.GaussianBlur(image, kernel_size, 0)
            blurred_images.append(blurred_image)
        return blurred_images

    @staticmethod
    def median_blur(images, kernel_size=5):
        blurred_images = []
        for image in images:
            blurred_image = cv2.medianBlur(image, kernel_size)
            blurred_images.append(blurred_image)
        return blurred_images

    @staticmethod
    def mean_blur(images, kernel_size=(5, 5)):
        blurred_images = []
        for image in images:
            blurred_image = cv2.blur(image, kernel_size)
            blurred_images.append(blurred_image)
        return blurred_images

    @staticmethod
    def manual_image_binarization(image, low_threshold=140, high_threshold=300, threshold_mode='in_range'):
        if threshold_mode == 'in_range':
            _, binarized_image = cv2.threshold(image, low_threshold, 255, cv2.THRESH_BINARY)
        elif threshold_mode == 'out_of_range':
            _, binarized_image = cv2.threshold(image, low_threshold, 255, cv2.THRESH_BINARY_INV)
        else:
            raise ValueError("无效的阈值模式。请选择 'in_range' 或 'out_of_range'")
        return binarized_image

def blob_analysis_best(image, min_area, max_area):
    # 读取图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化图像
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # 初始化 SimpleBlobDetector
    params = cv2.SimpleBlobDetector_Params()

    # 设置面积过滤参数
    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area

    # 创建检测器
    detector = cv2.SimpleBlobDetector_create(params)

    # 检测 Blob
    keypoints = detector.detect(binary_image)

    # 绘制 Blob 区域
    highlighted_image = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # 计算 Blob 个数和面积
    blob_count = len(keypoints)
    blob_areas = [keypoint.size for keypoint in keypoints]

    return blob_count, blob_areas, highlighted_image