import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import torch
# Giả sử đã cài đặt Segment Anything Model (SAM)
from segment_anything import sam_model_registry, SamPredictor

# Load YOLO model
model = YOLO(r'D:\Shop_Thoi_Trang_Ao\YOLO_Person\Person_V2\runs\detect\train\weights\best.pt')

# Load SAM model và kiểm tra thiết bị
device = "cuda" if torch.cuda.is_available() else "cpu"
sam_checkpoint = r"D:\Shop_Thoi_Trang_Ao\Model\sam_vit_h_4b8939.pth" 
sam = sam_model_registry["vit_h"](checkpoint=sam_checkpoint)
sam.to(device)
sam_predictor = SamPredictor(sam)

# Đọc ảnh
image_path = r"D:\Shop_Thoi_Trang_Ao\image\Ao_thun\Ao_thun_khong_co_co\khong_co_co (1).png"
image = cv2.imread(image_path)
image_copy = image.copy()

# Resize ảnh để xử lý nhanh hơn
resized_image = cv2.resize(image, (640, 480))

# Dự đoán với YOLO
results = model(resized_image)

# Kiểm tra xem YOLO có phát hiện đối tượng không
if not results:
    print("Không có đối tượng nào được phát hiện bởi YOLO!")
else:
    print(f"YOLO phát hiện {len(results)} đối tượng.")

# Tạo mask cho vùng phát hiện
mask = np.zeros(resized_image.shape[:2], dtype=np.uint8)
detected = False  # Cờ để kiểm tra xem có phát hiện được không

for result in results:
    for box in result.boxes:
        detected = True  # Có đối tượng được phát hiện
        # Lấy tọa độ của bounding box phát hiện được
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Vẽ bounding box lên ảnh gốc
        cv2.rectangle(image_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Crop vùng áo từ ảnh gốc
        cropped_image = resized_image[y1:y2, x1:x2]

        # Sử dụng SAM để tạo mask chi tiết cho vùng phát hiện bởi YOLO
        sam_predictor.set_image(cropped_image)  # Đưa ảnh đã crop vào SAM để dự đoán
        input_box = np.array([0, 0, x2 - x1, y2 - y1])  # Tạo input box cho vùng đã crop

        masks, _, _ = sam_predictor.predict(box=input_box)  # Dự đoán mask từ vùng phát hiện

        # Resize mask SAM để khớp với kích thước vùng phát hiện từ YOLO
        sam_mask_resized = cv2.resize(masks[0].astype(np.uint8), (x2 - x1, y2 - y1))

        # Áp dụng mask vào hình ảnh gốc để tạo mask cho vùng áo
        mask[y1:y2, x1:x2] = (sam_mask_resized * 255).astype(np.uint8)  # Chuyển đổi mask về định dạng ảnh nhị phân

# Nếu không có đối tượng được phát hiện, báo lỗi
if not detected:
    print("Không phát hiện được vùng áo trong ảnh.")

# Hiển thị kết quả bằng matplotlib
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Hiển thị ảnh gốc với bounding box từ YOLO
ax[0].imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
ax[0].set_title("YOLO Detection")
ax[0].axis('off')

# Hiển thị mask đã tạo
ax[1].imshow(mask, cmap='gray')
ax[1].set_title("SAM Mask")
ax[1].axis('off')

plt.show()

# Xuất ảnh mask ra file
output_path = 'output_mask.jpg'
cv2.imwrite(output_path, mask)
print(f"Mask được xuất ra tại: {output_path}")
