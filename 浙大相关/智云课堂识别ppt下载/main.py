# %%
import json
import os

import cv2  # pip install opencv-python
import fitz  # pip install PyMuPDF
import matplotlib.pyplot as plt  # pip install matplotlib
import numpy as np  # pip install numpy
import requests  # pip install requests
from PIL import Image, ImageEnhance, ImageFilter  # pip install pillow
from tqdm import tqdm  # pip install tqdm


def security_filename(name: str) -> str:
    """移除非法文件名字符"""
    replace_char = """/\:*?"<>|."""
    for char in replace_char:
        while char in name:
            name = name.replace(char, "")
    return name


# %%

headers = {
        "Cookie": r"""_pm0=O%2FF63v2vIbWixGdP4aITsOyjvrS6NcJCNvgKxqVSXLM%3D; lang=zh-CN; _ga=GA1.1.1132895987.1727158620; _csrf=S8mwplVi9KWoF2WQ0TlCeDFJQxrbMPmZ1oqHFTh%2Fmu4%3D; _pv0=7L7uNKQk4tuABXiKUh6UvVvtAeN8gmxiMuD0OF5Tfmosu505S%2FcFq4gWBSLQybfZKXJpMsld6vNv0qTwt%2BvMMSp7NQsND2fImR2K41IdUN%2FBzTWVx4f796tZgHjdoDhdfXiJqmiHYp%2FdsAXnF1fRiAOQwQ581osOHwCFYvrqEg31wVQMGSrmvhNV9%2Ffq%2BqfToVGR6bbf7JNoVBFG%2F1XPa3hHqHNC8FQB%2FtdPEhUC4QYhMaPqSwIkaPAb1Bo7Lo9GfGX2yo2TzWya6JPYc7Ftk3UUifRvmr5IwRTwSoEUI50RNMv8uzJNhzvgqlIL9D5I19YJARmMvj0T57x7IqWCKm2%2BegcdRmJRHVrmuV5%2BiD%2FSvm5akWbZnG9wSKpuEnPnTTB0rsgrEemI0BCRuIqo%2BpjmmTSCXNSTRw1PH9%2FJVm4%3D; _pf0=TguggYNJ7vF6lQbvB0qRnxPEZiEvaPLJ7mLhyegsYuk%3D; _pc0=kIPrjKcNR8EKDSCUeg2degUvJuXYKUCJHFJZL2r61tFTt9w63jLrrMKlVDkC%2BDZP; iPlanetDirectoryPro=IlWBhwjehJ9mYV1d0USo9L4%2Fx%2FG7Rj5AZ1FfZwlKWIG83Q%2FK6iOhCkrwjDbjkY1NQDz2bRCwkFMA%2FXoz2%2B9QVG%2FJ1A%2FWgST%2B5Tv%2FDy6QyvtW7Y5dvvrtfFffoT%2FB3rzvWxoi7r2V02aFz%2F1w0xODdTtHt9g0XpFjgME9dn6p7bfvZAKZOPU2teLEg1t5wZSm7OVgfYvN7cstMezT4nRb2iPtMySEngfGxpufx9aaijjK2vD4HmubdZcYKaZt3R3i%2BiSE2D0gCvJ2IejuqQUyzkf%2FB9T0P324Ot5AAF9mbr%2BTN45qvkuxOabNoMw6UjCk%2BXHadHc6lHst7VfQrMqVPA%2Fm5gE3UNJvV5zVnozB6FCiJoaRRltWDXrm%2FFW4iuPN; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1726901808,1727249338,1729333312; HMACCOUNT=28CDEFF586D59BC5; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; login_cmc_id=e6594f5a75e2456c6b02e98b7015f7eb; login_cmc_tid=b65edf64e16b072e2db5e7a86c3217ae; group_code=1800000448; login_cmc_url=https%3A%2F%2Ftgmedia.cmc.zju.edu.cn%2Flogin1800000448.html; login_cmc_type=2; cmc_version=v3; _token=eb8ad22a86f5056c9cb3a49b09da628a98500105a25d166bb36d69ddf5f856a1a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22_token%22%3Bi%3A1%3Bs%3A648%3A%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiMzIxMDEwMzUyMiIsImNtY0dyb3VwQ29kZSI6IjE4MDAwMDA0NDgiLCJjbWNHcm91cElkIjoiZjE4YjhmNGVlNDBiY2QwNzY1Y2ZlOTg3Y2E4MjA0NmUiLCJleHAiOjE3Mjk0MTk3MTQsImxvZ2luVHlwZSI6ImRlZmF1bHQiLCJtcm9sZXMiOlt7ImNtY19yb2xlIjoiNmJiMmE0NWM3Yjc3NGJkNjZhZjMzYWRmODgwZmFlYTMiLCJjb2RlIjoic3R1ZGVudCIsImNyZWF0ZWRfYXQiOiIyMDIxLTA3LTMwIDE0OjQzOjE3IiwiZGVzY3JpcHRpb24iOiIiLCJkaXNwbGF5X25hbWUiOiLlrabnlJ8iLCJpZCI6MjA1LCJpc2RlZmF1bHQiOiIwIiwic3RhdHVzIjowfV0sInBhc3N3b3JkIjoiNDJiOWZmM2IyNDlkYTM5N2Y0NDMyNGE4YjY0YmIxMzQiLCJyZWFsbmFtZSI6IumZiOmUpuavhSIsInN1YiI6NDY3ODk2LCJ0ZW5hbnRfaWQiOjExMn0.HOP-r-RBQG0Tp-0HvJgUJ_9XqqP5NVSLGckquXi-y64%22%3B%7D; _ga_H5QC8W782Q=GS1.1.1729333296.5.1.1729333317.39.0.0; PHPSESSID=ku13e9rao0mlk9jgf859opc8ta; _csrf=36e297d3c1a8f34e403099b1686bd1da0d0a9e0eaf31708c5d0a6ff5f5d0a9bda%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%222RNjYTFQAUvn_MAzqGgAOf3nBv5SlnHp%22%3B%7D; Hm_lpvt_35da6f287722b1ee93d185de460f8ba2=1729333721""",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }

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
        tempList = requests.get(url.format(course_id, sub_id, count),headers=headers)
        print(url.format(course_id, sub_id, count))
        print(tempList.json())
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
_pm0=O%2FF63v2vIbWixGdP4aITsOyjvrS6NcJCNvgKxqVSXLM%3D; lang=zh-CN; _ga=GA1.1.1132895987.1727158620; _csrf=S8mwplVi9KWoF2WQ0TlCeDFJQxrbMPmZ1oqHFTh%2Fmu4%3D; _pv0=7L7uNKQk4tuABXiKUh6UvVvtAeN8gmxiMuD0OF5Tfmosu505S%2FcFq4gWBSLQybfZKXJpMsld6vNv0qTwt%2BvMMSp7NQsND2fImR2K41IdUN%2FBzTWVx4f796tZgHjdoDhdfXiJqmiHYp%2FdsAXnF1fRiAOQwQ581osOHwCFYvrqEg31wVQMGSrmvhNV9%2Ffq%2BqfToVGR6bbf7JNoVBFG%2F1XPa3hHqHNC8FQB%2FtdPEhUC4QYhMaPqSwIkaPAb1Bo7Lo9GfGX2yo2TzWya6JPYc7Ftk3UUifRvmr5IwRTwSoEUI50RNMv8uzJNhzvgqlIL9D5I19YJARmMvj0T57x7IqWCKm2%2BegcdRmJRHVrmuV5%2BiD%2FSvm5akWbZnG9wSKpuEnPnTTB0rsgrEemI0BCRuIqo%2BpjmmTSCXNSTRw1PH9%2FJVm4%3D; _pf0=TguggYNJ7vF6lQbvB0qRnxPEZiEvaPLJ7mLhyegsYuk%3D; _pc0=kIPrjKcNR8EKDSCUeg2degUvJuXYKUCJHFJZL2r61tFTt9w63jLrrMKlVDkC%2BDZP; iPlanetDirectoryPro=IlWBhwjehJ9mYV1d0USo9L4%2Fx%2FG7Rj5AZ1FfZwlKWIG83Q%2FK6iOhCkrwjDbjkY1NQDz2bRCwkFMA%2FXoz2%2B9QVG%2FJ1A%2FWgST%2B5Tv%2FDy6QyvtW7Y5dvvrtfFffoT%2FB3rzvWxoi7r2V02aFz%2F1w0xODdTtHt9g0XpFjgME9dn6p7bfvZAKZOPU2teLEg1t5wZSm7OVgfYvN7cstMezT4nRb2iPtMySEngfGxpufx9aaijjK2vD4HmubdZcYKaZt3R3i%2BiSE2D0gCvJ2IejuqQUyzkf%2FB9T0P324Ot5AAF9mbr%2BTN45qvkuxOabNoMw6UjCk%2BXHadHc6lHst7VfQrMqVPA%2Fm5gE3UNJvV5zVnozB6FCiJoaRRltWDXrm%2FFW4iuPN; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1726901808,1727249338,1729333312; HMACCOUNT=28CDEFF586D59BC5; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; login_cmc_id=e6594f5a75e2456c6b02e98b7015f7eb; login_cmc_tid=b65edf64e16b072e2db5e7a86c3217ae; group_code=1800000448; login_cmc_url=https%3A%2F%2Ftgmedia.cmc.zju.edu.cn%2Flogin1800000448.html; login_cmc_type=2; cmc_version=v3; _token=eb8ad22a86f5056c9cb3a49b09da628a98500105a25d166bb36d69ddf5f856a1a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22_token%22%3Bi%3A1%3Bs%3A648%3A%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiMzIxMDEwMzUyMiIsImNtY0dyb3VwQ29kZSI6IjE4MDAwMDA0NDgiLCJjbWNHcm91cElkIjoiZjE4YjhmNGVlNDBiY2QwNzY1Y2ZlOTg3Y2E4MjA0NmUiLCJleHAiOjE3Mjk0MTk3MTQsImxvZ2luVHlwZSI6ImRlZmF1bHQiLCJtcm9sZXMiOlt7ImNtY19yb2xlIjoiNmJiMmE0NWM3Yjc3NGJkNjZhZjMzYWRmODgwZmFlYTMiLCJjb2RlIjoic3R1ZGVudCIsImNyZWF0ZWRfYXQiOiIyMDIxLTA3LTMwIDE0OjQzOjE3IiwiZGVzY3JpcHRpb24iOiIiLCJkaXNwbGF5X25hbWUiOiLlrabnlJ8iLCJpZCI6MjA1LCJpc2RlZmF1bHQiOiIwIiwic3RhdHVzIjowfV0sInBhc3N3b3JkIjoiNDJiOWZmM2IyNDlkYTM5N2Y0NDMyNGE4YjY0YmIxMzQiLCJyZWFsbmFtZSI6IumZiOmUpuavhSIsInN1YiI6NDY3ODk2LCJ0ZW5hbnRfaWQiOjExMn0.HOP-r-RBQG0Tp-0HvJgUJ_9XqqP5NVSLGckquXi-y64%22%3B%7D; _ga_H5QC8W782Q=GS1.1.1729333296.5.1.1729333317.39.0.0; PHPSESSID=ku13e9rao0mlk9jgf859opc8ta; Hm_lpvt_35da6f287722b1ee93d185de460f8ba2=1729333570; _csrf=36e297d3c1a8f34e403099b1686bd1da0d0a9e0eaf31708c5d0a6ff5f5d0a9bda%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%222RNjYTFQAUvn_MAzqGgAOf3nBv5SlnHp%22%3B%7D
        """,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
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
    download_pptimg(
        course_id=42036,
        sub_id=736109,
    )
    ppt_enhance2()
    img2pdf()
