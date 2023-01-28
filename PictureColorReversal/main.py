# %%
import os
import cv2
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

# %%
# img = cv2.imread("./input/ppt65.jpg")


def convert1(img):
    # 从BGR变为RGB
    b, g, r = cv2.split(img)
    img = cv2.merge([r, g, b])
    # plt.imshow(img)
    # plt.show()

    # 反色
    img = 255-img
    # plt.imshow(img)
    # plt.show()

    # 去绿色
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         if(np.linalg.norm(
    #             img[i][j]-np.array([0, 255, 0])
    #         ) < 200):
    #             img[i][j][0] = 255
    #             img[i][j][1] = 255
    #             img[i][j][2] = 255

    # plt.imshow(img)
    # plt.show()

    # 从RGB变为BGR
    r, g, b = cv2.split(img)
    img = cv2.merge([b, g, r])

    return img


# %%
# img = cv2.imread("./input/ppt65.jpg")

def convert2(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # plt.imshow(img, cmap="gray")
    # plt.show()

    # 反色
    img = 255-img
    # plt.imshow(img, cmap="gray")
    # plt.show()

    # 再将图片变为黑白图片（灰度值大于127的重置像素值为255，否则重置像素值为0，也就是通过阈值127将图像二值化-要么黑要么白）
    # ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # img=thresh
    # plt.imshow(img, cmap="gray")
    # plt.show()

    return img


# %%
for filename in tqdm(os.listdir("./input")):
    img = cv2.imread("./input/"+filename)
    out = convert1(img)

    cv2.imwrite("./output/out_"+filename, out)
