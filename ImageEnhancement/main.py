# %%
import cv2  
import numpy as np
import os
import matplotlib.pyplot as plt

# %%

def cv2imshow(img):
    # 从BGR变为RGB
    b, g, r = cv2.split(img)
    pltimg = cv2.merge([r, g, b])
    plt.imshow(pltimg)
    plt.show()

# %%
def imgBrightness(img1, c=1.5, b=3):
    """ 
    给每个像素点的三个通道加减一个值，增加亮度 
    - 变暗 rst = imgBrightness(img, 0.5, 3)
    - 变亮 rst = imgBrightness(img, 1.5, 3)
    """
    rows, cols, channels = img1.shape
    blank = np.zeros([rows, cols, channels], img1.dtype)
    rst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return rst

# %%

img= cv2.imread("./input/img (1).jpg")
cv2imshow(img)

# %%

# 清晰化
kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]], np.float32)
dst = cv2.filter2D(img, -1, kernel=kernel)
cv2imshow(dst)

# %%
rst=imgBrightness(dst,1.2)
cv2imshow(rst)
