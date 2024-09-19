# %%
import json
import os

import cv2
import fitz  # pip install PyMuPDF
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance, ImageFilter
from tqdm import tqdm


def security_filename(name: str) -> str:
    """移除非法文件名字符"""
    replace_char = """/\:*?"<>|."""
    for char in replace_char:
        while char in name:
            name = name.replace(char, "")
    return name


# %%


def download_pptimg(course_id, sub_id, name="default"):
    """下载图片到pptimg/{name}/"""
    if not os.path.exists("pptimg"):
        os.mkdir("./pptimg")
    if not os.path.exists("./pptimg/{}".format(security_filename(name))):
        os.mkdir("./pptimg/{}".format(security_filename(name)))
    url = "http://classroom.zju.edu.cn/pptnote/v1/schedule/search-ppt?course_id={}&sub_id={}&page={}&per_page=100"

    r_list = []
    count = 1
    while 1:
        tempList = requests.get(url.format(course_id, sub_id, count))
        print(url.format(course_id, sub_id, count))
        print(tempList)
        tempList = tempList.json()["data"]["list"]
        r_list.extend(tempList)
        count += 1
        if len(tempList) < 100:
            break

    print("download ", name)
    # print(r_list)
    for i in tqdm(range(len(r_list))):
        pptimgurl = json.loads(r_list[i]["content"])["pptimgurl"]
        c = requests.get(pptimgurl).content
        with open(
            "./pptimg/{}/ppt{:04d}.jpg".format(security_filename(name), i + 1), "wb"
        ) as f:
            f.write(c)


# %%


def download_sub_list(course_id):
    """爬取sublist并下载到pptimg/title/"""
    headers = {
        "Cookie": r"""
_ga=GA1.3.1594330328.1696573249; lang=zh-CN; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1705642395; device_token=97648f2c031313488126181ccb7b2956; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; _csrf=S8mwplVi9KWoF2WQ0TlCeAg%2F4xsS%2BF28vtYtxrDs0GU%3D; _pv0=jyVJ9igKi24glTFxOT27vO9yWaHBkiDajfm%2Fdh3uyAOF6B2WnIBLF1%2FQIaCxq87nia%2Fh09HKvir28prTaIQG3AcJEO5AFf59at97Xf8KsfolwDgUfms3sr5tw9ZIpYaBEIksbH74qSK1%2BwEC2OPeWl5D2XLvH7lgKAHqDoH1VECuNj%2Fft1Uv5Oqk8IzLN5QdZTtWzfAg6%2Bwr9DvgKwcWh29qxk0S%2BHhI1xkNcUrf6FI%2BG5i%2BO%2FfKhH1vDoLB0ydIum0mN%2B%2BLdu97%2BFCNVTxbOstein2j2BysHbAm899MoeJy1uNoRhmkMHjQ8rdxNcQ3dhvtdY35joN7n40dcufksUO0HaqM3ezSGhqDVqdYLOOQqHEKTrFit%2FNpDCyUbDyEwKKjsqUCSuI5kjIPFoojurnmZG9V3unx6uqWaKwxOH0%3D; _pf0=qcynJIwVU6yNEwvqUbX05WkDPX8b7KEKxD5NKnIXgcY%3D; _pc0=kIPrjKcNR8EKDSCUeg2deiqK5m6fIlXuoY8qoBnj5h1AnSr4AjaCDMBi72Y0TLJe; iPlanetDirectoryPro=Y2M1lWhWNz4qZMDLvQANSDf96DWiC%2BsEkSli%2FNq14KFkNjEkWi87pW4KU4c4z7cyan6HTFnK6Oj6nPkwtqf%2Biqarju8zNCY7OJ4JqeJvSDbfZiVbkysxzJQ4ncamzSzc5sPP5g00knw%2Bjlbmq5%2BtgCCKCEzDr9%2F8IIT0fLl4n4K0aQedSj7sWTri%2FX7cogEM8tWe6S7GZZr9PEzT%2B6YfjoPekPz1AeD5JjTcdCTdBNSDVQ1nDHW6lRaqtiz4BOEGC1CdEl3G6R5B2BjvE5L5NNVb0B6c%2B57dZx%2F8O1jupgY2G0zHhwU%2F%2FOf5X7pbET%2BxvmM%2BOyyTMH6fi5t3yQAh4Ow28RP%2BhLplc%2BTQo5v8nQu3ohGDv6KGI3EIsez39vP9; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1715569034,1715932184,1716614470,1717141515; login_cmc_id=e6594f5a75e2456c6b02e98b7015f7eb; login_cmc_tid=30d2942943a3899c1d3112d53b804738; group_code=1800000448; login_cmc_url=https%3A%2F%2Ftgmedia.cmc.zju.edu.cn%2Flogin1800000448.html; login_cmc_type=2; cmc_version=v3; _token=6190c0d146bf715feb2e25ac43d352ec8d6cf66a7f254eedd41c6d55216b3b40a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22_token%22%3Bi%3A1%3Bs%3A648%3A%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiMzIxMDEwMzUyMiIsImNtY0dyb3VwQ29kZSI6IjE4MDAwMDA0NDgiLCJjbWNHcm91cElkIjoiZjE4YjhmNGVlNDBiY2QwNzY1Y2ZlOTg3Y2E4MjA0NmUiLCJleHAiOjE3MTcyMjc5MTcsImxvZ2luVHlwZSI6ImRlZmF1bHQiLCJtcm9sZXMiOlt7ImNtY19yb2xlIjoiNmJiMmE0NWM3Yjc3NGJkNjZhZjMzYWRmODgwZmFlYTMiLCJjb2RlIjoic3R1ZGVudCIsImNyZWF0ZWRfYXQiOiIyMDIxLTA3LTMwIDE0OjQzOjE3IiwiZGVzY3JpcHRpb24iOiIiLCJkaXNwbGF5X25hbWUiOiLlrabnlJ8iLCJpZCI6MjA1LCJpc2RlZmF1bHQiOiIwIiwic3RhdHVzIjowfV0sInBhc3N3b3JkIjoiNDJiOWZmM2IyNDlkYTM5N2Y0NDMyNGE4YjY0YmIxMzQiLCJyZWFsbmFtZSI6IumZiOmUpuavhSIsInN1YiI6NDY3ODk2LCJ0ZW5hbnRfaWQiOjExMn0.ypig79QodHKiC_kotn1WwSxR4nvEI6AuLONrfeg9bsQ%22%3B%7D; PHPSESSID=5ck6epolejeijcl0eokcgblsog; Hm_lpvt_35da6f287722b1ee93d185de460f8ba2=1717142059; _csrf=461d379a21ff44f30937b5f3a43e183d9024d19bb2d3feea1b5a7e402516c277a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22HokQW1A-rSJ8SrSiTmJaLDSZTkmli9Ay%22%3B%7D
        """,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }
    url = "https://courses.zju.edu.cn/api/courses/{}/extension-lives?source=chinamcloud_live"
    r = requests.get(url.format(course_id), headers=headers).json()
    print("爬取sub_list：\n", r, "\n结束sub_list")
    r = r["lives"]
    for a in r:
        if a["status"] == "expired":
            download_pptimg(a["id"], a["sub_id"], a["title"])


