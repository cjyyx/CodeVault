# %%
import json
import os

import cv2
import fitz
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from PIL import Image, ImageFilter, ImageEnhance


def security_filename(name: str) -> str:
    '''移除非法文件名字符'''
    replace_char = '''/\:*?"<>|.'''
    for char in replace_char:
        while char in name:
            name = name.replace(char, '')
    return name

# %%


def download_pptimg(course_id, sub_id, name="default"):
    """ 下载图片到pptimg/{name}/ """
    if(not os.path.exists("pptimg")):
        os.mkdir("./pptimg")
    os.mkdir("./pptimg/{}".format(security_filename(name)))
    url = "http://classroom.zju.edu.cn/pptnote/v1/schedule/search-ppt?course_id={}&sub_id={}&page={}&per_page=100"

    r_list = []
    count = 1
    while(1):
        tempList = requests.get(url.format(
            course_id, sub_id, count)).json()['list']
        r_list.extend(tempList)
        count += 1
        if(len(tempList) < 100):
            break

    print("download ", name)
    # print(r_list)
    for i in tqdm(range(len(r_list))):
        pptimgurl = json.loads(r_list[i]['content'])['pptimgurl']
        c = requests.get(pptimgurl).content
        with open("./pptimg/{}/ppt{:04d}.jpg".format(security_filename(name), i+1), "wb") as f:
            f.write(c)

# %%


