import math
import time
import cv2
import numpy as np
import glob

# Lấy thông tin ảnh đầu vào
W = 960
H = 720
K = 1/24
T = K * W   # T = 40

#Bộ lọc morphological để lọc nhiễu
def morphological(img):
    # k1, k2, k3 = 1/80, 1/48, 1/64 với a = ki * min(W, H) làm tròn xuống đến số lẻ để dễ tính toán
    a1 = 9
    a2 = 15
    a3 = 11
    kernel1 = np.ones((a1, a1), np.uint8)
    kernel2 = np.ones((a2, a2), np.uint8)
    kernel3 = np.ones((a3, a3), np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel1)
    erosion = cv2.erode(closing, kernel2, iterations=1)
    dilation = cv2.dilate(erosion, kernel3, iterations=1)
    return dilation

# hàm main
if __name__ == '__main__':
    images_list = glob.glob('data/outputs/*.jpg')
    for img_path in images_list:
        t1 = time.time()
        img_name = img_path.split("\\")[-1]
        img = cv2.imread(img_path, 2)

        # chuyển sang ảnh nhị phân
        ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
        img = morphological(img)

        #Tìm tập hợp các điểm biên của phân đoạn ảnh
        l, r = [], []
        for i in range(H):
            l_, r_ = 0, 0
            for j in range(W):
                if img[i][j] == 255 and l_ == 0:
                    l.append((i, j))
                    l_ = 1
                    break
            for j in range(W):
                if img[i][W-1-j] == 255 and r_ == 0:
                    r.append((i, W-1-j))
                    r_ = 1
                    break
        img = cv2.imread(img_path)

        #In các điểm biên
        # for i in range(len(l)):
        #     lx, ly = l[i][0], l[i][1]
        #     rx, ry = r[i][0], r[i][1]
        #     img[lx - 3:lx + 3, ly - 3:ly + 3, :] = (0, 255, 0)
        #     img[rx - 3:rx + 3, ry - 3:ry + 3, :] = (0, 255, 0)

        # Tính toán điểm điều hướng
        #for i in range(len(l)):
        lx, ly = l[250][0], l[250][1]
        rx, ry = r[250][0], r[250][1]
        x = (lx+rx)//2
        y = (ly+ry)//2

        #draw rectangle
        #img[x-4:x+4, y-4:y+4, :] = (0, 255, 0)

        #draw circle
        cv2.circle(img, (y, x), 5, (0, 255, 0), -1)
        cv2.circle(img, (480, 720), 5, (255, 0, 0), -1)

        #draw line
        start_point = (480, 720)
        end_point = (y, x)
        color = (0, 255, 255)
        thickness = 2
        cv2.arrowedLine(img, start_point, end_point, color, thickness)

        #Calculate corner and distance
        a = abs(480 - y)
        b = abs(720 - x)
        c = math.sqrt((a*a)+(b*b))
        tan_corner = a/c
        corner_rad = math.atan(tan_corner)
        rad = 57.295779513
        corner = corner_rad * rad
        if(y < 480):
            corner = corner + 90
        else:
            corner = 90 - corner
        print("Corner: ", corner, "\nDistance: ", c)

        #Show image
        #cv2.imshow('show_image', img)
        #cv2.waitKey(0)
        cv2.imwrite('data/local/'+img_name, img)
        t2 = time.time()
        print('Thời gian: {}'.format(t2 - t1))

