"""
开始时运行

```bash
BBDown login
```

登录

"""

# %%

import os
import re
from datetime import datetime

from utils import Log

BV = "BV19YbgzrEHD"

# %%

# command = f"BBDown {BV}"
command = f"BBDown {BV} --sub-only --skip-ai false"
print(f"运行命令：{command}\n{'-'*50}")
os.system(command)

# %%

srt_file = [f for f in os.listdir() if f.endswith(".srt")]

if len(srt_file) == 1:
    srt_file = srt_file[0]
else:
    raise Exception("无法确定字幕文件")

with open(srt_file, "r", encoding="utf-8") as f:
    srt_txt = f.read()
srt_txt

# %%

pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)'
matches = re.findall(pattern, srt_txt, re.DOTALL)

subtitles = []

for match in matches:
    index = int(match[0])
    start_time = match[1]
    end_time = match[2]
    text = match[3].strip()
    subtitles.append({
        'index': index,
        'start_time': start_time,
        'end_time': end_time,
        'text': text
    })

detailed_text = ""
for subtitle in subtitles:
    detailed_text += f"{subtitle['text']}\t{subtitle['start_time'][:-4]}\n"


with open(f"results/{srt_file[:-4]}_{BV}.txt", "w", encoding="utf-8") as f:
    f.write(detailed_text)

os.remove(srt_file)
