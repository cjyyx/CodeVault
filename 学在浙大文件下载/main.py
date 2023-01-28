# %%
import requests
import json
import tqdm
import os
# from urllib.request import urlretrieve
# import wget
# %%
course_id = 51579

activities_url = "https://courses.zju.edu.cn/api/courses/{}/activities"
document_url = "https://courses.zju.edu.cn/api/uploads/reference/document/{}/url?preview=true"
# %%
headers = {
    "Cookie": "BSFIT_pi620=yJhELJkEyJDRI2ycLO,y2pZy2DXyJy3LS,y2pEI2hXyJy3yO; BSFIT_52q/y=; BSFIT_53ys6=; BSFIT_5h1m4=9SE0JH93IS4zJSaFJP,9m4QJHkW9mqZJ5,9m5FIS/W9m4WI5,9m5KIm9W9m9WJP,9m529HkW9m9QIP,9m529mqW9m/3J5; BSFIT_l7xtp=; BSFIT_gm+2B=65yVpOkwL5gc6czwLg,62BxL26w62zX6S; BSFIT_ozmhA=; BSFIT_5oy60=; BSFIT_6A05x=; BSFIT_hwz19=ImD02Co5nm95219e2h,I1hSImDSImhc2g,I1hS213SI1dCng; BSFIT_5iBp4=; BSFIT_x/n8g=; BSFIT_qpkBr=; BSFIT_zw05t=HKECJ5gCBKvABjgDBQ,H5txBAzXH5tXHz; BSFIT_yl1s0=; BSFIT_h807u=; BSFIT_4w70j=L+UDq+41BYk5L+FaBN,L04DL0CNL0CYqr; BSFIT_7s6tp=; BSFIT_xqAp0=wN1E9NwKwN1J9pxHwg,wpxHwjxMwpkM92; BSFIT_7A32n=; BSFIT_t8min=; BSFIT_o37w+=; BSFIT_7lvAj=; BSFIT_hug/7=5R1c3RJFB/Ed3/J25V,5/7WBj5V5/IcBV,5/h25RZV5/hW5V,5/h25W5V5/hd3I; BSFIT_k06hj=; BSFIT_ty7n+=; BSFIT_onkgr=; BSFIT_i0k62=KNUHK6Uf+6MLKfbZ+i,K6iLK64ZK63LKi; BSFIT_ty2B4=; BSFIT_i+yu4=; BSFIT_/l6Ai=; BSFIT_7/2Cw=; BSFIT_wu2+6=z1WTz1j0pUzAz1S0pS,z+6KpV9Az+gKpg; BSFIT_zm5By=; BSFIT_1y+Ck=BhPVBh9fwCk0qe3MqL,BCkQqf3WBCkfqL; BSFIT_rl0mq=; BSFIT_yvg3A=; BSFIT_52h0l=wFkHwjlMBjTewFTeB+,w0lywFTMw0+zr+,w05HwjwMw0+cB+,w05Dw0wMw0wyB+,w05zBj+Mw0wHw+,w05zBj9Mw0wHwT,w05zBj3Mw0wDwT,w05zBzkMw0wHBM,w05HBzTMw0+KB5,w05yBFQMw0+ywM; BSFIT_h8qzu=; lang=zh-CN; _ga_RSHERGT34X=GS1.1.1653046172.1.1.1653046384.0; _ga=GA1.3.1744784656.1645541262; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1666092267,1667261931; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1668000938; _csrf=S8mwplVi9KWoF2WQ0TlCeJfXE6JpRIep0mwzxuZuY5w%3D; _pv0=czmlBsOqKSg4Cupv9Kk6vWPjxx8xaeaI1kPrQoxoyZm7S76gADMFwHfHTwgFeLYLm3JunXr8vi6qyRPNkVzcC5QD7%2Fgkm%2BkWDZY5O1DNyix98rMjxD1T%2B3zXdEjU8NbKzE3nCBPB5b2ZIEzEuaRzEQITEHbKGFAdDFPAB2gBev3DQAGRhfTuYkVGazbKOHDCuS2hwunREB6dA6%2BnO8okDmREroBcAitgj9Y7bll%2F5n3PWg6FCrFEL0oZXEF6j5i89A3M%2ByX3kt4%2BZMwnH7HNZ%2Fbc9O51mxB0pmhhg%2FhspN%2FAwSXk4ubPMNCetK1Dx%2FG%2FqJWgd7%2Bpqq9ZhsB5DLJ3A%2FmuCrdHSkPpjIHC39LEMuwzP8AHtOlTmBoLri6guoPo3ZghFfsaTmTAVSq3D3iH%2BUuJi9wJXuNszmMaZangveU%3D; _pf0=mtuzs21Y4c1%2BO67tqJRxZs1pz%2FXuMssN7Cu4Y4ahICw%3D; _pc0=kIPrjKcNR8EKDSCUeg2depi6YMad7Iproo%2BPDQaOAb7PnDzTbdO91RoJacu1vx8j; iPlanetDirectoryPro=%2BSjPnBJQ6MliQZC4o3Ta%2Bqkr5yVNHw4uMZJdKz3HCKos0juVrjs9uecg5tWGARwYxKiZEl473zOV5ykQz5C4fRBb0Bd4zLxqTH5VH3l9Cj1dcZ3%2Bhv8UpO%2FOPW6DD7R%2Bpa1Dgi6tSyDPr5WHpy7%2BIZtTcLc%2BToJtuETSbjZsPhSyqhqBlanJ97ID0Z%2BDt6OMUkcUdlPDoVMkJ7PgNy0O6niedKzliLl8YNs%2F73zGCoCgIuY6kNIqvCpAvlv1m55waHJS5%2B6PKV4oC6Zjgx3J4o4NPbfcNZyOCYgxMCxVTiUdqX7OJA4IM1jAScSBLMrhjrrTPbsSSpkJjQOAst1S72GDrLzF2Ypfx3o6K8%2FzDy1XiLwz4tqE0b%2F9eoWk0mqg; route=91f4597d05e1312b78298311d2684137; _gat=1; fp_ver=4.7.15; BSFIT_EXPIRATION=1668027418976; BSFIT_DEVICEID=Q7wGa737AliTmgnlw83srr_8Tx-EEKFQ2WQRgv6kvE8nVLlj8B6KWBtHWApqwVp6InVyleeRsfFYkzKrgSWkRwSwR7mcDjcSeXtphW-a3oieGLlmjB_WE4xbdYxuBy74PXJVhMOXjCK3CncKG4qCPL_5FM5CvYt1; BSFIT_59+r4=GSN2Kr5VGSHeGRdxKH,Gr4x0rCVGrHzGH; session=V2-1-cf4db345-e7f3-4efc-8e9b-12459a4b4e1a.MTYwOTE4.1668087891134.k3awM6gMb8Y_einLnXJSIfMvPKU",
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
