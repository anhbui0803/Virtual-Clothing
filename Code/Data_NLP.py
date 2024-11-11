import random
import pandas as pd
import numpy as np

# Các danh sách thuộc tính sản phẩm
loai_trang_phuc = ['Áo sơ mi', 'Váy', 'Quần jean', 'Áo thun', 'Áo khoác', 'Đầm dạ hội', 'Quần kaki', 'Áo hoodie', 'Áo vest', 'Áo len', 'Quần short']
mau_sac = ['trắng', 'đen', 'đỏ', 'xanh', 'xám', 'nâu', 'hồng', 'vàng', 'tím', 'xanh lá cây', 'cam', 'nâu đỏ']
phong_cach = ['trẻ trung', 'năng động', 'cổ điển', 'sang trọng', 'đơn giản', 'thanh lịch', 'phá cách', 'thể thao', 'lịch lãm', 'hiện đại', 'quyến rũ', 'truyền thống']
doi_tuong_su_dung = ['trẻ em', 'người lớn', 'người già', 'nam', 'nữ', 'trung niên', 'con trai', 'con gái', 'doanh nhân', 'vận động viên', 'phụ nữ mang thai', 'người nội trợ']
chat_lieu = ['cotton', 'denim', 'polyester', 'lụa', 'len', 'vải dạ', 'vải nỉ', 'vải kaki', 'vải dù', 'nhung', 'vải lanh', 'da thật']
tinh_nang = ['chống nhăn', 'co giãn', 'thoáng khí', 'giữ ấm', 'không thấm nước', 'dễ giặt', 'chống tia UV', 'chống bám bụi', 'kháng khuẩn', 'thoải mái vận động']
cam_giac = ['thoải mái', 'lịch lãm', 'nhẹ nhàng', 'dễ chịu', 'ấm áp', 'thời thượng', 'tự tin', 'năng động', 'mạnh mẽ', 'quyến rũ', 'dịu dàng']
kich_co = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

