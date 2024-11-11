from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from ultralytics import YOLO

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1322, 851)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1321, 831))
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 240);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        # Frame to show person image
        self.label_person = QLabel(self.groupBox)
        self.label_person.setGeometry(QtCore.QRect(90, 40, 500, 340))
        self.label_person.setStyleSheet("background-color: rgb(167, 175, 200);")
        self.label_person.setObjectName("label_person")

        # Frame to show clothes image
        self.label_clothes = QLabel(self.groupBox)
        self.label_clothes.setGeometry(QtCore.QRect(700, 40, 500, 340))
        self.label_clothes.setStyleSheet("background-color: rgb(239, 243, 255);")
        self.label_clothes.setObjectName("label_clothes")

        # Frame to show final merged image
        self.label_result = QLabel(self.groupBox)
        self.label_result.setGeometry(QtCore.QRect(90, 410, 500, 340))
        self.label_result.setStyleSheet("background-color: rgb(240, 255, 252);")
        self.label_result.setObjectName("label_result")

        # Buttons
        self.pushButton = self.create_button("Thêm ảnh person", 700, 440, 121, 41, self.add_person_image)
        self.pushButton_2 = self.create_button("Thêm đồ", 700, 510, 121, 41, self.add_clothes_image)
        self.pushButton_3 = self.create_button("Xử lý ảnh person", 880, 440, 121, 41, self.process_person_image)
        self.pushButton_4 = self.create_button("Xử lý ảnh đồ", 880, 510, 121, 41, self.process_clothes_image)
        self.pushButton_5 = self.create_button("Ghép ảnh", 800, 590, 121, 41, self.merge_images)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1322, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Variables to store images
        self.person_image = None
        self.clothes_image = None
        self.yolo_model = YOLO(r'D:\Shop_Thoi_Trang_Ao\YOLO_Person\runs\detect\train\weights\best.pt')  # Load YOLO model

    def create_button(self, text, x, y, width, height, func):
        button = QtWidgets.QPushButton(self.groupBox)
        button.setGeometry(QtCore.QRect(x, y, width, height))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        button.setFont(font)
        button.setStyleSheet("""
            QPushButton {
                background-color: rgb(157, 205, 255);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgb(100, 160, 255);
            }
        """)
        button.setText(text)
        button.clicked.connect(func)
        return button

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    # Function to load person image
    def add_person_image(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Chọn ảnh person", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.label_person.setPixmap(pixmap.scaled(self.label_person.size(), QtCore.Qt.KeepAspectRatio))
            self.person_image = cv2.imread(file_name)  # Load image for processing

    # Function to load clothes image
    def add_clothes_image(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Chọn ảnh đồ", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.label_clothes.setPixmap(pixmap.scaled(self.label_clothes.size(), QtCore.Qt.KeepAspectRatio))
            self.clothes_image = cv2.imread(file_name)  # Load image for processing

    # Placeholder for processing person image (using YOLO model)
    def process_person_image(self):
        if self.person_image is not None:
            print("Processing person image...")
            results = self.yolo_model(self.person_image)
            # Only focus on the detected shirt region
            self.shirt_mask = self.get_mask_from_results(results)
            self.masked_person_image = cv2.bitwise_and(self.person_image, self.person_image, mask=self.shirt_mask)
            self.display_image(self.masked_person_image, self.label_person)

    # Function to create mask from YOLO results for shirt
    def get_mask_from_results(self, results):
        mask = np.zeros(self.person_image.shape[:2], dtype=np.uint8)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                mask[y1:y2, x1:x2] = 255  # Mask the shirt area
        return mask

    # Function to display image in QLabel
    def display_image(self, img, label):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        label.setPixmap(QtGui.QPixmap.fromImage(q_img).scaled(label.size(), QtCore.Qt.KeepAspectRatio))

    # Function to process clothes image and extract the shirt
    def process_clothes_image(self):
        if self.clothes_image is not None:
            print("Processing clothes image...")
            self.clothes_mask = self.create_clothes_mask(self.clothes_image)
            self.segmented_clothes = cv2.bitwise_and(self.clothes_image, self.clothes_image, mask=self.clothes_mask)
            self.display_image(self.segmented_clothes, self.label_clothes)

    # Function to create a mask for the clothes image (basic background removal)
    def create_clothes_mask(self, img):
        # Simple background subtraction or thresholding method to segment the clothes
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_color = np.array([0, 0, 0])  # Adjust this threshold for better segmentation
        upper_color = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        return mask

    # Function to merge images
    def merge_images(self):
        if self.masked_person_image is not None and self.segmented_clothes is not None:
            print("Merging images...")
            # Resize clothes image to match the mask area
            x1, y1, x2, y2 = self.get_clothes_position_from_mask()  # Get the position for the new clothes
            resized_clothes = cv2.resize(self.segmented_clothes, (x2 - x1, y2 - y1))

            # Place the new clothes on top of the masked person image
            result_image = self.masked_person_image.copy()
            result_image[y1:y2, x1:x2] = resized_clothes
            self.display_image(result_image, self.label_result)

    # Function to get position for clothes placement (from YOLO detection results)
    def get_clothes_position_from_mask(self):
        # You can calculate the exact position from YOLO results here
        return 100, 150, 300, 400  # Example values, use real coordinates

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
