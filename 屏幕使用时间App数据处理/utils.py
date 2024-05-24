import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import date2num
from scipy.interpolate import PchipInterpolator, make_interp_spline


def plot_daily_usage_time(
    df: pd.DataFrame,
    figsize=None,
    title=None,
    xlabel=None,
    ylabel=None,
    ylim=None,
    xtickMonthLocatorInterval=None,
    xticks_rotation=None,
):
    # 绘制使用时间变化曲线
    plt.figure(figsize=figsize)

    # 使用样条插值使曲线平滑
    x = date2num(df.index.to_pydatetime())
    y = df['usage_time'].values
    x_new = np.linspace(x.min(), x.max(), 300)

    # spl = make_interp_spline(x, y, k=3)  # k=3 表示三次样条
    # y_smooth = spl(x_new)
    pchip = PchipInterpolator(x, y) # PCHIP插值
    y_smooth = pchip(x_new)

    # 生成平滑曲线的日期索引
    date_range = mdates.num2date(x_new)

    plt.plot(date_range, y_smooth, label='Smooth curve')  # 平滑曲线
    plt.plot(df.index, df['usage_time'], 'o')  # 原始数据点

    plt.title(title)

    plt.xlabel(xlabel)
    if xtickMonthLocatorInterval:
        # 设置横坐标按月显示间隔
        plt.gca().xaxis.set_major_locator(
            mdates.MonthLocator(interval=xtickMonthLocatorInterval)
        )
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    if xticks_rotation:
        plt.xticks(rotation=xticks_rotation)  # 旋转横坐标标签以便更好地显示
    
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(*ylim)
    
    plt.grid(True)
    plt.show()
