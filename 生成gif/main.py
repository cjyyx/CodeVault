# %%
from PIL import Image
import os

# %%

# 读取文件夹中的所有png图片
images = []
for file_name in os.listdir('input'):
    if file_name.endswith('.png'):
        image = Image.open(os.path.join('input', file_name))
        images.append(image)

# %%

# 根据文件名末尾数字进行排序
images.sort(key=lambda x: int(x.filename.split('.')[1]))

# %%

# 合成为gif动图并导出
images[0].save('output.gif', save_all=True, append_images=images[1:], duration=50, loop=0)
