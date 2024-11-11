# import sys
# import cv2
# import numpy as np
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QFileDialog
# from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt
# from ultralytics import YOLO
# from sklearn.cluster import KMeans


# class VirtualTryOnApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Virtual Try-On Application")
#         self.setGeometry(100, 100, 1200, 600)
#         self.initUI()

#     def initUI(self):
#         layout = QGridLayout()

#         # Khung chứa hình ảnh và các nút
#         self.person_frame = QLabel("Khung person")
#         self.person_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.person_frame.setFixedSize(300, 400)

#         self.mask_person_frame = QLabel("Khung person mask")
#         self.mask_person_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.mask_person_frame.setFixedSize(300, 400)

#         self.shirt_frame = QLabel("Khung shirt")
#         self.shirt_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.shirt_frame.setFixedSize(300, 400)

#         self.mask_shirt_frame = QLabel("Khung shirt mask")
#         self.mask_shirt_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.mask_shirt_frame.setFixedSize(300, 400)

#         self.result_frame = QLabel("Khung ghép ảnh")
#         self.result_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.result_frame.setFixedSize(300, 400)

#         # Nút bấm
#         self.load_person_btn = QPushButton('Load Person')
#         self.load_person_btn.setStyleSheet(self.button_style())
#         self.load_person_btn.clicked.connect(self.load_person)

#         self.mask_person_btn = QPushButton('Mask Person')
#         self.mask_person_btn.setStyleSheet(self.button_style())
#         self.mask_person_btn.clicked.connect(self.mask_person)

#         self.load_shirt_btn = QPushButton('Load Shirt')
#         self.load_shirt_btn.setStyleSheet(self.button_style())
#         self.load_shirt_btn.clicked.connect(self.load_shirt)

#         self.mask_shirt_btn = QPushButton('Mask Shirt')
#         self.mask_shirt_btn.setStyleSheet(self.button_style())
#         self.mask_shirt_btn.clicked.connect(self.mask_shirt)

#         self.merge_btn = QPushButton('Merge Clothes')
#         self.merge_btn.setStyleSheet(self.button_style())
#         self.merge_btn.clicked.connect(self.merge_clothes)

#         # Thêm vào layout
#         layout.addWidget(self.person_frame, 0, 0)
#         layout.addWidget(self.mask_person_frame, 0, 1)
#         layout.addWidget(self.shirt_frame, 0, 2)
#         layout.addWidget(self.mask_shirt_frame, 0, 3)
#         layout.addWidget(self.result_frame, 1, 1, 1, 2)

#         layout.addWidget(self.load_person_btn, 2, 0)
#         layout.addWidget(self.mask_person_btn, 2, 1)
#         layout.addWidget(self.load_shirt_btn, 2, 2)
#         layout.addWidget(self.mask_shirt_btn, 2, 3)
#         layout.addWidget(self.merge_btn, 3, 1, 1, 2)

#         self.setLayout(layout)

#         # Khởi tạo biến để lưu trữ hình ảnh
#         self.person_img = None
#         self.shirt_img = None
#         self.mask_person_img = None
#         self.mask_shirt_img = None
#         self.yolo_model = YOLO(r'D:\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt')

#     def button_style(self):
#         return """
#         QPushButton {
#             background-color: #00CED1;
#             border-radius: 10px;
#             padding: 10px;
#             font-weight: bold;
#         }
#         QPushButton:hover {
#             background-color: #20B2AA;
#         }
#         """

#     def load_image(self, frame):
#         # Load file ảnh
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg)')
#         if file_name:
#             image = cv2.imread(file_name)
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
#             # Lấy kích thước của khung chứa ảnh (QLabel)
#             label_width = frame.width()
#             label_height = frame.height()

#             # Resize ảnh cho vừa với khung
#             resized_image = cv2.resize(image, (label_width, label_height), interpolation=cv2.INTER_AREA)

#             # Chuyển đổi sang QImage để hiển thị
#             height, width, channel = resized_image.shape
#             bytes_per_line = 3 * width
#             qimg = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qimg)

#             # Hiển thị ảnh lên khung
#             frame.setPixmap(pixmap)
            
#             return image
#         return None

#     def load_person(self):
#         self.person_img = self.load_image(self.person_frame)

#     def load_shirt(self):
#         self.shirt_img = self.load_image(self.shirt_frame)

#     def mask_person(self):
#         if self.person_img is not None:
#             # Chuyển ảnh từ OpenCV sang định dạng để YOLO sử dụng
#             person_img_rgb = cv2.cvtColor(self.person_img, cv2.COLOR_BGR2RGB)

#             # Dùng model YOLO để phát hiện và phân đoạn person
#             results = self.yolo_model(person_img_rgb)

#             if results[0].masks is not None:
#                 # Lấy mask từ kết quả YOLO
#                 mask = results[0].masks.data[0].cpu().numpy()

