# %%
import requests
import json
import tqdm
import os
# from urllib.request import urlretrieve
# import wget
# %%
course_id = 57479

activities_url = "https://courses.zju.edu.cn/api/courses/{}/activities"
document_url = "https://courses.zju.edu.cn/api/uploads/reference/document/{}/url?preview=true"
# %%
headers = {
    "Cookie": "lang=zh-CN; _ga=GA1.3.1049916803.1676973780; device_token=0c153f9e02283e9884a3a07af778dcfb; JWTUser=%7B%22account%22%3A%223210103522%22%2C%22id%22%3A467896%2C%22tenant_id%22%3A112%7D; Hm_lvt_fe30bbc1ee45421ec1679d1b8d8f8453=1686897518,1686910195,1686913599,1687175680; Hm_lvt_35da6f287722b1ee93d185de460f8ba2=1686013609,1686496295,1686730408,1687332156; BSFIT_+5pxl=Hso4BbjbBQg4BQlbBg,Hx+1BQ+eHxneB+; route=fb5ee7e10de5ba251c427d2afdd710ce; _csrf=S8mwplVi9KWoF2WQ0TlCeKobUtU56qp2YVALLnk5KEU%3D; _pv0=O%2BS%2FCxg4K7dSCngI4mMATS9KtOnomAFPRvEX63tLVnOFkgeKVUHahGrLGcAvYRXsjadSYiTYPUsvqEFF8MFOjoTpfkDlesBB30qFxcVqfptQtsxQNFfnRK%2B3BHdi2hltlAeD%2BPVlVcug6Ta6E58Y9gsVSbUdK22%2Bpzk8p9WPkc30CVX7YAMJy5yQjlM0kAaGg27VzyJgykWnhm2YCagNCm94EQtwdvznPmX8WdydbgGLrY3QJg6BcqcBZg0olcHM3QgM9pWiq6zprL1RCIHWZVi1rv8strSOg%2FM%2FCkjv7TC%2BhXnoO3BHPfCJ6M3KLI8A9i7yzzCSgu%2BTADVNqJBTVqcFv5Ck%2FRDomMY2XTr8TiEWZ7xHtQyoB7Yi9AgwVr9xoOzBSFYnJ86HJZniGp%2FYD9USmHQdbhHQZyjoq2Upeik%3D; _pf0=ttoatTAkRr1YMpkNER9mVfVPkv3QaaJwdz%2B%2Btkoz%2BbI%3D; _pc0=kIPrjKcNR8EKDSCUeg2desG7PrqkDaYkZxUtHUQj14puyi5K27IbOl9ppVUaaCY6; iPlanetDirectoryPro=hAciaXNm%2Bu8oKFfOiqbdmVjxZ7LsxjJ1FY0f17s3u10MzeEa9qJE6%2BdWnRQ1ZceGC5dhvG%2Bj9InpzmCzrM3CRAwYV9IEAjBjLF1liPjNk0z3Zz9WZMDnTwqJR%2FhASdWPNSJ21DM4ExrHlVAb18rxUvTzTDMROpSEWTQu0oOr4gz5k408%2BA7DX9zXOPZwwOdoP3vqmmRB6ndUx6rqR4FZFhP95bjr8LAEuW1saKeG1t1qLeMXFmtVV9FIfb5a6pNe3wIc1nNDqf%2BbK5HrVutLuvdhBp1xnW%2F3Rc5rs7inYez5gK3q%2F6YFayOAtiMKk5%2F0G5rc8ZtTRCuPZppIiIJt7D6%2BMCe%2FcQGZXfUME9e%2B3z5Ys3vR046jrRpDE7CBjXHz; __ts=1687505596006; _gat=1; BSFIT_EXPIRATION=1687539916182; BSFIT_DEVICEID=OMT5NeSCH095LB6gc6VX5l8-Hp8mKmvr1uryt4SDFSc1H-T1_sGEcBO-TsyxI4lSrkmp5XXI0CWR7j8tV3ZHTlWv0Kw_DANVQg5a4ophsuwxsPUogZhszOl5-EQVeRkz-Q4FQRPerqniXFrwVPcgagY43xgkH_Sb; BSFIT_1zt7l=How4GByYGowYG71AG1,H7lOxowYH75Ox5; BSFIT_1zt7l=How4GByYGowOGVfWGf,H71BGVwYH79WH1; session=V2-1-5c373cc7-be28-42c0-94ff-2b9823ded727.MTYwOTE4.1687592083529.P8-ALCMsmgWbbkCISPVXlkpv2_I",
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
