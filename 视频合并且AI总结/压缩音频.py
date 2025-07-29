import os

ffmpeg_path = "C:/Users/cjy/Desktop/DouyinLiveRecorder_v4.0.3/ffmpeg/ffmpeg.exe"

input_file = "憨大炒股_2025-07-24_19-07-05_合并.mp3"

output_file = "output.mp3"

# 压缩

# command = f'{ffmpeg_path} -i "{input_file}" -c:a libmp3lame -q:a 4 -ar 22050 -ac 1 "{output_file}"'
command = f'{ffmpeg_path} -i "{input_file}" -c:a libmp3lame -q:a 3 -ar 44100 "{output_file}"'
os.system(command)


