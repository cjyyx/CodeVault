#!/usr/bin/env python
# coding=utf-8

import subprocess
import os
import json
import logging
import uuid
from http import HTTPStatus
from urllib import request

import dashscope
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bos.bos_client import BosClient

baidu_key_dict = json.load(open("baidu_key.json"))

for dirname in ["input_video", "input_recording", "results", "tmp"]:
    if not os.path.exists(dirname):
        os.makedirs(dirname)


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
            self.log.write(line)
        process.wait()
        self.breakpoint()


class BOS:
    """上传音频文件获得公网url"""

    def __init__(self):
        bos_host = "su.bcebos.com"
        access_key_id = baidu_key_dict["access_key_id"]
        secret_access_key = baidu_key_dict["secret_access_key"]

        config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)

        self.bos_client = BosClient(config)
        self.bucket_name = "recording-storage"

    def upload(self, file_path):
        self.object_key = str(uuid.uuid4())
        self.bos_client.put_object_from_file(self.bucket_name, self.object_key, file_path)

        speech_url = self.bos_client.generate_pre_signed_url(self.bucket_name, self.object_key, expiration_in_seconds=7200).decode(encoding="utf-8")

        return speech_url

    def delete(self):
        self.bos_client.delete_object(self.bucket_name, self.object_key)


def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def audio2text(speech_url):
    """云端音频转写"""

    task_response = dashscope.audio.asr.Transcription.async_call(
        model="paraformer-v2",
        file_urls=[speech_url],
        language_hints=["zh", "en"],
    )

    transcription_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)

    if transcription_response.status_code == HTTPStatus.OK:
        for transcription in transcription_response.output["results"]:
            url = transcription["transcription_url"]
            result = json.loads(request.urlopen(url).read().decode("utf8"))
        print("transcription done!")
    else:
        print("Error: ", transcription_response.output.message)

    url = transcription_response.output["results"][0]["transcription_url"]
    result = json.loads(request.urlopen(url).read().decode("utf8"))

    all_text = result["transcripts"][0]["text"]

    detailed_text = ""
    for seg in result["transcripts"][0]["sentences"]:
        detailed_text += seg["text"]

        begin_time = int(seg["begin_time"] / 1000)
        detailed_text += f"\t{seconds_to_hms(begin_time)}"
        detailed_text += "\n"

    return detailed_text
