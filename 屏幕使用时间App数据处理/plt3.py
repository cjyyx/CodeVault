# %%
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# 设置字体为SimHei（黑体）
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
# 解决负号显示问题
matplotlib.rcParams["axes.unicode_minus"] = False

# %%
data_file = "AppUsage/AppUsage_day_2025_6_2_21_17_20.txt"

with open(data_file, "r", encoding="utf-8") as file:
    data = file.read()
lines = data.strip().split("\n")

# %%
structured_data = []

current_data = {}
for line in lines:
    if line.startswith("202"):  # 检查是否是日期行
        date_str = line.split(",")[0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        current_data["date_obj"] = date_obj
        current_data["apps"] = {}
    elif len(line) == 0:
        structured_data.append(current_data)
        current_data = {}
    else:
        # 解析应用数据
        parts = line.split(",")
        if len(parts) > 1:  # 确保是应用数据行
            app_data = {
                "应用名称": parts[1].strip(),
                "应用标识": parts[2].strip(),
                "格式化时间": parts[3].strip(),
                "使用时长": int(parts[4].strip()),
                "启动次数": int(parts[5].strip()),
                "通知次数": int(parts[6].strip()),
            }
            current_data["apps"][app_data["应用标识"]] = app_data

# %%

novel_apps = [
    "com.qidian.QDReader",
    "com.sfacg",
    "com.kuangxiangciweimao.novel",
    "com.dragon.read",
    "com.tencent.mtt",
    "com.txtqbmf.zjqy",
]

media_apps = [
    "com.tencent.mm",
    "com.tencent.mobileqq",
    "com.zhihu.android",
    "com.baidu.tieba",
    "com.sina.weibo",
    "com.xingin.xhs",
    "com.coolapk.market",
    "com.xiaomi.vipaccount",
]

data = []
for entry in structured_data:
    date_obj = entry["date_obj"]

    all_usage_time = 0
    novel_usage_time = 0
    media_usage_time = 0
    else_usage_time = 0

    if "ALL" in entry["apps"]:
        all_usage_time = entry["apps"]["ALL"]["使用时长"] / (
            1000 * 3600
        )  # 以小时为单位
    for app_id in novel_apps:
        if app_id in entry["apps"]:
            novel_usage_time += entry["apps"][app_id]["使用时长"] / (1000 * 3600)
    for app_id in media_apps:
        if app_id in entry["apps"]:
            media_usage_time += entry["apps"][app_id]["使用时长"] / (1000 * 3600)
    else_usage_time = all_usage_time - novel_usage_time - media_usage_time

    novel_usage_rate = novel_usage_time / all_usage_time
    media_usage_rate = media_usage_time / all_usage_time
    else_usage_rate = else_usage_time / all_usage_time

    data.append(
        (
            date_obj,
            all_usage_time,
            novel_usage_time,
            media_usage_time,
            else_usage_time,
            novel_usage_rate,
            media_usage_rate,
            else_usage_rate,
        )
    )

df = pd.DataFrame(
    data,
    columns=[
        "date",
        "all_usage_time",
        "novel_usage_time",
        "media_usage_time",
        "else_usage_time",
        "novel_usage_rate",
        "media_usage_rate",
        "else_usage_rate",
    ],
)
df.set_index("date", inplace=True)

# %%

# plt.figure(figsize=(10, 6))
plt.scatter(df["novel_usage_time"],df["all_usage_time"], alpha=0.7)
plt.xlabel("小说应用使用时间 (小时)")
plt.ylabel("总使用时间 (小时)")
plt.grid(True)
# plt.axis('equal')  # 设置横纵坐标比例单位相同
plt.show()


# %%

plt.scatter(df["novel_usage_rate"],df["all_usage_time"], alpha=0.7)
plt.xlabel("小说应用使用时间占比")
plt.ylabel("总使用时间 (小时)")
plt.grid(True)
plt.show()

# %%

plt.scatter(df["media_usage_time"],df["else_usage_time"], alpha=0.7)
plt.xlabel("社交媒体应用使用时间 (小时)")
plt.ylabel("其他应用使用时间 (小时)")
plt.grid(True)
plt.show()

# %%

plt.scatter(df["media_usage_rate"],df["else_usage_rate"], alpha=0.7)
plt.xlabel("社交媒体应用使用时间占比")
plt.ylabel("其他应用使用时间占比")
plt.grid(True)
plt.show()

# %%