def download_sub_list(course_id):
    """ 爬取sublist并下载到pptimg/title/ """
    headers = {
        "Cookie": "BSFIT_pi620=yJhELJkEyJDRI2ycLO,y2pZy2DXyJy3LS,y2pEI2hXyJy3yO; BSFIT_52q/y=; BSFIT_53ys6=; BSFIT_5h1m4=9SE0JH93IS4zJSaFJP,9m4QJHkW9mqZJ5,9m5FIS/W9m4WI5,9m5KIm9W9m9WJP,9m529HkW9m9QIP,9m529mqW9m/3J5; BSFIT_l7xtp=; BSFIT_gm+2B=65yVpOkwL5gc6czwLg,62BxL26w62zX6S; BSFIT_ozmhA=; BSFIT_5oy60=; BSFIT_6A05x=; BSFIT_hwz19=ImD02Co5nm95219e2h,I1hSImDSImhc2g,I1hS213SI1dCng; BSFIT_5iBp4=; BSFIT_x/n8g=; BSFIT_qpkBr=; BSFIT_zw05t=HKECJ5gCBKvABjgDBQ,H5txBAzXH5tXHz; BSFIT_yl1s0=; BSFIT_h807u=; BSFIT_4w70j=L+UDq+41BYk5L+FaBN,L04DL0CNL0CYqr; BSFIT_7s6tp=; BSFIT_xqAp0=wN1E9NwKwN1J9pxHwg,wpxHwjxMwpkM92; BSFIT_7A32n=; BSFIT_t8min=; BSFIT_o37w+=; BSFIT_7lvAj=; BSFIT_hug/7=5R1c3RJFB/Ed3/J25V,5/7WBj5V5/IcBV,5/h25RZV5/hW5V,5/h25W5V5/hd3I; BSFIT_k06hj=; BSFIT_ty7n+=; BSFIT_onkgr=; BSFIT_i0k62=KNUHK6Uf+6MLKfbZ+i,K6iLK64ZK63LKi; BSFIT_ty2B4=; BSFIT_i+yu4=; BSFIT_/l6Ai=; BSFIT_7/2Cw=; BSFIT_wu2+6=z1WTz1j0pUzAz1S0pS,z+6KpV9Az+gKpg; BSFIT_zm5By=; BSFIT_1y+Ck=BhPVBh9fwCk0qe3MqL,BCkQqf3WBCkfqL; BSFIT_rl0mq=; BSFIT_yvg3A=; BSFIT_52h0l=wFkHwjlMBjTewFTeB+,w0lywFTMw0+zr+,w05HwjwMw0+cB+,w05Dw0wMw0wyB+,w05zBj+Mw0wHw+,w05zBj9Mw0wHwT,w05zBj3Mw0wDwT,w05zBzkMw0wHBM,w05HBzTMw0+KB5,w05yBFQMw0+ywM; BSFIT_h8qzu=; lang=zh-CN; _ga_RSHERGT34X=GS1.1.1653046172.1.1.1653046384.0; _ga=GA1.3.1744784656.1645541262; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1668000938,1669449445; BSFIT_s23n5=; BSFIT_EXPIRATION=1669578105363; BSFIT_DEVICEID=EO2bw5XEsRpC1RuuIGC5dt2gJKLuday6be6q8awE3Ts2YT520HSbK0CctVdnck1pPwzAxPkT8zAo9riEw3JEa6yg0rMwhu2qYCdwqbooFTjJb30AT_SeSyMZCqeGIY_aZSGlnT5-wEX3tMdLi-PcKDECQdhZfa15; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; login_cmc_id=e6594f5a75e2456c6b02e98b7015f7eb; login_cmc_tid=02d08712121a3cfe12613dd26f6cd5ca; group_code=1800000448; login_cmc_url=https%3A%2F%2Ftgmedia.cmc.zju.edu.cn%2Flogin1800000448.html; login_cmc_type=2; cmc_version=v3; _token=af201fddf15f0fbd5856449eda308b10ecc2945b2b470db4e6eaa614d120276aa%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22_token%22%3Bi%3A1%3Bs%3A633%3A%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiMzIxMDEwMzUyMiIsImNtY0dyb3VwQ29kZSI6IjE4MDAwMDA0NDgiLCJjbWNHcm91cElkIjoiZjE4YjhmNGVlNDBiY2QwNzY1Y2ZlOTg3Y2E4MjA0NmUiLCJleHAiOjE2Njk2MDM0ODQsImxvZ2luVHlwZSI6ImRlZmF1bHQiLCJtcm9sZXMiOlt7ImNtY19yb2xlIjoiNmJiMmE0NWM3Yjc3NGJkNjZhZjMzYWRmODgwZmFlYTMiLCJjb2RlIjoic3R1ZGVudCIsImNyZWF0ZWRfYXQiOiIyMDIxLTA3LTMwIDE0OjQzOjE3IiwiZGVzY3JpcHRpb24iOiIiLCJkaXNwbGF5X25hbWUiOiLlrabnlJ8iLCJpZCI6MjA1LCJpc2RlZmF1bHQiOiIwIn1dLCJwYXNzd29yZCI6IjY2ZGRjMDRkNjgzOGQxNWNjZjM4Y2VkN2YwODZiZTQ3IiwicmVhbG5hbWUiOiLpmYjplKbmr4UiLCJzdWIiOjQ2Nzg5NiwidGVuYW50X2lkIjoxMTJ9.ZMRjR0YjQoi9oAl5n-9AcQ8r4sdIFW8hW3K4r9geEnI%22%3B%7D; _csrf=S8mwplVi9KWoF2WQ0TlCeExj5QuZeu3EydDw5YmMqgg%3D; _pv0=XvHxHHrJJ5iBNqxE5EBQallrs56LG7vGNM4VQ4vz0fJYJE6O6m8v8F%2F85qrR%2FBhRr%2FjR3HPw%2FrTWRln70WwxIKD7CfHNJXF799FkiiGHKYLSdv53C3aeM304%2BY6hlcFPeZRQxDwUGfDWHNMqqICWvC%2F08OJtHpbNvnWW%2Bp17mTyaxvXEezqZbom2IfUUiAhbzgvQmZd94AuDULvBWQ96OhIPXqJ1t1QYIz0YyAvHS26pLLIHgG1HCX%2BnFGSxFSbrrFHM4hKl54Tb%2BRoY1F0UK1ky3Uy36Lf8j3aOS8PTE79Okv8P4zyyO3ajqm9gYYbi%2FLUsg15Ja%2BhEnNhCGtM%2Fy6EKnePmFHlOT3DyGSnm6i3pdU73FyJ3%2F%2Bc3yBGu5n69alr%2F6zQJkAg%2F%2F5uTKSEW87MY7LtnKjrfox72YSV%2FtOw%3D; _pf0=mtuzs21Y4c1%2BO67tqJRxZno12GT1lCwdkhql3vCpf6o%3D; _pc0=kIPrjKcNR8EKDSCUeg2deovVOnRskXKM3Ac4orULfwTzAXVKGiy4%2Fz79GcpUgwgP; iPlanetDirectoryPro=QXCmIMNSqHqIgh84lKP7JM4Kna%2BYxcQSUr3KIT%2FBmz%2F%2BNLXkm8bIrz%2F1bUx7A1b%2FTim3QQ4v7cpRb%2Fl7BLdU2sJHuDKNRUXAGDd1%2F1npCHZYoYGFJinamiEWxPb%2BuPtDYERSpuhZX4v6KnzFJccx4kl1cWFibg8INun8bWj%2Bf7nk60fgyVlCT78WoEM9Iv7MxO%2FKt5L4umD1XHLD6DpuLtBgx2AfPelTRB3nwIx3IKuDu0RlTSqCX4fjwejuyb8tXgENFqv3CMyOfXf7Si5Yp1kCa49oIpmn2vKQxTg%2BIhfBtsDChRbrsn23r6ng8kWIOFObNEK3nkEnN4WQLF%2F4g1hQNvftTuKRZfq06ewk8MRzvnJEvay8pFGVWKTy0mIV; route=24c1ab9749e53cd7e554511d8a844ba9; _gat=1; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1667261931,1669517085,1669542526; Hm_lpvt_35da6f287722b1ee93d185de460f8ba2=1669542736; BSFIT_19gui=; session=V2-1-c1526f80-4b72-4679-9048-3197f59f0b75.MTYwOTE4.1669629223793.MJVTvdg3DsJSxKDRgVY_M-nhsw4",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
    }
    url = "https://courses.zju.edu.cn/api/courses/{}/extension-lives?source=chinamcloud_live"
    r = requests.get(url.format(course_id), headers=headers).json()
    print("爬取sub_list：\n", r, "\n结束sub_list")
    r = r["lives"]
    for a in (r):
        if(a["status"] == "expired"):
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
    rst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return rst


