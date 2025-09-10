# %%
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import plot_daily_usage_time

plt.rcParams["figure.dpi"] = 300


# 设置字体为SimHei（黑体）
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
# 解决负号显示问题
matplotlib.rcParams["axes.unicode_minus"] = False

# %%

data_file = "data/AppUsage_day_2025_9_2_20_51_40.txt"

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

all_usage_data = []
for entry in structured_data:

    date = entry["date_obj"]
    all_usage = entry["apps"]["ALL"]["使用时长"] / (1000 * 3600)

    all_usage_data.append((date, all_usage))

usage_df = pd.DataFrame(all_usage_data, columns=["date", "usage"])
usage_df["date"] = pd.to_datetime(usage_df["date"])
usage_df.sort_values(by="date", inplace=True)
usage_df.reset_index(drop=True, inplace=True)
usage_df

# %%

# 电池循环计数数据

loop_date = ["2024/1/2", "2024/1/31", "2024/2/19", "2024/3/2", "2024/3/30", "2024/4/17", "2024/5/11", "2024/6/4", "2024/6/26", "2024/7/22", "2024/8/7", "2024/8/27", "2024/9/14", "2024/9/26", "2024/10/7", "2024/10/24", "2024/11/15", "2024/12/1", "2024/12/21", "2025/1/6", "2025/1/22", "2025/2/15", "2025/3/8", "2025/3/25", "2025/4/16", "2025/5/14", "2025/6/2", "2025/6/20", "2025/7/12", "2025/8/12", "2025/9/2"]

loop_count = [267, 296, 318, 332, 358, 376, 400, 423, 445, 473, 494, 519, 534, 548, 562, 578, 604, 618, 641, 658, 676, 704, 723, 740, 763, 791, 811, 827, 858, 901, 927]

loop_df = pd.DataFrame({"date": pd.to_datetime(loop_date, format="%Y/%m/%d"), "loop_count": loop_count})
loop_df = loop_df.sort_values("date").reset_index(drop=True)
loop_df

# %%

results = []
# 从第二个采样点开始遍历，计算与前一个点之间的差异
for i in range(1, len(loop_df)):
    # 当前采样点和上一个采样点的数据
    end_record = loop_df.iloc[i]
    start_record = loop_df.iloc[i - 1]

    start_date = start_record["date"]
    end_date = end_record["date"]

    delta_loops = end_record["loop_count"] - start_record["loop_count"]

    period_usage_df = usage_df.query("date >= @start_date and date <= @end_date")
    total_usage_hours = period_usage_df["usage"].sum()
    period_days = (end_date - start_date).days

    if delta_loops > 0:
        hours_per_cycle = total_usage_hours / delta_loops
        days_per_cycle = period_days / delta_loops

        results.append(
            {
                "start_date": start_date,
                "end_date": end_date,
                "period_days": period_days,
                "delta_loops": delta_loops,
                "total_usage_hours": total_usage_hours,
                "hours_per_cycle": hours_per_cycle,
                "days_per_cycle": days_per_cycle,
            }
        )

result_df = pd.DataFrame(results)
result_df

# %%

plt.figure(figsize=(14, 7))

result_df.plot("start_date", "hours_per_cycle")

plt.title("每个电池循环的可用小时数随时间变化趋势", fontsize=16)
plt.xlabel("日期", fontsize=12)
plt.ylabel("每循环可用小时数 (小时/循环)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)  # 让日期显示更清晰
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 7))

result_df.plot("start_date", "days_per_cycle")

plt.title("每个电池循环的电池使用天数随时间变化趋势", fontsize=16)
plt.xlabel("日期", fontsize=12)
plt.ylabel("每循环使用天数 (天/循环)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
