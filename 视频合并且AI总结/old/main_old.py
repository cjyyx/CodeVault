# %%
import json
import os
import subprocess
import tempfile
import time
import uuid
from datetime import datetime

import requests
from baidubce.services.bos.bos_client import BosClient

import bos_sample_conf

ffmpeg_path = "C:/Users/cjy/Desktop/DouyinLiveRecorder_v4.0.3/ffmpeg/ffmpeg.exe"
base_path = "C:/Users/cjy/Desktop/DouyinLiveRecorder_v4.0.3/downloads/B站直播/憨大炒股"

video_name = "憨大炒股_2025-07-20_19-02-10"

output_audio = f"{video_name}_合并.mp3"

# %%


class Log:
    def __init__(self, log_file):
        self.log_file = log_file
        self.log = open(log_file, "w", encoding="utf-8")

    def write(self, text):
        self.log.write(text)
        self.log.flush()

    def breakpoint(self):
        self.write("-" * 50 + "\n")

    def close(self):
        self.log.close()

    def run_cmd(self, command):
        self.write(f"执行命令: {command}\n")
        self.breakpoint()
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        for line in process.stdout:
            log.write(line)
        process.wait()
        self.breakpoint()


log_file = "log"
log = Log(log_file)

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

bos_client = BosClient(bos_sample_conf.config)
bucket_name = "recording-storage"
object_key = str(uuid.uuid4())

bos_client.put_object_from_file(bucket_name, object_key, output_audio)

speech_url = bos_client.generate_pre_signed_url(bucket_name, object_key, expiration_in_seconds=7200).decode(encoding="utf-8")
print(f"speech_url: {speech_url}")

# %%

#### 云端音频转写 ####

baidu_key_dict = json.load(open("baidu_key.json"))
API_KEY = baidu_key_dict["speech_api_key"]
SECRET_KEY = baidu_key_dict["speech_secret_key"]


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


url = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + get_access_token()

payload = json.dumps(
    {
        "speech_url": speech_url,
        "format": "mp3",
        "pid": 80006,
        "rate": 16000,
    },
    ensure_ascii=False,
)
headers = {"Content-Type": "application/json", "Accept": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))

result = json.loads(response.text)
task_id = result["task_id"]

# %%

#### 获取音频转写结果 ####

print("任务进行中...")
while 1:

    url = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + get_access_token()

    payload = json.dumps({"task_ids": [task_id]}, ensure_ascii=False)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))

    result = json.loads(response.text)
    if result["tasks_info"][0]["task_status"] == "Running":
        time.sleep(2)
    else:
        break


all_text = result["tasks_info"][0]["task_result"]["result"][0]


detailed_text = ""
for seg in result["tasks_info"][0]["task_result"]["detailed_result"]:
    detailed_text += seg["res"][0]

    begin_time = seg["begin_time"] / 1000
    detailed_text += f"\t{begin_time:.0f}s"
    detailed_text += "\n"

with open(f"{video_name}_文字.txt", "w", encoding="utf-8") as f:
    f.write(detailed_text)

# %%

bos_client.delete_object(bucket_name, object_key)