#                 # Tạo mask hình ảnh
#                 mask_img = (mask * 255).astype("uint8")
#                 self.mask_person_img = mask_img

#                 # Hiển thị mask person
#                 self.show_image(cv2.merge([mask_img, mask_img, mask_img]), self.mask_person_frame)
#             else:
#                 print("Không tìm thấy bất kỳ mask nào từ YOLO")
#                 return None
#         return None

#     def mask_shirt(self):
#         if self.shirt_img is not None:
#             # Chuyển ảnh thành không gian màu HSV
#             hsv = cv2.cvtColor(self.shirt_img, cv2.COLOR_RGB2HSV)

#             # Định nghĩa ngưỡng màu cho áo (dựa trên màu sắc áo mà bạn mong muốn xử lý)
#             # Bạn có thể điều chỉnh giá trị ngưỡng này để phù hợp với màu áo
#             lower_bound = np.array([30, 50, 50])  # Giới hạn dưới cho Hue, Saturation và Value
#             upper_bound = np.array([120, 255, 255])  # Giới hạn trên cho Hue, Saturation và Value

#             # Tạo mask dựa trên giá trị ngưỡng
#             mask = cv2.inRange(hsv, lower_bound, upper_bound)

#              # Sử dụng các phép dãn và xói mòn để làm mịn mask
#             kernel = np.ones((5, 5), np.uint8)
#             mask = cv2.dilate(mask, kernel, iterations=2)
#             mask = cv2.erode(mask, kernel, iterations=2)

#             # # Làm mịn mask bằng Gaussian Blur để biên mượt hơn
#             # mask = cv2.GaussianBlur(mask, (21, 21), 0)

#             self.mask_shirt_img = mask

#             # Hiển thị mask áo
#             self.show_image(cv2.merge([mask, mask, mask]), self.mask_shirt_frame)

#             return mask
#         return None

#     def merge_clothes(self):
#         # Ghép ảnh từ person và shirt mask
#         if self.mask_person_img is not None and self.mask_shirt_img is not None:
#             # Kiểm tra kích thước và resize mask của áo cho phù hợp với mask của person
#             if self.mask_person_img.shape != self.mask_shirt_img.shape:
#                 self.mask_shirt_img = cv2.resize(self.mask_shirt_img, 
#                                                  (self.mask_person_img.shape[1], self.mask_person_img.shape[0]))

#             # Tạo vùng kết hợp: chỉ giữ lại phần của áo trên thân người
#             combined_mask = cv2.bitwise_and(self.mask_person_img, self.mask_shirt_img)

#             # Chỉnh lại kích thước áo cho phù hợp với người
#             shirt_resized = cv2.resize(self.shirt_img, (self.person_img.shape[1], self.person_img.shape[0]))

#             # Tạo ảnh nền là ảnh người, nhưng chỉ giữ lại vùng thân người
#             person_resized = self.person_img.copy()

#             # Kết hợp áo mới vào hình ảnh người
#             combined_result = np.where(combined_mask[:, :, None] == 255, shirt_resized, person_resized)

#             # Hiển thị kết quả
#             self.show_image(combined_result, self.result_frame)

#     def show_image(self, image, frame):
#         # Resize ảnh cho vừa với khung
#         resized_image = cv2.resize(image, (frame.width(), frame.height()), interpolation=cv2.INTER_AREA)

#         # Chuyển đổi sang QImage để hiển thị
#         height, width, channel = resized_image.shape
#         bytes_per_line = 3 * width
#         qimg = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(qimg)

#         # Hiển thị ảnh lên khung
#         frame.setPixmap(pixmap)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = VirtualTryOnApp()
#     window.show()
#     sys.exit(app.exec_())


# import sys
# import cv2
# import numpy as np
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QFileDialog
# from PyQt5.QtGui import QPixmap, QImage
# from PyQt5.QtCore import Qt
# from ultralytics import YOLO
# from sklearn.cluster import KMeans


# class VirtualTryOnApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Virtual Try-On Application")
#         self.setGeometry(100, 100, 1200, 600)
#         self.initUI()

#     def initUI(self):
#         layout = QGridLayout()

#         # Khung chứa hình ảnh và các nút
#         self.person_frame = QLabel("Khung person")
#         self.person_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.person_frame.setFixedSize(300, 400)

#         self.mask_person_frame = QLabel("Khung person mask")
#         self.mask_person_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.mask_person_frame.setFixedSize(300, 400)

#         self.shirt_frame = QLabel("Khung shirt")
#         self.shirt_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.shirt_frame.setFixedSize(300, 400)

#         self.mask_shirt_frame = QLabel("Khung shirt mask")
#         self.mask_shirt_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.mask_shirt_frame.setFixedSize(300, 400)

