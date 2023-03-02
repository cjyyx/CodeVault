# %%

catalogue=""

with open("电工电子学目录.txt","r",encoding="utf-8") as f:
    catalogue=f.read()

catalogue_list=list(map(
    lambda x:x.split("\t"),
    catalogue.split("\n")
))

# %%

mm_data=[{
    "name": "电工电子学",
    "children":[]
}]


for line in catalogue_list:
    if(len(line)==1):
        node={
            "name":line[0],
            "children":[]
        }
        mm_data[0]["children"].append(node)
    elif(len(line)==2):
        node={
            "name":line[1],
            "children":[]
        }
        mm_data[0]["children"][-1]["children"].append(node)
    elif(len(line)==3):
        node={
            "name":line[2],
            "children":[]
        }
        mm_data[0]["children"][-1]["children"][-1]["children"].append(node)
        pass


