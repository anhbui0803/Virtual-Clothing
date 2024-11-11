import cv2
import time
import os
from datetime import datetime

# Tạo thư mục chính để lưu ảnh nếu chưa có
main_output_folder = r"D:\Shop_Thoi_Trang_Ao\data_1"
if not os.path.exists(main_output_folder):
    os.makedirs(main_output_folder)

# Mở camera
cap = cv2.VideoCapture(1)

# Kiểm tra xem camera có mở được không
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

# Hiển thị camera trong khi đếm ngược
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame từ camera")
            break
        # Hiển thị camera trong quá trình đếm ngược
        cv2.putText(frame, f"Chụp ảnh trong {i} giây...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Camera", frame)
        cv2.waitKey(1000)  # Chờ 1 giây cho mỗi lần đếm ngược

# Tạo một thư mục mới cho mỗi lần chụp dựa trên thời gian
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_folder = os.path.join(main_output_folder, f"session_{timestamp}")
os.makedirs(output_folder, exist_ok=True)

# Đếm ngược 5 giây trước khi chụp
countdown_timer(5)

# Số lượng ảnh cần chụp
total_images = 100
delay_between_shots = 0.3  # Thời gian giữa các lần chụp (0.3 giây)

print("Bắt đầu chụp ảnh...")

# Chụp ảnh
for i in range(1, total_images + 1):
    ret, frame = cap.read()
    if not ret:
        print("Không thể chụp ảnh từ camera")
        break
    
    # Lưu ảnh vào thư mục
    image_path = os.path.join(output_folder, f"image_{i:03d}.jpg")
    cv2.imwrite(image_path, frame)
    
    print(f"Đã chụp và lưu {image_path}")
    
    # Hiển thị ảnh đã chụp
    cv2.imshow("Image", frame)
    
    # Dừng giữa các lần chụp
    time.sleep(delay_between_shots)
    
    # Nhấn phím 'q' để dừng sớm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()

print(f"Đã chụp {i} ảnh và lưu vào thư mục {output_folder}")
