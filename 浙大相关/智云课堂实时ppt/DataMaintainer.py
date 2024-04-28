# %%
from config import *
from utils import *
import os
import requests
import json
import shutil
import time
from PIL import Image, ImageEnhance

if (not os.path.exists(data_path)):
    os.mkdir(data_path)

# %%


def get_ppt_list(course_id, sub_id):

    url = "http://classroom.zju.edu.cn/pptnote/v1/schedule/search-ppt?course_id={}&sub_id={}&page={}&per_page=100"

    r_list = []
    count = 1
    while (1):
        tempList = requests.get(
            url.format(course_id, sub_id, count),
            proxies={"http": None, "https": None}
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
    # print(f"下载 img {url} 至 {path}")
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
    iimg = image
    iimg = stretch_image(iimg, 1.5, 1.8)
    iimg = ImageEnhance.Brightness(iimg).enhance(1.25)
    iimg = ImageEnhance.Contrast(iimg).enhance(1.2)
    iimg = ImageEnhance.Sharpness(iimg).enhance(2)
    return iimg

# %%


def course_maintain(course_id):
    course_path = f"{data_path}/{course_id}"
    if (not os.path.exists(course_path)):
        os.mkdir(course_path)

    url = "https://yjapi.cmc.zju.edu.cn/courseapi/v2/course/catalogue?course_id={}"

    req = requests.get(
        url.format(course_id),
        proxies={"http": None, "https": None}
    ).json()

    sub_list = [
        {
            'title': x['title'],
            'sub_id':x['sub_id'],
            'status':x['status'],
            'start_at':x['start_at'],
        }
        for x in req['result']['data']
    ]
    # status 6: 已放完，1: 正在放，2: 还未放
    sub_list = sorted(sub_list, key=lambda sub: sub['start_at'])

    for sub in sub_list:
        if (sub['status'] == '2'):
            continue
        sub_maintain(course_id, sub['sub_id'])


def sub_maintain(course_id, sub_id):
    sub_path = f"{data_path}/{course_id}/{sub_id}"
    if (not os.path.exists(sub_path)):
        print(f"发现新 sub {course_id}/{sub_id}")
        os.makedirs(sub_path)
    ppt_dir = f"{sub_path}/ppt"
    if (not os.path.exists(ppt_dir)):
        os.mkdir(ppt_dir)
    enhanced_ppt_dir = f"{sub_path}/enhanced_ppt"
    if (not os.path.exists(enhanced_ppt_dir)):
        os.mkdir(enhanced_ppt_dir)

    ppt_list = get_ppt_list(course_id, sub_id)

    for ppt in ppt_list:
        ppt_path = f"{ppt_dir}/{ppt['i']}.jpg"
        if (not os.path.exists(ppt_path)):
            print(f"发现新 ppt {ppt['pptimgurl']}")
            download_img(ppt["pptimgurl"], ppt_path)
        enhanced_ppt_path = f"{enhanced_ppt_dir}/{ppt['i']}.png"
        if (not os.path.exists(enhanced_ppt_path)):
            img = Image.open(ppt_path)
            enhanced_img = enhance_img(img)
            enhanced_img.save(enhanced_ppt_path)

# %%

if __name__ == "__main__":

    # for course_id in course_id_list:
    #     course_maintain(course_id)

    # while 1:
    #     sub_maintain(
    #         course_id=52993,
    #         sub_id=991048
    #     )
    #     time.sleep(1)

    course_maintain(
        course_id=54578
    )
