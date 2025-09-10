# %%
from PIL import Image
import os

# %%

# 读取文件夹中的所有png图片
image_files = []
for file_name in os.listdir("input"):
    if file_name.endswith(".png"):
        image_files.append(file_name)
image_files

# %%

# 测试排序
def extract_key(file_name):
    return int(file_name.split(".")[0][23:])
    return file_name.split(".")[0][23:]


[extract_key(file_name) for file_name in image_files]

# %%

# image_files.sort()
image_files.sort(key=extract_key)

image_files


# %%

images = [Image.open(os.path.join("input", file_name)) for file_name in image_files]

# %%

img = images[0].copy()
print(img.size, img.mode)

if img.mode != "RGBA":
    img = img.convert("RGBA")

# 将透明区域替换为某种背景色
background = Image.new("RGB", img.size, color=(252, 228, 236))
background.paste(img, mask=img.split()[-1])
# 裁剪图像
W = 450
H = 1000
C = 1340
D = 1080
cropped = background.crop((C - W / 2, D - H, C + W / 2, D))
cropped

# %%


def process(img):
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    background = Image.new("RGB", img.size, color=(252, 228, 236))
    background.paste(img, mask=img.split()[-1])
    W = 450
    H = 1000
    C = 1340
    D = 1080
    cropped = background.crop((C - W / 2, D - H, C + W / 2, D))
    return cropped


images = [process(img) for img in images]

# %%

# 合成为gif动图并导出
images[0].save("output.gif", save_all=True, append_images=images[1:], duration=200, loop=0)

# %%

# gif转mp4
# ffmpeg -i xxx.gif -vcodec libx264 -crf 10 -pix_fmt yuv420p -profile:v baseline -level 3.0 -movflags +faststart xxx.mp4
