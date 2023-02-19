# Đây là mã python sử dụng thư viện OpenCV để chuyển đổi video thành hình ảnh.

# Import thư viện OpenCV và thư viện os
import cv2
import os

# Đọc video từ đường dẫn data/Demo.mp4
vid_cap = cv2.VideoCapture('data/Demo.mp4')

# Đọc frame đầu tiên của video
success, image = vid_cap.read()

# Khởi tạo biến count và đường dẫn lưu hình ảnh
count = 0
sv_path = 'data/inputs/'

# Vòng lặp để đọc từng frame trong video
while success:
    # Đọc frame kế tiếp
    success, image = vid_cap.read()

    # Resize hình ảnh về kích thước (960, 720)
    resize = cv2.resize(image, (960, 720))

    # Kiểm tra xem thư mục sv_path có tồn tại hay không, nếu không tồn tại thì tạo mới
    if not os.path.exists(sv_path):
        os.mkdir(sv_path)

    # Lưu hình ảnh mỗi 10 frame
    if count % 10 == 0:
        cv2.imwrite(sv_path + "%04d.jpg" % count, resize)

    # Nếu người dùng nhấn phím Esc, dừng vòng lặp
    if cv2.waitKey(10) == 27:
        break

    # Tăng biến count lên 1
    count += 1