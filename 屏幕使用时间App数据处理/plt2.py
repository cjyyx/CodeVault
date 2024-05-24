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
with open("AppUsage_example.txt", "r", encoding="utf-8") as file:
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

    data.append(
        (
            date_obj,
            all_usage_time,novel_usage_time,media_usage_time,else_usage_time,
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
    ],
)
df.set_index("date", inplace=True)

# %%

# 计算14日平均值
df_avg = df.rolling(window=14).mean()

# 绘制图表
plt.figure(figsize=(12, 6))
plt.plot(df_avg.index, df_avg["all_usage_time"], label="总使用时间")
plt.plot(df_avg.index, df_avg["novel_usage_time"], label="小说应用使用时间")
plt.plot(df_avg.index, df_avg["media_usage_time"], label="社交媒体应用使用时间")
plt.plot(df_avg.index, df_avg["else_usage_time"], label="其他应用使用时间")

# 设置横坐标为年月，间隔为一个月
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(matplotlib.dates.MonthLocator())

plt.xlabel("日期")
plt.ylabel("14日平均使用时间（小时）")
plt.title("应用使用时间统计")
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()

# %%


