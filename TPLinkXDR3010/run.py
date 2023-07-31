import os
import time
from utils import log

while 1:
    log.info("开始运行")
    os.system("python main.py")
    log.error("运行错误，准备重启")
    time.sleep(15)