# Từ đồng nghĩa cho các thuộc tính
dong_nghia = {
    'Áo sơ mi': ['áo sơ mi', 'sơ mi', 'áo', 'quần áo', 'trang phục'],
    'Váy': ['váy', 'đầm', 'váy ngắn', 'váy dài'],
    'Quần jean': ['quần jean', 'quần bò', 'quần denim', 'jean'],
    'Áo thun': ['áo thun', 'áo phông', 'áo t-shirt', 't-shirt', 'áo cotton'],
    'Áo khoác': ['áo khoác', 'khoác', 'áo jacket', 'jacket'],
    'Đầm dạ hội': ['đầm dạ hội', 'váy dạ hội', 'đầm'],
    'Quần kaki': ['quần kaki', 'kaki', 'quần vải', 'quần'],
    'Áo hoodie': ['áo hoodie', 'hoodie', 'áo chui đầu'],
    'Áo vest': ['áo vest', 'vest', 'áo blazer', 'blazer'],
    'Áo len': ['áo len', 'len', 'áo sweater', 'sweater'],
    'Quần short': ['quần short', 'short', 'quần ngắn'],

    # Màu sắc
    'trắng': ['trắng', 'màu trắng', 'trăng'],
    'đen': ['đen', 'màu đen'],
    'đỏ': ['đỏ', 'màu đỏ'],
    'xanh': ['xanh', 'màu xanh', 'xanh dương'],
    'xám': ['xám', 'màu xám', 'màu ghi', 'ghi'],
    'nâu': ['nâu', 'màu nâu'],
    'hồng': ['hồng', 'màu hồng'],
    'vàng': ['vàng', 'màu vàng'],
    'tím': ['tím', 'màu tím'],
    'xanh lá cây': ['xanh lá cây', 'màu xanh lá', 'xanh lá', 'xanh lục'],
    'cam': ['cam', 'màu cam'],
    'nâu đỏ': ['nâu đỏ', 'màu nâu đỏ'],

    # Phong cách
    'trẻ trung': ['trẻ trung', 'tươi trẻ'],
    'năng động': ['năng động', 'hoạt bát'],
    'cổ điển': ['cổ điển', 'vintage', 'xưa'],
    'sang trọng': ['sang trọng', 'quý phái', 'luxury'],
    'đơn giản': ['đơn giản', 'giản dị'],
    'thanh lịch': ['thanh lịch', 'lịch sự', 'elegant'],
    'phá cách': ['phá cách', 'độc đáo', 'cá tính'],
    'thể thao': ['thể thao', 'sporty'],
    'lịch lãm': ['lịch lãm', 'trang trọng', 'formal'],
    'hiện đại': ['hiện đại', 'modern'],
    'quyến rũ': ['quyến rũ', 'sexy', 'gợi cảm'],
    'truyền thống': ['truyền thống', 'cổ truyền', 'xưa cũ'],

    # Đối tượng sử dụng
    'trẻ em': ['trẻ em', 'thiếu nhi', 'em bé', 'con nít'],
    'người lớn': ['người lớn', 'người trưởng thành', 'người lớn tuổi'],
    'người già': ['người già', 'người cao tuổi'],
    'nam': ['nam', 'con trai', 'đàn ông', 'phái nam'],
    'nữ': ['nữ', 'con gái', 'phụ nữ', 'phái nữ'],
    'trung niên': ['trung niên', 'người trung niên'],
    'doanh nhân': ['doanh nhân', 'người kinh doanh'],
    'vận động viên': ['vận động viên', 'thể thao'],
    'phụ nữ mang thai': ['phụ nữ mang thai', 'mang bầu', 'bầu bí'],
    'người nội trợ': ['người nội trợ', 'bà nội trợ'],

    # Chất liệu
    'cotton': ['cotton', 'vải cotton', 'cotton 100%'],
    'denim': ['denim', 'vải denim', 'jean'],
    'polyester': ['polyester', 'vải polyester'],
    'lụa': ['lụa', 'vải lụa', 'lụa mềm'],
    'len': ['len', 'vải len', 'len dày'],
    'vải dạ': ['vải dạ', 'dạ'],
    'vải nỉ': ['vải nỉ', 'nỉ'],
    'vải kaki': ['vải kaki', 'kaki'],
    'vải dù': ['vải dù', 'dù'],
    'nhung': ['nhung', 'vải nhung'],
    'vải lanh': ['vải lanh', 'lanh'],
    'da thật': ['da thật', 'vải da', 'da'],

    # Tính năng
    'chống nhăn': ['chống nhăn', 'không nhăn'],
    'co giãn': ['co giãn', 'đàn hồi', 'giãn'],
    'thoáng khí': ['thoáng khí', 'hút ẩm'],
    'giữ ấm': ['giữ ấm', 'ấm áp'],
    'không thấm nước': ['không thấm nước', 'chống nước'],
    'dễ giặt': ['dễ giặt', 'giặt dễ'],
    'chống tia UV': ['chống tia UV', 'kháng UV', 'chống nắng'],
    'chống bám bụi': ['chống bám bụi', 'kháng bụi'],
    'kháng khuẩn': ['kháng khuẩn', 'chống khuẩn'],
    'thoải mái vận động': ['thoải mái vận động', 'dễ vận động', 'tự do vận động'],


    # Cảm giác
    'thoải mái': ['thoải mái', 'dễ chịu', 'tự do'],
    'lịch lãm': ['lịch lãm', 'trang trọng', 'quý phái'],
    'nhẹ nhàng': ['nhẹ nhàng', 'êm dịu'],
    'dễ chịu': ['dễ chịu', 'thoải mái'],
    'ấm áp': ['ấm áp', 'giữ ấm'],
    'thời thượng': ['thời thượng', 'hợp mốt'],
    'tự tin': ['tự tin', 'đầy tự tin'],
    'năng động': ['năng động', 'hoạt bát'],
    'mạnh mẽ': ['mạnh mẽ', 'quyết đoán'],
    'quyến rũ': ['quyến rũ', 'sexy', 'gợi cảm'],
    'dịu dàng': ['dịu dàng', 'nhẹ nhàng'],
    
    # Kích cỡ
    'S': ['S', 'size S', 'nhỏ'],
    'M': ['M', 'size M', 'vừa'],
    'L': ['L', 'size L', 'lớn'],
    'XL': ['XL', 'size XL', 'rộng'],
    'XXL': ['XXL', 'size XXL', 'cỡ lớn'],
    'XXXL': ['XXXL', 'size XXXL', 'rất lớn']
}

