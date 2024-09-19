# %%
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from utils import plot_daily_usage_time

# 设置字体为SimHei（黑体）
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
# 解决负号显示问题
matplotlib.rcParams["axes.unicode_minus"] = False

# %%

data_file = "AppUsage/AppUsage_day_2024_9_19_11_12_55.txt"

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

print("所有应用日均用时数据")

# 提取应用标识为 ALL 的应用使用时间
data0 = []
for entry in structured_data:
    date_obj = entry["date_obj"]
    if "ALL" in entry["apps"]:
        usage_time = entry["apps"]["ALL"]["使用时长"] / (1000 * 3600)  # 以小时为单位
        data0.append((date_obj, usage_time))

# 创建 DataFrame
df = pd.DataFrame(data0, columns=["date", "usage_time"])
df.set_index("date", inplace=True)

# 按周汇总使用时间
dfw = df.resample("W").mean()

plot_daily_usage_time(
    dfw,
    figsize=(10, 5),
    title="日均用时按周变化曲线",
    ylabel="日均用时 (小时)",
    ylim=(2, 14),
)

# 按月汇总使用时间
dfm = df.resample("M").mean()

plot_daily_usage_time(
    dfm,
    figsize=(10, 5),
    title="日均用时按月变化曲线",
    ylabel="日均用时 (小时)",
    ylim=(4, 10),
)

# %%

print("小说类应用日均用时数据")

novel_apps = [
    "com.qidian.QDReader",
    "com.sfacg",
    "com.kuangxiangciweimao.novel",
    "com.dragon.read",
    "com.tencent.mtt",
    "com.txtqbmf.zjqy",
]

data_novel = []
for entry in structured_data:
    date_obj = entry["date_obj"]
    usage_time = 0
    for app_id in novel_apps:
        if app_id in entry["apps"]:
            usage_time += entry["apps"][app_id]["使用时长"] / (1000 * 3600)
    data_novel.append((date_obj, usage_time))

# 创建 DataFrame
df = pd.DataFrame(data_novel, columns=["date", "usage_time"])
df.set_index("date", inplace=True)
dfw = df.resample("W").mean()
plot_daily_usage_time(
    dfw,
    figsize=(10, 5),
    title="小说类应用日均用时按周变化曲线",
    ylabel="日均用时 (小时)",
)

dfm = df.resample("M").mean()
plot_daily_usage_time(
    dfm,
    figsize=(10, 5),
    title="小说类应用日均用时按月变化曲线",
    ylabel="日均用时 (小时)",
)

# %%

print("除小说类应用外的其他应用日均用时数据")

data_other = []
for entry in structured_data:
    date_obj = entry["date_obj"]
    all_usage_time = entry["apps"]["ALL"]["使用时长"] / (1000 * 3600)
    novel_usage_time = 0
    for app_id in novel_apps:
        if app_id in entry["apps"]:
            novel_usage_time += entry["apps"][app_id]["使用时长"] / (1000 * 3600)
    data_other.append((date_obj, all_usage_time - novel_usage_time))

df = pd.DataFrame(data_other, columns=["date", "usage_time"])
df.set_index("date", inplace=True)
dfw = df.resample("W").mean()
plot_daily_usage_time(
    dfw,
    figsize=(10, 5),
    title="除小说类应用外的其他应用日均用时按周变化曲线",
    ylabel="日均用时 (小时)",
)

dfm = df.resample("M").mean()
plot_daily_usage_time(
    dfm,
    figsize=(10, 5),
    title="除小说类应用外的其他应用日均用时按月变化曲线",
    ylabel="日均用时 (小时)",
)

# %%
