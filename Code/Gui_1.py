from ultralytics import YOLO
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import os
import cv2
import numpy as np

# Định nghĩa các từ khóa cho loại sản phẩm và màu sắc
product_types = ['áo sơ mi', 'áo thun', 'áo',
                 'nón', 'quần', 'váy', 'giày', 'hoodie']
colors = ['đỏ', 'xanh', 'vàng', 'đen', 'trắng', 'nâu', 'tím', 'hồng']

# Đường dẫn tới hình ảnh sản phẩm
product_images = {
    'áo sơ mi': {
        'trắng': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (52).png",
                  r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (51).png",
                  r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (44).png"],
        'đen': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (47).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (50).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (49).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (41).png"],
        'xanh': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (48).png",
                 r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (53).png",
                 r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (39).png",],
        'nâu': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (37).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (40).png",]
    },
    'áo thun': {
        'trắng': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (61).png",
                  r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (60).png",
                  r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (31).png",
                  r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (30).png"],
        'đen': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (59).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (58).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (1).png",
                r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (34).png"],
        'xanh': [r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (63).png",
                 r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (62).png",
                 r"D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\image\abc (54).png"]
    }
}

# Hàm trích xuất nhãn từ mô tả sản phẩm


def extract_labels(description):
    description = description.lower()
    product_type = next((p for p in product_types if p in description), 'khác')
    color = next((c for c in colors if c in description), 'không rõ')
    return pd.Series([product_type, color])

