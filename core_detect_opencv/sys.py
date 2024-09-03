import os
import sys
import cv2
import numpy as np

from library import*
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self,parent=None):
        self.parent = parent
        self.img_path_tem=''#用于各个方法之间传递临时文件路径
        self.img_path_org=''#用于各个方法之间传递文件路径
        self.img_temp_cv2=np.zeros((100, 100, 3), dtype=np.uint8)#临时传递图片

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1318, 1004)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 730, 181, 61))
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 1301, 591))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")




        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)



        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)





        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 810, 181, 61))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 810, 181, 61))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 890, 181, 61))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(250, 730, 181, 61))
        self.pushButton_7.setObjectName("pushButton_7")

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 660, 1301, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_6.setObjectName("pushButton_6")

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_5.setObjectName("pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(250, 890, 181, 61))
        self.pushButton_8.setObjectName("pushButton_8")

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(770, 710, 531, 271))
        self.textBrowser.setObjectName("textBrowser")




        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.blob_find_circle)
        #self.pushButton_2.clicked.connect(self.defect_detect)
        self.pushButton_3.clicked.connect(self.ROI_set)
        self.pushButton_4.clicked.connect(self.binarization)
        self.pushButton_7.clicked.connect(self.defect_detect)
        self.pushButton_6.clicked.connect(self.import_img)
        self.pushButton_5.clicked.connect(self.save_img)
        self.pushButton_8.clicked.connect(self.enhance_img)

        ##
        self.verticalLayoutwidget = QtWidgets.QWidget(Form)
        self.verticalLayoutwidget.setGeometry(QtCore.QRect(1, 1, 1310, 80))
        self.verticalLayoutwidget.setObjectName("VLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName('VLayout')

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutwidget)
        self.label_3.setFixedWidth(1318)
        self.label_3.setFixedHeight(80)
        self.label_3.setObjectName("label_3")
        pixmap = QtGui.QPixmap(r'C:\Users\zjq\Desktop\Pyqt-opencv\icon_title_1.jpg')
        self.label_3.setPixmap(pixmap)

        self.line_v = QtWidgets.QFrame(self.verticalLayoutwidget)
        self.line_v.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_v.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_v.setObjectName("line_v")

        self.verticalLayout.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.line_v)

    ##

    def defect_detect(self):
        self.textBrowser.setText("--------------------------")
        self.textBrowser.append("#####芯位置检测#####")
        img=self.img_temp_cv2
        num, info = find_circle_blob(img)

        center_circle = []
        radius_circle = []
        for x, y, z in info:
            center_circle.append((x, y))
            radius_circle.append(z - 2)  # 去边缘操作


        if num == 0:
            self.textBrowser.setText("未检测到圆\n或\n检测图像非光纤跳线芯，请导入光纤条线芯的图片！")
        else:

            ###裁剪圆储存在列表里
            crop_img_list = []
            scratch_images = []
            diff_x = [center_circle[i + 1][0] - center_circle[i][0] for i in range(len(center_circle) - 1)]
            if center_circle[0][1] < 400:
                for i in range(len(diff_x)):
                    if 350 < diff_x[i] < 450:
                        break
                    else:
                        self.textBrowser.append("第" + str(i + 1) + "个芯位置异常")
            else:
                self.textBrowser.append("第一个芯位置异常")
            self.textBrowser.append("--------------------------")

            for i in range(num):
                circle_crop = CircleCropper(img)
                cropped_img_circle = circle_crop.crop_circle(center_circle[i], radius_circle[i])
                crop_img_list.append(cropped_img_circle)
            self.textBrowser.append("#####芯划痕检测#####")

            for n in range(num):
                # 裁剪一个圆
                c = CircleCropper(crop_img_list[n])
                img_circle_cropped = c.crop_circle(center_circle[n], radius_circle[n])
                # 创建一个预处理类的对象，进行二值化操作
                P = Preprocessing()
                binarized_image = P.manual_image_binarization(image=img_circle_cropped, threshold_mode='in_range')
                # Blob分析检测划痕设置最大最小区域
                min_area = 5
                max_area = 1000
                blob_count, blob_areas, highlighted_image = blob_analysis_best(binarized_image, min_area, max_area)

                if blob_count > 0:
                    self.textBrowser.append('第' + str(n + 1) + '个芯表面有划痕，划痕个数为 ' + str(blob_count))
                    scratch_images.append(highlighted_image)
                else:
                    self.textBrowser.append('第' + str(n + 1) + '个芯表面良好')
            combined_image = np.zeros_like(img)
            alpha = 0.8  # 设置透明度
            for scratch_image in scratch_images:
                combined_image = cv2.addWeighted(combined_image, 1 - alpha, scratch_image, alpha, 0)

            pixmap = cv2_to_pixmap(combined_image)
            scaled_pixmap = pixmap.scaled(645, 645, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_2.setPixmap(scaled_pixmap)
            self.textBrowser.append("--------------------------")
            self.textBrowser.append('检测结果如上图所示\n红色为识别到的杂质\n如效果不明显请去源代码调整参数')
            cv2.imwrite('defect.jpg', combined_image)
            self.textBrowser.append('结果已保存在同目录下defect.jpg')


    def ROI_set(self):
        self.textBrowser.setText("正在开发中。。。")
        pass

    def enhance_img(self):
        self.textBrowser.setText("正在开发中。。。")
        pass

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OPENCV-based fiber patch core defect detection"))
        self.pushButton.setText(_translate("Form", "Blob-找圆"))
        # self.label_3.setText(_translate("Form", "基于OPEN_CV的光纤跳线芯缺陷检测"))

        self.pushButton_2.setText(_translate("Form", "待定"))
        self.pushButton_3.setText(_translate("Form", "ROI设定"))
        self.pushButton_4.setText(_translate("Form", "二值化"))
        self.pushButton_7.setText(_translate("Form", "缺陷检测"))
        self.pushButton_6.setText(_translate("Form", "导入图像"))
        self.pushButton_5.setText(_translate("Form", "保存图像"))
        self.pushButton_8.setText(_translate("Form", "图像增强"))

    def import_img(self):
        # 获取当前窗口对象，假设 form 是在 setupUi 方法中创建的 QWidget 对象
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self.parent, '打开文件', '.', '图形文件 (*.jpg *.png *.bmp)')
        self.img_path_org = fname  # 文件路径储存在变量里
        pixmap = QtGui.QPixmap(fname)
        scaled_pixmap = pixmap.scaled(645, 645, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled_pixmap)
        if fname:

            self.img_temp_cv2 = cv2.imread(fname)
            #self.img_temp_cv2 = cv2.cvtColor(self.img_temp_cv2, cv2.COLOR_BGR2RGB)
            # cv2.imshow('img',self.img_temp_cv2)
        else:
            print("未导入图片")
    def save_img(self):
        if self.label_2.pixmap() == None:
            self.textBrowser.setText("上述窗口没有保存的图片！" )
        else:
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self.parent, "另存为", "",
                                                       "图片文件 (*.png *.jpg *.jpeg);;所有文件 (*)",
                                                       options=options)
            if file_name:
                pixmap = self.label_2.pixmap()
                if pixmap:
                    pixmap.save(file_name)
                    self.textBrowser.setText("已经保存至：" + str(file_name))

            else:
                self.textBrowser.setText("保存失败，原因：未给出路径")

    def blob_find_circle(self):
        gray_image = cv2.cvtColor(self.img_temp_cv2, cv2.COLOR_BGR2GRAY)

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
            circle_info.sort(key=lambda x: x[0])
        tem_dialog=f"找到了 {len(keypoints)} 圆形"+"\n"+"坐标以及半径信息："+str(circle_info)
        self.textBrowser.setText(tem_dialog)
        QApplication.processEvents()
    def binarization(self):
        gray_image = cv2.cvtColor(self.img_temp_cv2, cv2.COLOR_BGR2GRAY)
        threshold_mode='in_range'
        if threshold_mode == 'in_range':
            _, binarized_image = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)
        elif threshold_mode == 'out_of_range':
            _, binarized_image = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY_INV)
        else:
            raise ValueError("无效的阈值模式。请选择 'in_range' 或 'out_of_range'")

        pixmap=cv2_to_pixmap(binarized_image)
        scaled_pixmap = pixmap.scaled(645, 645, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_2.setPixmap(scaled_pixmap)
        self.textBrowser.setText("图像已二值化，如上图所示")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())