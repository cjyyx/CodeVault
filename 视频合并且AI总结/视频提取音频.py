import os

from utils import Log
from datetime import datetime

log = Log("ffmpeg.log")
log.write(f"日志开始时间: {datetime.now()}\n")
log.breakpoint()

for filename in os.listdir("input_video"):

    video_file = f"input_video/{filename}"
    video_name = os.path.splitext(filename)[0]

    audio_file = f"input_recording/{video_name}.mp3"

    print(f"processing {video_file}")

    command = f'ffmpeg -i "{video_file}" -vn -acodec mp3 -q:a 0 -y "{audio_file}"'
    log.run_cmd(command)
