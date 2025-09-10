# %%

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# %%


def display_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame_rgb)
    plt.show()


# %%


input_video = os.listdir("input")[0]
input_video_path = os.path.join("input", input_video)
print(f"输入视频路径：{input_video_path}")

# %%

cap = cv2.VideoCapture(input_video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"总帧数：{total_frames}")
print(f"帧率：{fps}")
print(f"分辨率：{width}x{height}")

# %%

frame_index_to_extract = int(2.5 * fps)  # xx秒对应的帧索引

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index_to_extract)
ret, frame = cap.read()

display_frame(frame)

# %%

template = frame.copy()
template_lab = cv2.cvtColor(template, cv2.COLOR_BGR2LAB)
template_lab = template_lab.astype("float32")

cap.release()


def match_histograms(source):
    """
    通过直方图匹配实现色彩迁移。
    :param source: 待处理的帧
    :return: 经过色彩校正的帧
    """
    # 将图像从 BGR 转换为 L*a*b* 色彩空间
    # L*a*b* 空间更适合进行色彩匹配，因为它将亮度（L）与颜色（a、b）分离开来。
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
    source_lab = source_lab.astype("float32")

    # 对每个色彩通道（L, a, b）进行直方图匹配
    for i in range(3):
        hist_source, _ = np.histogram(source_lab[:, :, i], 256, [0, 256])
        hist_template, _ = np.histogram(template_lab[:, :, i], 256, [0, 256])

        # 计算累积直方图
        cdf_source = hist_source.cumsum()
        cdf_template = hist_template.cumsum()

        # 归一化
        cdf_source = cdf_source / cdf_source[-1]
        cdf_template = cdf_template / cdf_template[-1]

        # 创建查找表 (Lookup Table)
        lookup_table = np.zeros(256, dtype=np.uint8)
        j = 0
        for k in range(256):
            while cdf_template[j] < cdf_source[k] and j < 255:
                j += 1
            lookup_table[k] = j

        # 应用查找表进行转换
        source_lab[:, :, i] = lookup_table[source_lab[:, :, i].astype(np.uint8)]

    # 将图像从 L*a*b* 转换回 BGR
    matched_image = cv2.cvtColor(source_lab.astype("uint8"), cv2.COLOR_LAB2BGR)
    return matched_image


# %%


def process_video(input_video_path, output_video_path):
    """
    处理视频，对每一帧进行色彩校正。
    :param input_video_path: 输入视频路径
    :param output_video_path: 输出视频路径
    """
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: 无法打开视频文件。")
        return

    # 获取视频属性
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 定义视频编码器和输出对象
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 或 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    frame_count = 0
    for _ in tqdm(range(total_frames)):
        ret, frame = cap.read()
        if not ret:
            break

        # 对当前帧进行色彩校正
        matched_frame = match_histograms(frame)

        # 写入处理后的帧
        out.write(matched_frame)
        frame_count += 1

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("视频处理完成！")


output_video_path = "output_corrected.mp4"
process_video(input_video_path, output_video_path)

# %%

os.system(f"ffmpeg -y -i {output_video_path} -c:v libx265 -crf 20 output_final.mp4")

# %%
