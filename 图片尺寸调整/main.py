""" 
https://blog.csdn.net/boysoft2002/article/details/117919526
 """

# %%
import os
from tqdm import tqdm
from PIL import Image

# %%

out_size=(4528, 6732)

for filename in tqdm(os.listdir("./input")):
    img = Image.open("./input/{}".format(filename))
    out = img.resize(out_size,Image.ANTIALIAS)
    out.save("./output/{}".format(filename),'png')

