import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random
from improved_apf import APF_Improved
import time
import glob

W = 960
H = 720
K = 1/24
T = K * W   # T = 40

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

def cal_goal(img_path):
    img = cv2.imread(img_path, 2)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    img = morphological(img)
    goal_r, goal_c = H-1, W//2
    for i in range(H):
        # l: mép đường trái, r: mép đường phải, d: động rộng đường
        l, r, d = 0, 0, 0
        count = 0
        for j in range(W):
            if img[H-1-i][j] == 255:
                count += 1
                if j == W-1 and d < count:
                    r, d = j, count
            elif count != 0:
                if d < count:
                    d = count
                    r = j-1
                    count = 0
        if r < T or d < T:
            break
        goal_r = H-1-i
        goal_c = r-d//2
    return (goal_r, goal_c)

if __name__ == '__main__':
    #images_list = glob.glob('data/outputs/*.jpg')
    images_list = glob.glob('C:/Users/Dun/Desktop/nghiencuctrenleb/PID_Net/data/outputs/*.jpg')
    for img_path in images_list:
        img_name = img_path.split("\\")[-1]
        goal = cal_goal(img_path)

        img = cv2.imread(img_path, 2)
        img = cv2.resize(img, (24, 18), interpolation = cv2.INTER_NEAREST)

        k_att, k_rep = 1, 0.8
        rr = 3
        step_size, max_iters, goal_threashold = 1, 1000, 2
        step_size_ = 2

        start, goal = (12, 0), (goal[1]//40, 17-goal[0]//40)
        is_plot = False
        if is_plot:
            fig = plt.figure(figsize=(7, 7))
            subplot = fig.add_subplot(111)
            subplot.set_xlabel('X-distance: m')
            subplot.set_ylabel('Y-distance: m')
            subplot.plot(start[0], start[1], '*r')
            subplot.plot(goal[0], goal[1], '*r')

        obs = []
        for i in range(18):
            for j in range(24):
                if img[i][j] == 0:
                    obs.append((j, 17 - i))
        print('obstacles: {0}'.format(obs))
        for i in range(0):
            obs.append([random.uniform(2, goal[1] - 1), random.uniform(2, goal[1] - 1)])

        if is_plot:
            for OB in obs:
                circle = Circle(xy=(OB[0], OB[1]), radius=rr, alpha=0.3)
                subplot.add_patch(circle)
                subplot.plot(OB[0], OB[1], 'xk')
        t1 = time.time()
        # path plan
        if is_plot:
            apf = APF_Improved(start, goal, obs, k_att, k_rep, rr, step_size, max_iters, goal_threashold, is_plot)
        else:
            apf = APF_Improved(start, goal, obs, k_att, k_rep, rr, step_size, max_iters, goal_threashold, is_plot)
        apf.path_plan()
        t2 = time.time()
        print('Thời gian được sử dụng để tìm 1000 lần: {}, Thời gian được sử dụng để tìm 1 lần: {}'.format(t2 - t1, (t2 - t1) / 1000))

        #img_path = 'data/inputs/' + img_name
        img_path = 'C:/Users/Dun/Desktop/nghiencuctrenleb/PID_Net/data/inputs/' + img_name
        img = cv2.imread(img_path)
        if apf.is_path_plan_success:
            path = apf.path
            path_ = []
            i = 0
            while i < len(path):
                path_.append(path[i])
                i += int(step_size_ / step_size)

            if path_[-1] != path[-1]:
                path_.append(path[-1])
            print('planed path points:{}'.format(path_))
            print('path plan success '+img_name)
            if is_plot:
                px, py = [K[0] for K in path_], [K[1] for K in path_]
                subplot.plot(px, py, '^k')
                plt.show()
                for i in range(len(px)):
                    r = int(H-1-py[i]*40)
                    c = int(px[i]*40)
                    cv2.circle(img, (c, r), 5, (0, 0, 255), 2)
                    #img[r-10:r+10, c-10:c+10, :] = (255, 0, 0)
            else:
                px, py = [K[0] for K in path_], [K[1] for K in path_]
                for i in range(len(px)):
                    r = int(H - 1 - py[i] * 40)
                    c = int(px[i] * 40)
                    cv2.circle(img, (c, r), 5, (0, 0, 255), 2)
                    # img[r-10:r+10, c-10:c+10, :] = (255, 0, 0)
            cv2.imwrite('C:/Users/Dun/Desktop/nghiencuctrenleb/PID_Net/data/plans/'+img_name, img)
        else:
            print('path plan failed')