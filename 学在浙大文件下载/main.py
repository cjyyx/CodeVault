# %%
import requests
import json
import tqdm
import os
# from urllib.request import urlretrieve
# import wget
# %%
course_id = 55721

activities_url = "https://courses.zju.edu.cn/api/courses/{}/activities"
document_url = "https://courses.zju.edu.cn/api/uploads/reference/document/{}/url?preview=true"
# %%
headers = {
    "Cookie": "lang=zh-CN; _ga=GA1.3.1049916803.1676973780; device_token=0c153f9e02283e9884a3a07af778dcfb; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1681527349,1683775221; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1683430026,1683517894,1683790104,1683869783; _csrf=S8mwplVi9KWoF2WQ0TlCeNcFeyajPYqOh08cJCTZtBo%3D; _pv0=8CifdfVWdFfK31gaEaeAo24e4Gk%2BbBYrJFkAhzrwI7odWvTzdpAe9CEt3dW3pQvt6BPk4gcLZrHaNlH8LG580yMhfPw4MVhsMDpgsIkdNzGPDCvfUgXA7ZXqc0nQFXiPhAQzE3cMhzHWnl6fblPR%2F7KX5DTTBQd1V3slSPJWhNUPaaz4d0cO0ybFyfSt6EEcFidyDJ184jET5EFA%2F4F4D7uoqD7E2dIuD1D1mXfbs2seywDOist3uSTv4EgHfBTNl%2FNjTP%2FDcwGKPbHI%2BbGy41GlX8hwxUqaUppJNDFzYj5iRXt2Yfj320fgq93L%2BU9hbxRsoR7A5HOw92kj2JBxr57zbRRCX3QRRS%2F7DQWuXi%2BsfhBf4JCGrKC9QRNr0bGDUdcL%2F0%2ByTKdftunO5empZ33wK91zH4QmzvkAiehGXjU%3D; _pf0=ttoatTAkRr1YMpkNER9mVWMkKOitIJXHu7jHlqnpL98%3D; _pc0=kIPrjKcNR8EKDSCUeg2detmPZxzFSxKbs1ItrRFrqShTQlTgcEZ6yuncOQDcers3; iPlanetDirectoryPro=9CUYo9swi34odetm%2BxrTS4HiIcVwVZ09cddoc0madcsIsrIPgPh7N%2Bygq4Rgnok1kP9jO%2BWfxzTjTPKLStwBu6isZ1fMsH04IDgUv4aFMTJdo1yXCAmXjbM8vWHySP0TM5WFImRBiXTwt5dYamyMKGSFxyosP4iOUi%2FY8bG%2BagznPwWIqUYxhOh6fn14MboWHqGA2OXEEqMkWIdJZYd3TmZzFu7Ja71qQlAhp88p6VbEbwCrvX7UXaTIbpmFwIvG%2F1fllWN9lQawvhih1nouXsA646bNacslWqvBVanubUIQDkVvIK1IVN1BVxYj0UcxfU57ZLCvd207cuxCnj6%2FbcsNd9xITJJco3yGgSrtu4EYFDPfzQ%2F39g60Ui054kV4; _gat=1; session=V2-1-c4de4553-5282-4c7d-bbb4-f74bd3bc519c.MTYwOTE4.1684331831134.V35kZ-9HFXGlogdaLELgDN6x4rk",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
}
acs = requests.get(activities_url.format(course_id), headers=headers).text

# %%
# with open("test.html","w",encoding="utf-8")as f:
#     f.write(acs)

# %%
acs = json.loads(acs)

# %%

redos = []
for gg in acs["activities"]:
    for dd in gg["uploads"]:
        # print(dd["reference_id"])
        redos.append(dd)

# %%

fdf = open("log.txt", "w", encoding="utf-8")
for dd in tqdm.tqdm(redos):
    rrr = requests.get(document_url.format(
        dd["reference_id"]), headers=headers).json()
    fdf.write(dd["name"]+"\t"+rrr["url"]+"\n")

    na=dd["name"]
    if(os.path.splitext(na)[-1] in [".pptx",".ppt",".docx",".doc",".xlsx",".xls"]):
        na+=".pdf"

    with open("dds/"+na,"wb") as f:
        f.write(requests.get(rrr["url"],headers=headers).content)

    # urlretrieve(rrr["url"],'dds/'+dd["name"])

    # wget.download(rrr["url"], 'dds/'+dd["name"])
fdf.close()
