import cv2
import torch
import numpy as np
from ultralytics import YOLO
from matplotlib import pyplot as plt

# Tải mô hình YOLO đã được huấn luyện với khả năng segmentation
model = YOLO(r'D:\Shop_Thoi_Trang_Ao\Model\segmention_Yolov8.pt')  # Thay thế đường dẫn bằng mô hình YOLO segmentation của bạn

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Không thể load ảnh từ đường dẫn đã cho")
    return img

def display_image(img, title="Hình ảnh"):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def create_mask_using_yolo(image):
    results = model(image)

    if results[0].masks is not None:
        # Lấy mask đầu tiên
        mask = results[0].masks.data[0].cpu().numpy()

        # Chuyển đổi mask sang ảnh trắng đen
        mask_img = (mask * 255).astype(np.uint8)

        # Resize mask cho phù hợp với kích thước gốc của ảnh
        mask_img_resized = cv2.resize(mask_img, (image.shape[1], image.shape[0]))

        return mask_img_resized
    else:
        print("Không tìm thấy bất kỳ vùng phân đoạn nào.")
        return None

def create_mask_manually(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # Tìm contours
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        contour_info.append((c, cv2.isContourConvex(c), cv2.contourArea(c)))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    
    # Tạo mask trống và fill các contours
    mask = np.zeros(edges.shape, dtype=np.uint8)
    for c in contour_info:
        cv2.fillConvexPoly(mask, c[0], 255)

    # Làm mịn và blur mask
    kernel = np.ones((10, 10), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)

    return mask

def apply_transparent_background(image, mask):
    # Tạo mask 3 kênh
    mask_stack = np.dstack([mask]*3)

    # Chuyển đổi ảnh và mask về dạng float32
    mask_stack = mask_stack.astype('float32') / 255.0
    image = image.astype('float32') / 255.0

    # Áp dụng mask vào ảnh
    masked = (mask_stack * image) + ((1-mask_stack) * (1.0, 1.0, 1.0))
    masked = (masked * 255).astype('uint8')

    # Thêm kênh alpha để tạo nền trong suốt
    tmp = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    b, g, r = cv2.split(masked)
    rgba = [b, g, r, alpha]
    transparent_image = cv2.merge(rgba, 4)

    return transparent_image

def save_image(image, output_path="output.png"):
    cv2.imwrite(output_path, image)
    print(f"Đã lưu ảnh đầu ra tại {output_path}")

# Main program
if __name__ == "__main__":
    # Đường dẫn cố định
    image_path = r"C:\Users\LENOVO\Downloads\Data\data\image_238.jpg"  # Thay bằng đường dẫn của bạn
    image = load_image(image_path)
    
    # Thử tạo mask bằng YOLO
    mask = create_mask_using_yolo(image)
    
    if mask is None:
        # Nếu YOLO không tìm thấy mask, tạo mask thủ công
        print("Không tìm thấy mask từ YOLO, tạo mask thủ công...")
        mask = create_mask_manually(image)

    # Hiển thị kết quả mask
    display_image(mask, title="Mask đã tạo")

    # Áp dụng nền trong suốt
    transparent_image = apply_transparent_background(image, mask)

    # Hiển thị ảnh với nền trong suốt
    display_image(transparent_image, title="Ảnh với nền trong suốt")

    # Lưu ảnh kết quả
    save_image(transparent_image)
