import os

from utils import BOS, audio2text


for filename in os.listdir("input_recording"):

    recording_file = f"input_recording/{filename}"
    recording_name = os.path.splitext(filename)[0]

    print(f"processing {recording_file}")

    bos = BOS()
    speech_url = bos.upload(recording_file)

    print(f"speech_url: {speech_url}")

    detailed_text = audio2text(speech_url)

    with open(f"results/{recording_name}_文字.txt", "w", encoding="utf-8") as f:
        f.write(detailed_text)

    bos.delete()
