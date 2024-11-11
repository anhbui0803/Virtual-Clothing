from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1400, 800))
        self.groupBox.setStyleSheet("background-color: rgb(165, 200, 193);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(410, 20, 571, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(50, 670, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(1230, 660, 75, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.search_clothes)

        # Input text box for user search
        self.textEdit = QtWidgets.QLineEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(260, 660, 941, 41))
        self.textEdit.setObjectName("textEdit")

        # Group box for image display
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 100, 500, 500))
        self.groupBox_2.setStyleSheet("background-color: rgb(230, 255, 253);")
        self.groupBox_2.setObjectName("groupBox_2")
        
        # Image label
        self.image_label = QtWidgets.QLabel(self.groupBox_2)
        self.image_label.setGeometry(QtCore.QRect(10, 10, 480, 480))
        self.image_label.setObjectName("image_label")
        self.image_label.setStyleSheet("border: 1px solid black;")
        
        # Group box for clothing options
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(580, 100, 771, 401))
        self.groupBox_3.setObjectName("groupBox_3")
        
        # Buttons for main actions
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(580, 510, 771, 91))
        self.groupBox_4.setStyleSheet("background-color: rgb(237, 255, 241);")
        self.groupBox_4.setObjectName("groupBox_4")
        
        # Sửa khoảng cách và thêm nút mới
        button_width = 81
        button_spacing = 40
        total_buttons = 5
        start_x = (self.groupBox_4.width() - total_buttons * button_width - (total_buttons - 1) * button_spacing) // 2

        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_3.setGeometry(QtCore.QRect(start_x, 30, button_width, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.load_image)
        
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setGeometry(QtCore.QRect(start_x + (button_width + button_spacing), 30, button_width, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.capture_image)

        self.pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton.setGeometry(QtCore.QRect(start_x + 2 * (button_width + button_spacing), 30, button_width, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.try_on_clothes)
        
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_5.setGeometry(QtCore.QRect(start_x + 3 * (button_width + button_spacing), 30, button_width, 31))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.reset_image)
        
        # Nút mở camera
        self.pushButton_open_camera = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_open_camera.setGeometry(QtCore.QRect(start_x + 4 * (button_width + button_spacing), 30, button_width, 31))
        self.pushButton_open_camera.setObjectName("pushButton_open_camera")
        self.pushButton_open_camera.clicked.connect(self.start_camera)

        # Timer để cập nhật video real-time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None  # Biến để lưu camera stream

        # Styling the buttons with rounded corners, hover effects, and colors
        self.set_button_styles()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_button_styles(self):
        # Common style for all buttons
        button_style = """
            QPushButton {
                background-color: rgb(102, 204, 255);
                color: white;
                border-radius: 10px;
                border: 1px solid gray;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(51, 153, 255);
            }
        """
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_4.setStyleSheet(button_style)
        self.pushButton.setStyleSheet(button_style)
        self.pushButton_5.setStyleSheet(button_style)
        self.pushButton_open_camera.setStyleSheet(button_style)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "KHÔNG GIAN THỜI TRANG ẢO"))
        self.label_2.setText(_translate("MainWindow", "Tôi có thể giúp gì cho bạn?"))
        self.pushButton_2.setText(_translate("MainWindow", "TÌM KIẾM"))
        self.pushButton_3.setText(_translate("MainWindow", "TẢI ẢNH"))
        self.pushButton.setText(_translate("MainWindow", "THỬ ĐỒ"))
        self.pushButton_4.setText(_translate("MainWindow", "CHỤP ẢNH"))
        self.pushButton_5.setText(_translate("MainWindow", "QUAY LẠI"))
        self.pushButton_open_camera.setText(_translate("MainWindow", "MỞ CAMERA"))

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            # Resize the image to fit the label
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio))
        else:
            QMessageBox.information(None, "Error", "No image selected")

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.information(None, "Error", "Camera not accessible")
            return
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("captured_image.png", frame)
            self.load_image_from_file("captured_image.png")
        cap.release()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)  # Mở camera
        if not self.cap.isOpened():
            QMessageBox.information(None, "Error", "Camera not accessible")
            return
        self.timer.start(30)  # Cập nhật khung hình mỗi 30ms (tương đương khoảng 33 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Chuyển đổi khung hình từ BGR (mặc định của OpenCV) sang RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio))

    def load_image_from_file(self, file_path):
        pixmap = QtGui.QPixmap(file_path)
        # Resize the image to fit the label
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio))

    def try_on_clothes(self):
        QMessageBox.information(None, "Try Clothes", "Feature to try clothes will be implemented here.")

    def reset_image(self):
        self.image_label.clear()
        if self.cap:
            self.cap.release()  
            self.timer.stop()  

    def search_clothes(self):
        search_query = self.textEdit.text()
        QMessageBox.information(None, "Search", f"You searched for: {search_query}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
