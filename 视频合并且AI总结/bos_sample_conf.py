#!/usr/bin/env python
# coding=utf-8

import json
import logging

from baidubce.auth.bce_credentials import BceCredentials

# 从Python SDK导入BOS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration

baidu_key_dict = json.load(open("baidu_key.json"))

# 设置BosClient的Host，Access Key ID和Secret Access Key
bos_host = "su.bcebos.com"
access_key_id = baidu_key_dict["access_key_id"]
secret_access_key = baidu_key_dict["secret_access_key"]

# 设置日志文件的句柄和日志级别
logger = logging.getLogger("baidubce.http.bce_http_client")
fh = logging.FileHandler("sample.log")
fh.setLevel(logging.DEBUG)

# 设置日志文件输出的顺序、结构和内容
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# 创建BceClientConfiguration
config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)