# Hàm chọn từ đồng nghĩa ngẫu nhiên
def chon_tu_dong_nghia(tu):
    if tu in dong_nghia:
        return random.choice(dong_nghia[tu])
    return tu

# Hàm tạo lỗi chính tả ngẫu nhiên bằng cách đổi một chữ cái
def tao_loi_chinh_ta(tu):
    if len(tu) > 3 and random.random() < 0.3:  # Xác suất tạo lỗi là 30%
        vi_tri = random.randint(0, len(tu) - 2)
        return tu[:vi_tri] + tu[vi_tri+1] + tu[vi_tri] + tu[vi_tri+2:]  # Đổi vị trí hai chữ cái
    return tu

# Hàm tạo mô tả sản phẩm ngẫu nhiên với từ đồng nghĩa và lỗi chính tả
def tao_mo_ta():
    loai = chon_tu_dong_nghia(random.choice(loai_trang_phuc))
    mau = chon_tu_dong_nghia(random.choice(mau_sac))
    phong_cach_chon = chon_tu_dong_nghia(random.choice(phong_cach))
    doi_tuong = chon_tu_dong_nghia(random.choice(doi_tuong_su_dung))
    chat_lieu_chon = chon_tu_dong_nghia(random.choice(chat_lieu))
    tinh_nang_chon = chon_tu_dong_nghia(random.choice(tinh_nang))
    cam_giac_chon = chon_tu_dong_nghia(random.choice(cam_giac))
    kich_thuoc = random.choice(kich_co)
    cau_yeu_cau = random.choice([
        "Tôi muốn tìm một loại trang phục",
        "Tôi cần một bộ đồ",
        "Tôi đang tìm kiếm một kiểu trang phục",
        "Hãy gợi ý cho tôi một trang phục",
        "Tôi muốn một bộ đồ"
    ])

    # Tạo câu mô tả
    mo_ta = f"{cau_yeu_cau} là {loai} {mau} làm từ chất liệu {chat_lieu_chon}, phong cách {phong_cach_chon}, {tinh_nang_chon}, dành cho {doi_tuong}, mang lại cảm giác {cam_giac_chon}, kích thước {kich_thuoc}."
    
    # Áp dụng lỗi chính tả cho từng từ
    mo_ta_loi = " ".join([tao_loi_chinh_ta(tu) for tu in mo_ta.split()])
    
    return mo_ta_loi

# Số lượng mô tả cần tạo
so_luong_mo_ta = 10000
mo_ta_tap_hop = set()

# Tạo và lưu các mô tả không trùng lặp vào tập hợp
while len(mo_ta_tap_hop) < so_luong_mo_ta:
    mo_ta = tao_mo_ta()
    mo_ta_tap_hop.add(mo_ta)  # Tự động loại bỏ các mô tả trùng lặp

# Chuyển tập hợp thành danh sách
mo_ta_danh_sach = list(mo_ta_tap_hop)

# Tạo DataFrame từ danh sách mô tả
df = pd.DataFrame(mo_ta_danh_sach, columns=['Mô tả sản phẩm'])

# Lưu vào file CSV
df.to_csv('Data_Training.csv', index=False, encoding='utf-8')

print(f"Đã tạo thành công {so_luong_mo_ta} mô tả sản phẩm không trùng lặp và lưu vào file 'mo_ta_san_pham_voi_yeu_cau.xlsx'.")