#         self.result_frame = QLabel("Khung ghép ảnh")
#         self.result_frame.setStyleSheet("border: 2px solid gray; background-color: lightgray")
#         self.result_frame.setFixedSize(300, 400)

#         # Nút bấm
#         self.load_person_btn = QPushButton('Load Person')
#         self.load_person_btn.setStyleSheet(self.button_style())
#         self.load_person_btn.clicked.connect(self.load_person)

#         self.mask_person_btn = QPushButton('Mask Person')
#         self.mask_person_btn.setStyleSheet(self.button_style())
#         self.mask_person_btn.clicked.connect(self.mask_person)

#         self.load_shirt_btn = QPushButton('Load Shirt')
#         self.load_shirt_btn.setStyleSheet(self.button_style())
#         self.load_shirt_btn.clicked.connect(self.load_shirt)

#         self.mask_shirt_btn = QPushButton('Mask Shirt')
#         self.mask_shirt_btn.setStyleSheet(self.button_style())
#         self.mask_shirt_btn.clicked.connect(self.mask_shirt)

#         self.merge_btn = QPushButton('Merge Clothes')
#         self.merge_btn.setStyleSheet(self.button_style())
#         self.merge_btn.clicked.connect(self.merge_clothes)

#         # Thêm vào layout
#         layout.addWidget(self.person_frame, 0, 0)
#         layout.addWidget(self.mask_person_frame, 0, 1)
#         layout.addWidget(self.shirt_frame, 0, 2)
#         layout.addWidget(self.mask_shirt_frame, 0, 3)
#         layout.addWidget(self.result_frame, 1, 1, 1, 2)

#         layout.addWidget(self.load_person_btn, 2, 0)
#         layout.addWidget(self.mask_person_btn, 2, 1)
#         layout.addWidget(self.load_shirt_btn, 2, 2)
#         layout.addWidget(self.mask_shirt_btn, 2, 3)
#         layout.addWidget(self.merge_btn, 3, 1, 1, 2)

#         self.setLayout(layout)

#         # Khởi tạo biến để lưu trữ hình ảnh
#         self.person_img = None
#         self.shirt_img = None
#         self.mask_person_img = None
#         self.mask_shirt_img = None

#         # Khởi tạo mô hình YOLO cho phân đoạn người và áo
#         self.yolo_model_for_person = YOLO(r'D:\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt')
#         self.yolo_model_for_person = YOLO(r'D:\Shop_Thoi_Trang_Ao\hihi.v1i.yolov11\hihi.pt')
#         self.yolo_model_for_shirt = YOLO(r'D:\Shop_Thoi_Trang_Ao\segment\train\weights\best.pt') 

#     def button_style(self):
#         return """
#         QPushButton {
#             background-color: #00CED1;
#             border-radius: 10px;
#             padding: 10px;
#             font-weight: bold;
#         }
#         QPushButton:hover {
#             background-color: #20B2AA;
#         }
#         """

#     def load_image(self, frame):
#         # Load file ảnh
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg)')
#         if file_name:
#             image = cv2.imread(file_name)
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
#             # Lấy kích thước của khung chứa ảnh (QLabel)
#             label_width = frame.width()
#             label_height = frame.height()

#             # Resize ảnh cho vừa với khung
#             resized_image = cv2.resize(image, (label_width, label_height), interpolation=cv2.INTER_AREA)

#             # Chuyển đổi sang QImage để hiển thị
#             height, width, channel = resized_image.shape
#             bytes_per_line = 3 * width
#             qimg = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qimg)

#             # Hiển thị ảnh lên khung
#             frame.setPixmap(pixmap)
            
#             return image
#         return None

#     def load_person(self):
#         self.person_img = self.load_image(self.person_frame)

