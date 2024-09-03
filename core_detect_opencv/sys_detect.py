import os
import sys
import cv2
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from array_to_pixmap import array_to_pixmap
from library import cv2_to_pixmap

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


########
        self.verticalLayoutwidget=QtWidgets.QWidget(Form)
        self.verticalLayoutwidget.setGeometry(QtCore.QRect(1,1, 1310, 80))
        self.verticalLayoutwidget.setObjectName("VLayoutWidget")

        self.verticalLayout=QtWidgets.QVBoxLayout(self.verticalLayoutwidget)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName('VLayout')

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutwidget)
        self.label_3.setFixedWidth(1318)
        self.label_3.setFixedHeight(80)
        self.label_3.setObjectName("label_3")
        pixmap=QtGui.QPixmap('icon_title_1.jpg')
        self.label_3.setPixmap(pixmap)



        self.line_v =QtWidgets.QFrame(self.verticalLayoutwidget)
        self.line_v.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_v.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_v.setObjectName("line_v")

        self.verticalLayout.addWidget(self.label_3)
        self.verticalLayout.addWidget(self.line_v)



#######


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
        print(self.label_3.width())
        print(self.label_3.height())
        print(self.verticalLayoutwidget.geometry())
        print("Vertical layout has widgets:", self.verticalLayout.count() > 0)
        print(self.verticalLayoutwidget.geometry())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())