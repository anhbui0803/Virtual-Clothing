import os
from PyQt5 import QtWidgets, QtGui, QtCore

# Đường dẫn tới hình ảnh sản phẩm
product_images = {
    'áo sơ mi': {
        'trắng': [r'D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (9).png', r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (7).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (6).png"],
        'đen': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (6).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (2).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (4).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (1).png"],
        'xanh': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (3).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_dai\so_mi_tay_dai (8).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (4).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (8).png"],
        'nâu': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (2).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (5).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_so_mi\Ao_so_mi_tay_ngan\so_mi_tay_ngan (7).png"]
    },
    'áo thun': {
        'trắng': [r'D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_co_co\co_co (4).png', r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_co_co\co_co (5).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (7).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (8).png"],
        'đen': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (6).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (5).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (1).png"],
        'xanh': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (10).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (9).png"],
        'xám': [r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_co_co\co_co (6).png", r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_co_co\co_co (7).png"]
    }
}

class ImageChecker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Path Checker')

        self.layout = QtWidgets.QVBoxLayout()

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit)

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.imageLabel)

        self.checkButton = QtWidgets.QPushButton('Check Image Paths', self)
        self.checkButton.clicked.connect(self.check_image_paths)
        self.layout.addWidget(self.checkButton)

        self.setLayout(self.layout)

    def check_image_paths(self):
        self.textEdit.clear()
        for product, colors in product_images.items():
            for color, paths in colors.items():
                for path in paths:
                    if os.path.exists(path):
                        self.textEdit.append(f'OK: {path}')
                        pixmap = QtGui.QPixmap(path)
                        if not pixmap.isNull():
                            self.imageLabel.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))
                            QtWidgets.QApplication.processEvents()  # Cập nhật giao diện để hiển thị ảnh
                        else:
                            self.textEdit.append(f'Error: Unable to load image: {path}')
                    else:
                        self.textEdit.append(f'Error: File does not exist: {path}')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    checker = ImageChecker()
    checker.show()
    sys.exit(app.exec_())
