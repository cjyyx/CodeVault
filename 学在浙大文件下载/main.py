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
    "Cookie": "lang=zh-CN; _csrf=S8mwplVi9KWoF2WQ0TlCeC4lUodLg76Kw2lX0dp%2BpYA%3D; _pv0=HlewuJ0Z0bi8foMA%2BcH2cvVvLbxEaSHDCHJKSIgjbXYVCMrF29eF%2Fyppx2nS9cbnjMHYksniNfXjdq37jjJs9f%2FRzPBaJeTu1GzY8UCXRB02LwekVH%2BH7FA6k4FCubkdV%2Bu1wxWmA5iGDCNqDdmACQ8GSqUeNyUqaeUBi5zdoVPyDpLzBdjlpOCla1905SmLlSzQY1oIuQXb7qv0nuDBvYW6XUxMHqm5pW0O7J2fh8R48vdIgWrWxSPMM6a9yfLZ4WMoPHIex3Ehbl5z1%2BD3bggq%2FJEPcFTOHisVrgG0TwtXFXLYL2kvGNqw2QQ%2BPon8QgRuFgw72y6L90xSz53Nh9fSKcMiZesrbzL7uD5bmhhYYFg6pHmInQLWIubW8sD19mfOZBnnntwxUdgvdNgp1hBdqG4S1SGr%2BwqyTRNUJ%2Fw%3D; _pf0=nN1S%2FVG75tal0ZZNswaiQvdiuHI4bDZlegSLp%2FKvkjA%3D; _pc0=kIPrjKcNR8EKDSCUeg2denuLzc56VJCWxm33XvZqQMaIr%2BL%2Bd%2F20nzjLoKHtcoh%2F; iPlanetDirectoryPro=suQ4IExcWEUZA2ruCvZzxucE0ofXy6kP0Pz1KtMVcQS4ExiOSeMkB9w%2BofLdXzoiz1yK7SwqnYp7y7cBteBw4SdM%2ByT03ogKJVDMeXn1LQwG1cPSBHwsRieOW2%2F8UTg15Q0eIrlJfuXhYLG7WtVMkXolUvgw%2BfMSKJ6Is6QPIJFfNCPEhqDjm%2Boubnn4BQO1CfWGqo7g7q4Xw5eWcAgFmfAukuV%2BVwLzJ%2FzR512HQ%2ByjKo2rszzcVXsI6W7WJB%2F4URM9Cb37cpvlgWycKYfiDu2wZq8Y7Ple4904suRKKX0ORRNEZLT64dC0kc4hvDvBjkB39cBerRQYP1aWXRjCpHbl1fMTfk5EtMo%2BTDq5eAXEUXWAgIEWMpj2cmUYwEPq; _ga=GA1.3.1049916803.1676973780; _gat=1; session=V2-1-c25630a4-e3f6-4674-b8eb-180d9b0a538b.MTYwOTE4.1677060384507.kk9XsdwCrllEQlZnt6xxhponRag",
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
