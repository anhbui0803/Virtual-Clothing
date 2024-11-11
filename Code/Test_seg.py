import cv2
import numpy as np
from ultralytics import YOLO
import dlib
from scipy.interpolate import Rbf

# Khởi tạo YOLO model cho cả người và áo
yolo_person = YOLO(r"D:\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt")  # Model segmentation cho người
yolo_shirt = YOLO(r"D:\Shop_Thoi_Trang_Ao\segment\train\weights\best.pt")  # Model segmentation cho áo

# Load hình ảnh người và áo
person_img = cv2.imread(r"D:\Shop_Thoi_Trang_Ao\data_1\Person\person_image (515).jpg")
shirt_img = cv2.imread(r"D:\Shop_Thoi_Trang_Ao\data_1\Clothes\clothes_image (7).png")

# Thực hiện segmentation trực tiếp để tạo mask trong bộ nhớ
person_results = yolo_person.predict(person_img)
shirt_results = yolo_shirt.predict(shirt_img)

# Kiểm tra nếu có `masks` và lấy mask cho người và áo
if person_results[0].masks is not None:
    person_mask = person_results[0].masks.data[0].cpu().numpy().astype(np.uint8) * 255
else:
    raise ValueError("No mask found for person in the result.")

if shirt_results[0].masks is not None:
    shirt_mask = shirt_results[0].masks.data[0].cpu().numpy().astype(np.uint8) * 255
else:
    raise ValueError("No mask found for shirt in the result.")

# Tăng kích thước áo dựa trên chiều rộng của người
shirt_width = int(person_img.shape[1] * 0.8)  # Tăng chiều rộng của áo lên 80% chiều rộng người
shirt_height = int(shirt_img.shape[0] * (shirt_width / shirt_img.shape[1]))  # Tăng chiều cao theo tỷ lệ

shirt_img_resized = cv2.resize(shirt_img, (shirt_width, shirt_height))
shirt_mask_resized = cv2.resize(shirt_mask, (shirt_width, shirt_height))

# Đặt áo vào vị trí thân trên
x_offset = (person_img.shape[1] - shirt_width) // 2  # Căn giữa theo chiều ngang
y_offset = int(person_img.shape[0] * 0.3)  # Căn chỉnh vị trí áo trên thân người

# Tạo vùng chỉ chứa áo (dựa trên mask của áo đã được định vị)
shirt_only = np.zeros_like(person_img)
shirt_only[y_offset:y_offset + shirt_height, x_offset:x_offset + shirt_width] = cv2.bitwise_and(
    shirt_img_resized, shirt_img_resized, mask=shirt_mask_resized
)

# Đảo ngược mask của áo để tạo vùng hiển thị người
inverse_shirt_mask = cv2.bitwise_not(shirt_mask_resized)
person_only = person_img.copy()
person_only[y_offset:y_offset + shirt_height, x_offset:x_offset + shirt_width] = cv2.bitwise_and(
    person_img[y_offset:y_offset + shirt_height, x_offset:x_offset + shirt_width],
    person_img[y_offset:y_offset + shirt_height, x_offset:x_offset + shirt_width],
    mask=inverse_shirt_mask
)

# Ghép hai hình ảnh lại với nhau
final_output = cv2.add(person_only, shirt_only)

# Hiển thị kết quả cuối cùng
cv2.imshow("Virtual Try-On", final_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