#     def load_shirt(self):
#         self.shirt_img = self.load_image(self.shirt_frame)

    # def mask_person(self):
    #     if self.person_img is not None:
    #         # Chuyển ảnh từ OpenCV sang định dạng YOLO có thể sử dụng
    #         person_img_rgb = cv2.cvtColor(self.person_img, cv2.COLOR_BGR2RGB)

    #         # Dùng model YOLO để phát hiện và phân đoạn person
    #         results = self.yolo_model_for_person(person_img_rgb)

    #         if results[0].masks is not None:
    #             # Lấy mask từ kết quả YOLO
    #             mask = results[0].masks.data[0].cpu().numpy()

    #             # Tạo mask hình ảnh
    #             mask_img = (mask * 255).astype("uint8")
    #             self.mask_person_img = mask_img

    #             # Hiển thị mask person
    #             self.show_image(cv2.merge([mask_img, mask_img, mask_img]), self.mask_person_frame)
    #         else:
    #             print("Không tìm thấy bất kỳ mask nào từ YOLO")
    #             return None
    #     return None

    # def mask_shirt(self):
    #     if self.shirt_img is not None:
    #         # Chuyển ảnh từ OpenCV sang định dạng YOLO có thể sử dụng
    #         shirt_img_rgb = cv2.cvtColor(self.shirt_img, cv2.COLOR_BGR2RGB)

    #         # Dùng model YOLO để phát hiện và phân đoạn áo
    #         results = self.yolo_model_for_shirt(shirt_img_rgb)

    #         if results[0].masks is not None:
    #             # Lấy mask từ kết quả YOLO
    #             mask = results[0].masks.data[0].cpu().numpy()

    #             # Tạo mask hình ảnh
    #             mask_img = (mask * 255).astype("uint8")
    #             self.mask_shirt_img = mask_img

    #             # Hiển thị mask áo
    #             self.show_image(cv2.merge([mask_img, mask_img, mask_img]), self.mask_shirt_frame)
    #         else:
    #             print("Không tìm thấy bất kỳ mask nào từ YOLO")
    #             return None
    #     return None

    # def merge_clothes(self):
    #     # Merge images from person and shirt mask
    #     if self.mask_person_img is not None and self.mask_shirt_img is not None:
    #         # Ensure the mask sizes match
    #         if self.mask_person_img.shape != self.mask_shirt_img.shape:
    #             self.mask_shirt_img = cv2.resize(self.mask_shirt_img, 
    #                                              (self.mask_person_img.shape[1], self.mask_person_img.shape[0]))

    #         # Create a combined mask
    #         combined_mask = cv2.bitwise_and(self.mask_person_img, self.mask_shirt_img)

    #         # Resize shirt to match person's dimensions
    #         shirt_resized = cv2.resize(self.shirt_img, (self.person_img.shape[1], self.person_img.shape[0]))

    #         # Make a copy of person image
    #         person_resized = self.person_img.copy()

    #         # Iterate through each pixel of the combined mask
    #         for i in range(combined_mask.shape[0]):
    #             for j in range(combined_mask.shape[1]):
    #                 if combined_mask[i, j] == 255:
    #                     person_resized[i, j] = shirt_resized[i, j]

    #         # Display the result
    #         self.show_image(person_resized, self.result_frame)

    # def show_image(self, image, frame):
    #     # Resize ảnh cho vừa với khung
    #     resized_image = cv2.resize(image, (frame.width(), frame.height()), interpolation=cv2.INTER_AREA)

    #     # Chuyển đổi sang QImage để hiển thị
    #     height, width, channel = resized_image.shape
    #     bytes_per_line = 3 * width
    #     qimg = QImage(resized_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    #     pixmap = QPixmap.fromImage(qimg)

    #     # Hiển thị ảnh lên khung
    #     frame.setPixmap(pixmap)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = VirtualTryOnApp()
#     window.show()
#     sys.exit(app.exec_())
# from ultralytics import YOLO
# import cv2
# import numpy as np

# # Đường dẫn tới mô hình YOLO được huấn luyện cho phân đoạn áo
# model_path = r'D:\Shop_Thoi_Trang_Ao\hihi.v1i.yolov11\hihi.pt'
# yolo_model = YOLO(model_path)

# def segment_shirt(image_path):
#     # Đọc ảnh đầu vào
#     image = cv2.imread(image_path)
    
#     # Chuyển đổi ảnh sang RGB (YOLO yêu cầu định dạng RGB)
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Thực hiện phân đoạn bằng YOLO
#     results = yolo_model(image_rgb)

#     # Kiểm tra nếu có mặt nạ (mask) trong kết quả
#     if results[0].masks is not None:
#         # Lấy mask cho áo (dựa vào lớp áo trong kết quả YOLO)
#         mask = (results[0].masks.data[0].cpu().numpy() * 255).astype("uint8")

#         # Thay đổi kích thước của mask để khớp với kích thước ảnh gốc
#         mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

#         # Chuyển đổi mask thành ảnh ba kênh để dễ dàng ghép với ảnh gốc
#         mask_rgb = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2BGR)
        
#         # Tạo ảnh chỉ chứa phần áo bằng cách nhân mask với ảnh gốc
#         shirt_segmented = cv2.bitwise_and(image, mask_rgb)
        
#         return shirt_segmented, mask_resized
#     else:
#         print("Không tìm thấy áo trong ảnh này.")
#         return None, None

# # Đường dẫn tới ảnh áo cần phân đoạn
# image_path = r'D:\Shop_Thoi_Trang_Ao\data\Person\abc (81).jpg'
# # Thực hiện phân đoạn áo và hiển thị kết quả
# shirt_segmented, mask = segment_shirt(image_path)
# if shirt_segmented is not None:
#     # Hiển thị kết quả
#     cv2.imshow("Shirt Segmented", shirt_segmented)
#     cv2.imshow("Mask", mask)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
