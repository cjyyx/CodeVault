# %%

headers = {
    "cookie": "acw_tc=2f76e2d016773256789853306e86d49f53bc5b0657f5955c32d950947e; SESSION=ada57427-4421-478d-a9de-61b3bffdd62a; JSESSIONID=43F1C87ADFFA9F654750C9965A75EC5E; t_sid=ada57427-4421-478d-a9de-61b3bffdd62a; c_uid=5005461889; u_name=cjyyyy12; i_pd=9cf65d05fcc1b26fdfd76fc0fbc958dc; Hm_lvt_fa78e84859eb94eefe7235ad3e483e9f=1677325700; currentChoiceRoleMenuId=5000003863; SERVERID=987ae75ad05152c48774f44de4990a8c|1677326544|1677325679; Hm_lpvt_fa78e84859eb94eefe7235ad3e483e9f=1677326547",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
}

url = "https://abook.hep.com.cn/selectResource.action?user=2&roleMenuId=5000003863&currentChoiceRoleMenuId=5000003863"

# %%
import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import fitz

# %%

def security_filename(name: str) -> str:
    '''移除非法文件名字符'''
    replace_char = '''/\:*?"<>|.'''
    for char in replace_char:
        while char in name:
            name = name.replace(char, '')
    return name

def img2pdf():
    """ 把img_result下所有imgdir转换成pdf，保存到pdf_result中
     """
    if(not os.path.exists("pdf_result")):
        os.mkdir("./pdf_result")
    for imgdir in os.listdir("./img_result"):
        try:
            print("img2pdf ", imgdir)
            doc = fitz.open()
            for img in tqdm(sorted(os.listdir("./img_result/"+imgdir))):  # 读取图片，确保按文件名排序
                imgdoc = fitz.open(
                    "./img_result/{}/{}".format(imgdir, img))  # 打开图片
                pdfbytes = imgdoc.convert_to_pdf()  # 使用图片创建单页的 PDF
                imgdoc.close()
                imgpdf = fitz.open("pdf", pdfbytes)
                doc.insert_pdf(imgpdf)  # 将当前页插入文档
            doc.save("./pdf_result/{}.pdf".format(imgdir))  # 保存pdf文件
            doc.close()
        except Exception as e:
            print(e)


# %%

def getKeys(url)->list:
    """ 
    获得各课件的title,id
     """

    html = requests.get(url,headers=headers).text

    soup = BeautifulSoup(html, 'html.parser')
    liEs=soup.find_all("li", {'class': "iconLi"})

    keys=[]
    for li in liEs:
        key={
            "id":re.findall(r'\d+(?=,)', li.a["href"])[0],
            "title":security_filename(li.img["title"]),
        }
        print("发现文档：{}".format(key["title"]))
        keys.append(key)

    print('-'*10)
    print("共找到{}个文档".format(len(keys)))
    
    return keys


# %%

def download_doc_img(key):
    """ 
    key{title,id} 
     """
    
    if(not os.path.exists("img_result")):
        os.mkdir("./img_result")

    purl="https://abook.hep.com.cn/showResource.action?resourceInfoId={}&resBrowserUrl=undefined&mediaType=0&currCount=1&ifUser=DATA_IDS"

    newhtml=requests.get(purl.format(key["id"]),headers=headers).text

    soup = BeautifulSoup(newhtml, 'html.parser')
    div=soup.find("div",{"id":"video_box_id"})

    os.makedirs("./img_result/{}".format(key["title"]))

    img_url=div.iframe["src"][:-5]+".files/{}.png"
    i=1
    while(1):
        req=requests.get(img_url.format(i))
        if(req.status_code==requests.codes.ok):
            with open("./img_result/{}/{:0>4d}.png".format(key["title"],i),"wb") as f:
                f.write(req.content)
        else:
            break
        i+=1



# %%

# with open("test.html","w",encoding="utf-8") as f:
#     f.write(doc_html)


if __name__=="__main__":
    

    keys=getKeys(url)

    print("开始下载")

    for key in tqdm(keys):
        download_doc_img(key)

    print('-'*10)
    print("开始转换成pdf")
    img2pdf()

