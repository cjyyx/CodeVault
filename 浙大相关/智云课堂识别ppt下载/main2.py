# %%
import json
import os
import shutil
import datetime
import cv2  # pip install opencv-python
import fitz  # pip install PyMuPDF
import matplotlib.pyplot as plt  # pip install matplotlib
import numpy as np  # pip install numpy
import requests  # pip install requests
from PIL import Image, ImageEnhance, ImageFilter  # pip install pillow
from tqdm import tqdm  # pip install tqdm
import time


def security_filename(name: str) -> str:
    """移除非法文件名字符"""
    replace_char = """/\:*?"<>|."""
    for char in replace_char:
        while char in name:
            name = name.replace(char, "")
    return name


# %%

student = 3210103522
course_id = 72197
sub_id = 1541553

with open("myheaders.json", "r", encoding="utf-8") as f:
    headers = json.load(f)


# %%


def get_sub_list(course_id):
    url = "https://yjapi.cmc.zju.edu.cn/courseapi/v3/multi-search/get-course-detail?course_id={}&student={}"

    req = requests.get(url.format(course_id, student), headers=headers)
    if req.status_code != 200:
        raise Exception(f"course_id={course_id} 请求失败")

    data = req.json()["data"]
    title = data["title"]
    sub_list = data["sub_list"]

    p_list = []

    for year in sub_list.keys():
        for month in sub_list[year].keys():
            for week_count in sub_list[year][month].keys():
                # print(f"{year}年{month}月第{week_count}周")
                for p in sub_list[year][month][week_count]:
                    class_over = p["class_over"]
                    sub_title = p["sub_title"]
                    sub_id = p["id"]

                    if float(class_over) < time.time():
                        print(f"sub_id={sub_id} {sub_title} 已结束")
                        p_list.append({"sub_id": sub_id, "sub_title": sub_title})
                    else:
                        print(f"sub_id={sub_id} {sub_title} 没结束")

    return p_list


sub_list = get_sub_list(course_id)
sub_list


# %%


def download_pptimg(course_id, sub_id, name="default"):
    """下载图片到pptimg/{name}/"""
    if not os.path.exists("pptimg"):
        os.mkdir("./pptimg")

    download_path = f"./pptimg/{security_filename(name)}"
    if os.path.exists(download_path):
        shutil.rmtree(download_path)
        os.mkdir(download_path)
    else:
        os.mkdir(download_path)

    url = "https://interactivemeta.cmc.zju.edu.cn/pptnoteapi/v1/schedule/search-ppt?course_id={}&sub_id={}&page={}&per_page=100"

    r_list = []
    count = 1
    while 1:
        req = requests.get(url.format(course_id, sub_id, count), headers=headers)
        if req.status_code != 200:
            raise Exception(f"course_id={course_id} sub_id={sub_id} 请求失败")
        _tl = req.json()["list"]
        r_list.extend(_tl)
        count += 1
        if len(_tl) < 100:
            break

    pptimgurls = [json.loads(r["content"])["pptimgurl"] for r in r_list]

    print("download ", name)

    for i, pptimgurl in enumerate(tqdm(pptimgurls)):
        c = requests.get(pptimgurl).content
        img_type = pptimgurl.split(".")[-1]
        with open(f"{download_path}/ppt{i + 1:04d}.{img_type}", "wb") as f:
            f.write(c)


download_pptimg(course_id, 1541553)
# for sub in sub_list:
#     download_pptimg(course_id, sub["sub_id"], sub["sub_title"])


# %%


def ppt_enhance():
    """把pptimg下所有图片强化"""
    for imgdir in os.listdir("./pptimg"):
        print("imgEnhance ", imgdir)
        pppath = "./pptimg/Enhanced_" + imgdir
        os.mkdir(pppath)
        for img in tqdm(os.listdir("./pptimg/" + imgdir)):
            iimg = Image.open("./pptimg/{}/{}".format(imgdir, img))

            iimg = ImageEnhance.Brightness(iimg).enhance(1.25)
            iimg = ImageEnhance.Contrast(iimg).enhance(1.2)
            iimg = ImageEnhance.Sharpness(iimg).enhance(2)

            # 保存文件
            iimg.save("{}/{}".format(pppath, img))


ppt_enhance()


# %%


def img2pdf():
    """把pptimg下所有imgdir转换成pdf，保存到pptpdf中"""
    if not os.path.exists("pptpdf"):
        os.mkdir("./pptpdf")
    for imgdir in os.listdir("./pptimg"):
        try:
            print("img2pdf ", imgdir)
            doc = fitz.open()
            for img in tqdm(sorted(os.listdir("./pptimg/" + imgdir))):  # 读取图片，确保按文件名排序
                imgdoc = fitz.open("./pptimg/{}/{}".format(imgdir, img))  # 打开图片
                pdfbytes = imgdoc.convert_to_pdf()  # 使用图片创建单页的 PDF
                imgdoc.close()
                imgpdf = fitz.open("pdf", pdfbytes)
                doc.insert_pdf(imgpdf)  # 将当前页插入文档
            doc.save("./pptpdf/{}.pdf".format(imgdir))  # 保存pdf文件
            doc.close()
        except Exception as e:
            print(e)


img2pdf()