# Tạo một class QLabel custom để có thể nhận sự kiện click


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 890)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Groupbox tổng
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1500, 890))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("background-color: rgb(198, 226, 255);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        # Tiêu đề
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(330, 10, 951, 81))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Khung camera
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 110, 500, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.groupBox_2.setObjectName("groupBox_2")
        # Thêm QLabel để hiển thị hình ảnh từ camera
        self.label_img_1 = QtWidgets.QLabel(self.groupBox_2)
        # Tùy chỉnh vị trí và kích thước
        self.label_img_1.setGeometry(QtCore.QRect(10, 30, 480, 460))
        self.label_img_1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_img_1.setObjectName("label_img_1")
        # Khung gợi ý sản phẩm với thanh cuộn
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(530, 110, 951, 500))
        self.scrollArea.setStyleSheet("background-color: rgb(219, 255, 234);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 949, 498))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Khung nhập liệu và nút tìm kiếm
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(160, 620, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(410, 620, 681, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(1110, 620, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(131, 139, 131);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_search_click)

        # Khung chứa các thuộc tính đã tìm kiếm
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 660, 221, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet("background-color: rgb(254, 255, 224);")
        self.groupBox_4.setObjectName("groupBox_4")

        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser.setGeometry(QtCore.QRect(10, 30, 201, 141))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowser.setObjectName("textBrowser")

        # MENU và các nút chức năng
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(250, 660, 1231, 181))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setStyleSheet("background-color: rgb(240, 255, 205);")
        self.groupBox_5.setObjectName("groupBox_5")

        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 30, 231, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")

        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 40, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 80, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_3.setObjectName("pushButton_3")

        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_7.setGeometry(QtCore.QRect(250, 30, 971, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setObjectName("groupBox_7")

        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_5.setGeometry(QtCore.QRect(170, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_6.setGeometry(QtCore.QRect(300, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_7.setGeometry(QtCore.QRect(430, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_8.setGeometry(QtCore.QRect(560, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyle
        self.pushButton_8.setObjectName("pushButton_8")

        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_9.setGeometry(QtCore.QRect(690, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_9.setObjectName("pushButton_9")

        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_10.setGeometry(QtCore.QRect(820, 50, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setStyleSheet(
            "background-color: rgb(235, 246, 255);")
        self.pushButton_10.setObjectName("pushButton_10")
        # Thiết kế giao nút nhấn
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;   /* Màu nền */
                color: white;                /* Màu chữ */
                border-radius: 10px;         /* Bo tròn góc */
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;   /* Màu nền khi di chuột */
            }
        """)

        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: #E0F4FF;
                color: black;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #B4E1FF;
            }
        """)

        self.pushButton_3.setStyleSheet("""
            QPushButton {
                background-color: #E0F4FF;
                color: black;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #B4E1FF;
            }
        """)

        self.pushButton_4.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_5.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_6.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_7.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_8.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_9.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        self.pushButton_10.setStyleSheet("""
            QPushButton {
                background-color: #83A8BF;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4E8CBF;
            }
        """)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # # Tạo một QLabel để hiển thị ảnh kết quả thử đồ (result_frame)
        # self.result_frame = QtWidgets.QLabel(self.centralwidget)
        # self.result_frame.setGeometry(QtCore.QRect(900, 110, 500, 500))
        # self.result_frame.setStyleSheet("background-color: rgb(240, 240, 240);")
        # self.result_frame.setObjectName("result_frame")
        # Tạo model YOLO cho phân đoạn người và áo
        self.yolo_model_for_person = YOLO(
            r'D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt')
        self.yolo_model_for_shirt = YOLO(
            r'D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\Model\best.pt')

        # Biến lưu ảnh người và áo
        self.person_img = None
        self.shirt_img = None
        self.selected_product_image = None
        self.mask_person_img = None
        self.mask_shirt_img = None

        # Kết nối các nút với các chức năng tương ứng
        self.pushButton.clicked.connect(self.on_search_click)
        self.pushButton_2.clicked.connect(self.on_edit_click)
        self.pushButton_3.clicked.connect(self.on_save_click)
        self.pushButton_4.clicked.connect(self.on_camera_on_click)
        self.pushButton_5.clicked.connect(self.on_take_picture_click)
        self.pushButton_6.clicked.connect(self.on_add_image_click)
        self.pushButton_7.clicked.connect(self.on_try_on_click)
        self.pushButton_8.clicked.connect(self.on_save_image_click)
        self.pushButton_9.clicked.connect(self.on_camera_off_click)
        self.pushButton_10.clicked.connect(self.on_reset_click)

    def on_search_click(self):
        description = self.lineEdit.text()
        labels = extract_labels(description)
        result_text = f"""
        <b><span style="font-size:10pt;">Loại sản phẩm:</span></b> {labels[0]}<br>
        <b><span style="font-size:10pt;">Màu sắc:</span></b> {labels[1]}<br>
        """
        self.textBrowser.setHtml(result_text)

        product_type, color = labels[0], labels[1]
        if product_type in product_images and color in product_images[product_type]:
            images = product_images[product_type][color]
            self.update_product_images(images)

    def on_edit_click(self):
        # Lấy nội dung hiện tại từ ô tìm kiếm
        current_text = self.lineEdit.text()

        # Kiểm tra nếu nội dung không rỗng
        if current_text:
            # Trích xuất loại sản phẩm và màu sắc từ mô tả
            labels = extract_labels(current_text)

            # Hiển thị thuộc tính đã trích xuất lên textBrowser để người dùng chỉnh sửa
            edit_text = f"""
            <b><span style="font-size:10pt;">Loại sản phẩm:</span></b> {labels[0]}<br>
            <b><span style="font-size:10pt;">Màu sắc:</span></b> {labels[1]}<br>
            """
            self.textBrowser.setHtml(edit_text)
            # Thông báo cho người dùng đã sẵn sàng để chỉnh sửa
            QtWidgets.QMessageBox.information(
                None, "Chỉnh sửa", "Bạn có thể chỉnh sửa các thuộc tính và lưu lại để cập nhật.")
        else:
            QtWidgets.QMessageBox.warning(
                None, "Lỗi", "Không có nội dung để chỉnh sửa.")

    def on_save_click(self):
        # Lấy nội dung hiện tại từ ô tìm kiếm
        new_text = self.lineEdit.text()

        # Kiểm tra nếu nội dung không rỗng
        if new_text:
            # Trích xuất loại sản phẩm và màu sắc từ mô tả đã chỉnh sửa
            new_labels = extract_labels(new_text)

            # Cập nhật lại thuộc tính tìm kiếm trong `textBrowser`
            updated_text = f"""
            <b><span style="font-size:10pt;">Loại sản phẩm:</span></b> {new_labels[0]}<br>
            <b><span style="font-size:10pt;">Màu sắc:</span></b> {new_labels[1]}<br>
            """
            self.textBrowser.setHtml(updated_text)

            # Cập nhật danh sách ảnh sản phẩm phù hợp với thuộc tính mới
            product_type, color = new_labels[0], new_labels[1]
            if product_type in product_images and color in product_images[product_type]:
                images = product_images[product_type][color]
                self.update_product_images(images)

            # Thông báo rằng thuộc tính đã được cập nhật
            QtWidgets.QMessageBox.information(
                None, "Lưu thuộc tính", "Thuộc tính đã được lưu và cập nhật thành công.")
        else:
            QtWidgets.QMessageBox.warning(
                None, "Lỗi", "Không có thuộc tính để lưu.")

    def on_camera_on_click(self):
        # Bật camera và hiển thị hình ảnh
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Cannot open camera")
            return
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(
                rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(convert_to_Qt_format)
            # Đảm bảo rằng self.label_img_1 đã được khởi tạo
            self.label_img_1.setPixmap(pixmap)

            # Dừng lại sau 30ms
            cv2.waitKey(30)

    def on_take_picture_click(self):
        # Chụp ảnh từ camera và hiển thị trên khung hình camera
        if hasattr(self, 'cap'):
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite('captured_image.png', frame)  # Lưu ảnh vào file
                pixmap = QtGui.QPixmap('captured_image.png')
                self.label_img_1.setPixmap(pixmap)

    def load_person_image(self):
        # Mở hộp thoại để chọn ảnh người
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Chọn Ảnh Người", "", "Image Files (*.png *.jpg *.bmp)")

        if file_name:
            # Đọc ảnh và hiển thị ảnh gốc trên giao diện
            self.person_img = cv2.imread(file_name)
            self.display_image(self.person_img, self.label_img_1)

            # Chuyển đổi ảnh sang RGB để xử lý với YOLO model
            person_img_rgb = cv2.cvtColor(self.person_img, cv2.COLOR_BGR2RGB)

            # Thực hiện phân đoạn (segmentation) với YOLO model cho ảnh người
            results = self.yolo_model_for_person(person_img_rgb)

            # Kiểm tra kết quả phân đoạn và tạo mặt nạ
            if results[0].masks is not None:
                self.mask_person_img = (
                    results[0].masks.data[0].cpu().numpy() * 255).astype("uint8")
                print("Phân đoạn ảnh người thành công!")
            else:
                # Hiển thị thông báo nếu không thể phân đoạn
                QtWidgets.QMessageBox.warning(
                    None, "Warning", "Không thể phân đoạn ảnh người. Vui lòng thử ảnh khác!")
                self.mask_person_img = None

    def on_add_image_click(self):
        # Đường dẫn tới mô hình YOLO được huấn luyện cho phân đoạn
        model_path = r'D:\QuocAnh\Nam4_Ky1\Do an tot nghiep\Shop_Thoi_Trang_Ao\Model\hihi.pt'
        # model_path = r'D:\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt'
        yolo_model = YOLO(model_path)  # Tải mô hình YOLO cho phân đoạn áo

        # Mở hộp thoại để người dùng chọn ảnh người
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Chọn Ảnh Người", "", "Image Files (*.png *.jpg *.bmp)", options=options)

        if file_name:
            # Đọc ảnh và hiển thị ảnh gốc trên giao diện
            self.person_img = cv2.imread(file_name)
            # Hiển thị ảnh gốc trong label
            self.display_image(self.person_img, self.label_img_1)

            # Chuyển đổi ảnh sang RGB để xử lý với YOLO model
            person_img_rgb = cv2.cvtColor(self.person_img, cv2.COLOR_BGR2RGB)

            # Thực hiện phân đoạn bằng YOLO model
            results = yolo_model(person_img_rgb)

            # Kiểm tra kết quả phân đoạn
            if results[0].masks is not None:
                # Tạo mặt nạ phân đoạn và lưu vào biến
                self.mask_person_img = (
                    results[0].masks.data[0].cpu().numpy() * 255).astype("uint8")
                print("Đã thực hiện phân đoạn thành công!")
                QtWidgets.QMessageBox.information(
                    None, "Thông báo", "Đã thực hiện phân đoạn thành công!")
            else:
                # Hiển thị thông báo nếu không thể phân đoạn
                QtWidgets.QMessageBox.warning(
                    None, "Lỗi", "Không thể phân đoạn ảnh này. Vui lòng thử ảnh khác!")
                self.mask_person_img = None

    # def on_try_on_click(self):
    #     # Kiểm tra nếu ảnh người và mask của người đã sẵn sàng
    #     if self.person_img is None or self.mask_person_img is None:
    #         QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng thêm và phân đoạn ảnh người trước!")
    #         return

    #     # Kiểm tra nếu sản phẩm áo đã được chọn
    #     if self.selected_product_image is None:
    #         QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng chọn sản phẩm trước khi thử đồ!")
    #         return

    #     # Đọc ảnh áo đã chọn và phân đoạn áo
    #     self.shirt_img = cv2.imread(self.selected_product_image)
    #     self.mask_shirt()

    #     # Kiểm tra và ghép áo vào ảnh người
    #     if self.mask_shirt_img is not None:
    #         self.merge_clothes()
    #     else:
    #         QtWidgets.QMessageBox.warning(None, "Warning", "Không thể phân đoạn áo. Vui lòng thử ảnh khác!")

    def on_save_image_click(self):
        # Kiểm tra nếu ảnh đã ghép tồn tại trên giao diện
        if self.label_img_1.pixmap() is not None:
            # Lấy nội dung của QLabel dưới dạng QPixmap
            pixmap = self.label_img_1.pixmap()

            # Chuyển QPixmap thành QImage để lưu
            image = pixmap.toImage()

            # Đặt đường dẫn thư mục lưu ảnh
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(
                None, "Chọn thư mục lưu ảnh")

            # Nếu người dùng chọn thư mục
            if folder_path:
                # Tạo tên file với ngày giờ hiện tại để tránh trùng lặp
                file_path = os.path.join(
                    folder_path, f"saved_image_{QtCore.QDateTime.currentDateTime().toString('yyyyMMdd_HHmmss')}.png")

                # Lưu QImage vào đường dẫn chỉ định
                if image.save(file_path, "PNG"):
                    QtWidgets.QMessageBox.information(
                        None, "Lưu ảnh", f"Ảnh đã được lưu thành công tại {file_path}")
                else:
                    QtWidgets.QMessageBox.warning(
                        None, "Lỗi", "Không thể lưu ảnh. Vui lòng thử lại.")
        else:
            QtWidgets.QMessageBox.warning(
                None, "Lỗi", "Không có ảnh nào để lưu.")

    def on_camera_off_click(self):
        # Tắt camera
        if hasattr(self, 'cap'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.label_img_1.clear()

    def on_product_click(self, index):
        # Lấy đường dẫn hình ảnh từ danh sách image_paths
        if index < len(self.image_paths):
            self.selected_product_image = self.image_paths[index]
            QtWidgets.QMessageBox.information(
                None, "Sản phẩm đã chọn", f"Bạn đã chọn sản phẩm {self.selected_product_image}")
        else:
            QtWidgets.QMessageBox.warning(
                None, "Lỗi", "Không tìm thấy sản phẩm đã chọn.")

    def on_reset_click(self):
        # Xóa nội dung của ô nhập liệu và khung hiển thị kết quả tìm kiếm
        self.lineEdit.clear()
        self.textBrowser.clear()

        # Xóa ảnh đang hiển thị trên khung camera
        self.label_img_1.clear()

        # Xóa các ảnh gợi ý trong khu vực sản phẩm
        for i in reversed(range(self.gridLayout.count())):
            widget_to_remove = self.gridLayout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Reset các biến lưu trữ ảnh và mask về None
        self.person_img = None
        self.shirt_img = None
        self.selected_product_image = None
        self.mask_person_img = None
        self.mask_shirt_img = None

        # Thông báo cho người dùng rằng ứng dụng đã được reset
        QtWidgets.QMessageBox.information(
            None, "Reset", "Tôi đã giải phóng dung lượng xong, mời bạn tiếp tục với ứng dụng nhé!")

    def apply_virtual_try_on(self):
        if self.mask_person_img is not None and self.mask_shirt_img is not None:
            person_resized = self.person_img.copy()
            shirt_resized = cv2.resize(
                self.shirt_img, (self.person_img.shape[1], self.person_img.shape[0]))
            mask_person_resized = cv2.resize(
                self.mask_person_img, (self.person_img.shape[1], self.person_img.shape[0]))
            mask_shirt_resized = cv2.resize(
                self.mask_shirt_img, (self.person_img.shape[1], self.person_img.shape[0]))
            combined_mask = cv2.bitwise_and(
                mask_person_resized, mask_shirt_resized)

            for i in range(combined_mask.shape[0]):
                for j in range(combined_mask.shape[1]):
                    if combined_mask[i, j] == 255:
                        person_resized[i, j] = shirt_resized[i, j]

            self.display_image(person_resized, self.label_img_1)

    def display_image(self, image, frame):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(convert_to_Qt_format)
        frame.setPixmap(pixmap)

    def update_product_images(self, images):
        # Lưu tất cả các đường dẫn hình ảnh vào danh sách để dễ dàng truy xuất
        self.image_paths = images

        # Xóa tất cả widget trong layout
        for i in reversed(range(self.gridLayout.count())):
            widget_to_remove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        # Thêm các sản phẩm vào layout và gán sự kiện click cho mỗi sản phẩm
        for i, img_path in enumerate(images):
            if os.path.exists(img_path):
                pixmap = QtGui.QPixmap(img_path)
                label_img = ClickableLabel(self.scrollAreaWidgetContents)
                label_img.setPixmap(pixmap.scaled(
                    230, 270, QtCore.Qt.KeepAspectRatio))
                label_img.setObjectName(f"label_img_{i+1}")

                # Gán sự kiện click với index i
                label_img.clicked.connect(lambda i=i: self.on_product_click(i))
                self.gridLayout.addWidget(label_img, i // 3, i % 3)

        # # Đảm bảo gọi hàm retranslateUi ở cuối setupUi
        # self.retranslateUi(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
    # def mask_shirt(self):
    #     if self.shirt_img is not None:
    #         shirt_img_rgb = cv2.cvtColor(self.shirt_img, cv2.COLOR_BGR2RGB)
    #         results = self.yolo_model_for_shirt(shirt_img_rgb)

    #         if results[0].masks is not None:
    #             self.mask_shirt_img = (results[0].masks.data[0].cpu().numpy() * 255).astype("uint8")
    #         else:
    #             print("Không tìm thấy bất kỳ mask nào từ YOLO cho ảnh áo")
    #             self.mask_shirt_img = None

    # def merge_clothes(self):
    #     if self.mask_person_img is not None and self.mask_shirt_img is not None:
    #         # Đảm bảo kích thước của mask áo và người trùng khớp
    #         self.mask_shirt_img = cv2.resize(self.mask_shirt_img, (self.mask_person_img.shape[1], self.mask_person_img.shape[0]))

    #         # Tạo mask kết hợp và ảnh kết quả
    #         combined_mask = cv2.bitwise_and(self.mask_person_img, self.mask_shirt_img)
    #         shirt_resized = cv2.resize(self.shirt_img, (self.person_img.shape[1], self.person_img.shape[0]))
    #         person_resized = self.person_img.copy()

    #         # Ghép áo vào người theo mask
    #         person_resized[combined_mask == 255] = shirt_resized[combined_mask == 255]
    #         self.show_image(person_resized, self.result_frame)

    # def show_image(self, image, frame):
    #     resized_image = cv2.resize(image, (frame.width(), frame.height()), interpolation=cv2.INTER_AREA)
    #     height, width, channel = resized_image.shape
    #     bytes_per_line = 3 * width
    #     qimg = QtGui.QImage(resized_image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
    #     pixmap = QtGui.QPixmap.fromImage(qimg)
    #     frame.setPixmap(pixmap)

    def on_try_on_click(self):
        # Kiểm tra nếu đã có ảnh người và mask của người
        if self.person_img is None or self.mask_person_img is None:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "Vui lòng thêm và phân đoạn ảnh người trước!")
            return

        # Kiểm tra nếu đã chọn sản phẩm (ảnh áo)
        if self.selected_product_image is None:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "Vui lòng chọn sản phẩm trước khi thử đồ!")
            return

        # Đọc ảnh áo đã chọn và phân đoạn áo
        self.shirt_img = cv2.imread(self.selected_product_image)
        self.mask_shirt()  # Phân đoạn áo

        # Nếu phân đoạn áo thành công, ghép áo vào người và hiển thị
        if self.mask_shirt_img is not None:
            self.merge_clothes()
        else:
            QtWidgets.QMessageBox.warning(
                None, "Warning", "Không thể phân đoạn áo. Vui lòng thử ảnh khác!")

    def mask_shirt(self):
        if self.shirt_img is not None:
            shirt_img_rgb = cv2.cvtColor(self.shirt_img, cv2.COLOR_BGR2RGB)
            results = self.yolo_model_for_shirt(shirt_img_rgb)

            if results[0].masks is not None:
                self.mask_shirt_img = (
                    results[0].masks.data[0].cpu().numpy() * 255).astype("uint8")
            else:
                print("Không tìm thấy bất kỳ mask nào từ YOLO cho ảnh áo")
                self.mask_shirt_img = None

    def merge_clothes(self):
        if self.mask_person_img is not None and self.mask_shirt_img is not None:
            # Tính bounding box của người
            person_y, person_x = np.where(self.mask_person_img == 255)
            person_top_left = (np.min(person_x), np.min(person_y))
            person_bottom_right = (np.max(person_x), np.max(person_y))

            # Xác định chiều rộng và chiều cao của vùng người
            person_width = person_bottom_right[0] - person_top_left[0]
            person_height = person_bottom_right[1] - person_top_left[1]

            # Tính tỷ lệ cần thiết để điều chỉnh áo khớp với chiều cao của người
            shirt_aspect_ratio = self.shirt_img.shape[1] / \
                self.shirt_img.shape[0]
            new_shirt_height = person_height
            new_shirt_width = int(new_shirt_height * shirt_aspect_ratio)

            # Resize áo với tỷ lệ gốc
            shirt_resized = cv2.resize(
                self.shirt_img, (new_shirt_width, new_shirt_height))
            mask_shirt_resized = cv2.resize(
                self.mask_shirt_img, (new_shirt_width, new_shirt_height))

            # Tính vị trí căn giữa áo vào người
            offset_x = person_top_left[0] + \
                (person_width - new_shirt_width) // 2
            offset_y = person_top_left[1]

            # Dịch chuyển mask và ảnh của áo theo offset
            translation_matrix = np.float32(
                [[1, 0, offset_x], [0, 1, offset_y]])
            aligned_shirt_mask = cv2.warpAffine(mask_shirt_resized, translation_matrix, (
                self.mask_person_img.shape[1], self.mask_person_img.shape[0]))
            aligned_shirt_img = cv2.warpAffine(
                shirt_resized, translation_matrix, (self.person_img.shape[1], self.person_img.shape[0]))

            # Tạo mask kết hợp để chỉ giữ lại vùng của áo bên trong vùng người
            combined_mask = cv2.bitwise_and(
                self.mask_person_img, aligned_shirt_mask)

            # Tính màu trung bình của áo mới để phủ màu cho các vùng hở
            mean_color = cv2.mean(
                aligned_shirt_img, mask=aligned_shirt_mask.astype(np.uint8))[:3]

            # Tạo bản sao của ảnh người
            person_resized = self.person_img.copy()

            # Phủ màu trung bình lên các vùng hở và ghép áo vào người
            for i in range(combined_mask.shape[0]):
                for j in range(combined_mask.shape[1]):
                    # Nếu pixel thuộc cả mask người và mask áo
                    if combined_mask[i, j] == 255:
                        person_resized[i, j] = aligned_shirt_img[i, j]
                    elif self.mask_person_img[i, j] == 255 and aligned_shirt_mask[i, j] == 0:
                        # Phủ màu trung bình lên các vùng hở trong mask người nhưng không trong mask áo
                        person_resized[i, j] = mean_color

            # Hiển thị kết quả trên khung camera (label_img_1)
            self.display_image(person_resized, self.label_img_1)

    def display_image(self, image, frame):
        # Hàm hiển thị hình ảnh lên QLabel (khung hình)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(convert_to_Qt_format)
        frame.setPixmap(pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "CỬA HÀNG THỜI TRANG ẢO"))
        self.label.setText(_translate("MainWindow", "CỬA HÀNG THỜI TRANG ẢO"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Camera"))
        self.label_2.setText(_translate(
            "MainWindow", "Nhập tìm kiếm trang phục ở đây nhé!"))
        self.pushButton.setText(_translate("MainWindow", "Tìm kiếm"))
        self.groupBox_4.setTitle(_translate(
            "MainWindow", "Các thuộc tính tìm kiếm của bạn"))
        self.groupBox_5.setTitle(_translate("MainWindow", "MENU"))
        self.groupBox_6.setTitle(_translate(
            "MainWindow", "Chỉnh sửa thuộc tính"))
        self.pushButton_2.setText(_translate("MainWindow", "Sửa"))
        self.pushButton_3.setText(_translate("MainWindow", "Lưu"))
        self.groupBox_7.setTitle(_translate(
            "MainWindow", "Các chức năng chỉnh sửa"))
        self.pushButton_4.setText(_translate("MainWindow", "CAMERA ON"))
        self.pushButton_5.setText(_translate("MainWindow", "CHỤP ẢNH"))
        self.pushButton_6.setText(_translate("MainWindow", "THÊM ẢNH"))
        self.pushButton_7.setText(_translate("MainWindow", "THỬ ĐỒ"))
        self.pushButton_8.setText(_translate("MainWindow", "LƯU ẢNH"))
        self.pushButton_9.setText(_translate("MainWindow", "CAMERA OFF"))
        self.pushButton_10.setText(_translate("MainWindow", "RESET"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
