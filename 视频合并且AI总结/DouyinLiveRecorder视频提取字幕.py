# %%
import os
import tempfile
from datetime import datetime

from utils import Log, BOS, audio2text

ffmpeg_path = "C:/Users/cjy/Desktop/DouyinLiveRecorder_v4.0.3/ffmpeg/ffmpeg.exe"
base_path = "C:/Users/cjy/Desktop/DouyinLiveRecorder_v4.0.3/downloads/B站直播/憨大炒股"

video_name = "憨大炒股_2025-08-17_19-06-29"

output_audio = f"results/{video_name}_合并.mp3"

# %%

log = Log("ffmpeg.log")
log.write(f"日志开始时间: {datetime.now()}\n")
log.breakpoint()

#### 提取音频文件 ####

video_list = [v for v in os.listdir(base_path) if v.startswith(video_name)]
video_list = sorted(video_list)
print("开始提取", video_list)

temp_dir = tempfile.mkdtemp()
print(f"临时目录创建于: {temp_dir}")

temp_audio_files = []

for i, video in enumerate(video_list):
    temp_audio = os.path.join(temp_dir, f"temp_audio_{i}.mp3")
    temp_audio_files.append(temp_audio)

    video = os.path.join(base_path, video)
    command = f'{ffmpeg_path} -i "{video}" -vn -acodec mp3 -q:a 0 -y "{temp_audio}"'
    log.run_cmd(command)

concat_file = os.path.join(temp_dir, "concat_list.txt")  # FFmpeg concat 输入文件
with open(concat_file, "w", encoding="utf-8") as f:
    for audio in temp_audio_files:
        f.write(f"file '{audio}'\n")

command = f'{ffmpeg_path} -f concat -safe 0 -i "{concat_file}" -c copy -y "{output_audio}"'
log.run_cmd(command)

# %%

#### 上传音频文件获得公网url ####

print("开始上传音频文件...")

bos = BOS()
speech_url = bos.upload(output_audio)

print(f"speech_url: {speech_url}")

# %%

#### 云端音频转写 ####

print("任务处理中...")
detailed_text = audio2text(speech_url)

with open(f"results/{video_name}_文字.txt", "w", encoding="utf-8") as f:
    f.write(detailed_text)

# %%

bos.delete()