def ppt_enhance(reverse=False):
    """ 把pptimg下所有图片强化
    - reverse反色
     """
    for imgdir in os.listdir("./pptimg"):
        print("imgEnhance ", imgdir)
        pppath = "./pptimg/Enhanced_"+imgdir
        os.mkdir(pppath)
        for img in tqdm(os.listdir("./pptimg/"+imgdir)):
            iimg = cv2.imread("./pptimg/{}/{}".format(imgdir, img))
            if(reverse):
                iimg = 255-iimg

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
            kernel = np.array(
                [[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
            iimg = cv2.filter2D(iimg, -1, kernel=kernel)

            # 保存文件
            cv2.imwrite("{}/{}".format(pppath, img), iimg)

# %%


def ppt_enhance2():
    """ 把pptimg下所有图片强化
     """
    for imgdir in os.listdir("./pptimg"):
        print("imgEnhance ", imgdir)
        pppath = "./pptimg/Enhanced_"+imgdir
        os.mkdir(pppath)
        for img in tqdm(os.listdir("./pptimg/"+imgdir)):
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
    """ 把pptimg下所有imgdir转换成pdf，保存到pptpdf中

     """
    if(not os.path.exists("pptpdf")):
        os.mkdir("./pptpdf")
    for imgdir in os.listdir("./pptimg"):
        try:
            print("img2pdf ", imgdir)
            doc = fitz.open()
            for img in tqdm(sorted(os.listdir("./pptimg/"+imgdir))):  # 读取图片，确保按文件名排序
                imgdoc = fitz.open(
                    "./pptimg/{}/{}".format(imgdir, img))  # 打开图片
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
    #     course_id=46475,
    #     sub_id=794632,
    # )
    # ppt_enhance2()
    img2pdf()
