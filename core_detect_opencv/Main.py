
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ultralytics import YOLOv10
import os

class Q_core_detect(QWidget):
    def __init__(self):
        super(Q_core_detect, self).__init__()
        self.initUI()
        self.resize(1600,900)
        self.img_path_org=''
    # 编写初始化方法
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('光纤跳线芯-缺陷检测')

        main_layout = QVBoxLayout()
        layout_layout = QHBoxLayout()
        # 创建垂直布局
        layout_v1= QVBoxLayout()
        layout_v2= QVBoxLayout()

        self.Label_org_img = QLabel(self)
        self.Label_processed_img = QLabel(self)

        self.button_import_img=QPushButton('加载图片')
        self.button_save_img = QPushButton('保存结果')
        self.button_predict = QPushButton('运行检测')



        self.button_import_img.clicked.connect(self.loadImage)
        self.button_save_img.clicked.connect(self.saveImage)
        self.button_predict.clicked.connect(self.process)

        layout_v1.addWidget(self.Label_org_img)
        layout_v1.addWidget(self.button_import_img)
        layout_v2.addWidget(self.Label_processed_img)
        layout_v2.addWidget(self.button_save_img)

        layout_layout.addLayout(layout_v1)
        layout_layout.addLayout(layout_v2)

        main_layout.addLayout(layout_layout)
        main_layout.addWidget(self.button_predict)

        self.setLayout(main_layout)

    # 槽方法
    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '图形文件 (*.jpg *.png *.bmp)')
        self.img_path_org=fname#文件路径储存在变量里

        pixmap = QPixmap(fname)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.Label_org_img.setPixmap(scaled_pixmap)

    def saveImage(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "另存为", "", "图片文件 (*.png *.jpg *.jpeg);;所有文件 (*)", options=options)
        if file_name:
            pixmap = self.Label_processed_img.pixmap()
            if pixmap:
                pixmap.save(file_name)
        else:
            print("未给出路径")
        pass
    def process(self):
        #调用YOLO v10模型
        model = YOLOv10("best.pt")
        results = model.predict(source=self.img_path_org, imgsz=640, conf=0.3, save=True)
        save_Dir = results[0].save_dir
        path_processed_img = os.path.join(save_Dir, os.path.basename(self.img_path_org))
        print(path_processed_img)
        # self.Label_processed_img.setPixmap(QPixmap(path_processed_img))

        pixmap = QPixmap(path_processed_img)
        scaled_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.Label_processed_img.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Q_core_detect()
    main.show()
    sys.exit(app.exec_())


