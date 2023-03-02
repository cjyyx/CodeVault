
import xmind 


w = xmind.load("test.xmind") # 加载，如果不存在，创建新的工作布
s1=w.getPrimarySheet() # 得到第一页
s1.setTitle("first sheet") # 给第一页命名

r0=s1.getRootTopic() # 创建根节点
r0.setTitle("电工电子学") # 给根节点命名

catalogue=""

with open("电工电子学目录.txt","r",encoding="utf-8") as f:
    catalogue=f.read()

catalogue_list=list(map(
    lambda x:x.split("\t"),
    catalogue.split("\n")
))


for line in catalogue_list:
    if(len(line)==1):
        r0.addSubTopic().setTitle(line[-1])
    elif(len(line)==2):
        r0.getSubTopics()[-1].addSubTopic().setTitle(line[-1])
    elif(len(line)==3):
        r0.getSubTopics()[-1].getSubTopics()[-1].addSubTopic().setTitle(line[-1])


xmind.save(w, "test.xmind",only_content=True)