# %%


def imgBrightness(img1, c=1.2, b=3):
    """
    给每个像素点的三个通道加减一个值，增加亮度
    - 变暗 rst = imgBrightness(img, 0.5, 3)
    - 变亮 rst = imgBrightness(img, 1.5, 3)
    """
    rows, cols, channels = img1.shape
    blank = np.zeros([rows, cols, channels], img1.dtype)
    rst = cv2.addWeighted(img1, c, blank, 1 - c, b)
    return rst


def ppt_enhance(reverse=False):
    """把pptimg下所有图片强化
    - reverse反色
    """
    for imgdir in os.listdir("./pptimg"):
        print("imgEnhance ", imgdir)
        pppath = "./pptimg/Enhanced_" + imgdir
        os.mkdir(pppath)
        for img in tqdm(os.listdir("./pptimg/" + imgdir)):
            iimg = cv2.imread("./pptimg/{}/{}".format(imgdir, img))
            if reverse:
                iimg = 255 - iimg

            # 提高亮度
            iimg = imgBrightness(iimg, 1.25)

            # 调整对比度
            # 创建 CLAHE 对象 clipLimit 限制对比度，tileGridSize 块的大小
            clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(12, 12))
            b, g, r = cv2.split(iimg)
            b1 = clahe.apply(b)
            g1 = clahe.apply(g)
            r1 = clahe.apply(r)
            iimg = cv2.merge([b1, g1, r1])

            # 提高清晰度
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
            iimg = cv2.filter2D(iimg, -1, kernel=kernel)

            # 保存文件
            cv2.imwrite("{}/{}".format(pppath, img), iimg)


# %%


def ppt_enhance2():
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


# %%

# img=Image.open("./pptimg/2022-09-13第6-6节/ppt0002.jpg")
# plt.imshow(img)
# img=ImageEnhance.Brightness(img).enhance(1.25)
# img=ImageEnhance.Contrast(img).enhance(1.2)
# img=ImageEnhance.Sharpness(img).enhance(2)
# plt.imshow(img)

# %%


def img2pdf():
    """把pptimg下所有imgdir转换成pdf，保存到pptpdf中"""
    if not os.path.exists("pptpdf"):
        os.mkdir("./pptpdf")
    for imgdir in os.listdir("./pptimg"):
        try:
            print("img2pdf ", imgdir)
            doc = fitz.open()
            for img in tqdm(
                sorted(os.listdir("./pptimg/" + imgdir))
            ):  # 读取图片，确保按文件名排序
                imgdoc = fitz.open("./pptimg/{}/{}".format(imgdir, img))  # 打开图片
                pdfbytes = imgdoc.convert_to_pdf()  # 使用图片创建单页的 PDF
                imgdoc.close()
                imgpdf = fitz.open("pdf", pdfbytes)
                doc.insert_pdf(imgpdf)  # 将当前页插入文档
            doc.save("./pptpdf/{}.pdf".format(imgdir))  # 保存pdf文件
            doc.close()
        except Exception as e:
            print(e)


# %%


if __name__ == "__main__":
    # download_sub_list(50590)
    # download_pptimg(
    #     course_id=50660,
    #     sub_id=898607,
    # )
    ppt_enhance2()
    img2pdf()
