# %%
from config import *
from utils import *
import os
import requests
import json
import shutil
import time
from PIL import Image, ImageFilter, ImageEnhance

if (os.path.exists(ppt_dir)):
    with open(f"{ppt_dir}/annotation.json", "r") as f:
        annotation = json.load(f)
    if (annotation["course_id"] == course_id and annotation["sub_id"] == sub_id):
        pass
    else:
        shutil.rmtree(ppt_dir)
        os.mkdir(ppt_dir)
else:
    os.mkdir(ppt_dir)
    annotation = {
        "course_id": course_id,
        "sub_id": sub_id
    }
    with open(f"{ppt_dir}/annotation.json", "w") as f:
        json.dump(annotation, f, indent=4)

if (not os.path.exists(enhanced_ppt_dir)):
    os.mkdir(enhanced_ppt_dir)

# %%


def get_ppt_list():

    url = "http://classroom.zju.edu.cn/pptnote/v1/schedule/search-ppt?course_id={}&sub_id={}&page={}&per_page=100"

    r_list = []
    count = 1
    while (1):
        tempList = requests.get(
            url.format(course_id, sub_id, count),
            proxies=proxies
        ).json()['list']
        r_list.extend(tempList)
        count += 1
        if (len(tempList) < 100):
            break

    ppt_list = [
        {
            "i": i,
            "pptimgurl": json.loads(x["content"])["pptimgurl"],
            "create_time": x["create_time"],
            "created_sec": x["created_sec"]
        }
        for i, x in enumerate(r_list)
    ]

    return ppt_list


def download_img(url, path):
    print(f"下载 PPT {url} 至 {path}")
    c = requests.get(url, proxies=None).content
    with open(path, "wb") as f:
        f.write(c)

def stretch_image(image, width_ratio, height_ratio):
    width, height = image.size
    target_width = int(width * width_ratio)
    target_height = int(height * height_ratio)
    stretched_image = image.resize((target_width, target_height))
    return stretched_image

def enhance_img(image):
    iimg  = image
    iimg = stretch_image(iimg,1.5,1.8)
    iimg = ImageEnhance.Brightness(iimg).enhance(1.25)
    iimg = ImageEnhance.Contrast(iimg).enhance(1.2)
    iimg = ImageEnhance.Sharpness(iimg).enhance(2)
    return iimg

# %%

while 1:

    ppt_list = get_ppt_list()

    for ppt in ppt_list:
        path = f"{ppt_dir}/{ppt['i']}.jpg"
        enhanced_path = f"{enhanced_ppt_dir}/{ppt['i']}.png"
        if (not os.path.exists(path)):
            download_img(ppt["pptimgurl"], path)
        if (not os.path.exists(enhanced_path)):
            img = Image.open(path)
            enhanced_img = enhance_img(img)
            enhanced_img.save(enhanced_path)

    time.sleep(1)


