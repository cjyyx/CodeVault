# %%

from utils import log
import time

import requests
import win32api
import win32con


# %%

proxies = {"http": None, "https": None}

def getLoginStok() -> str:
    url = "http://tplogin.cn/"
    data = '''
    {"method":"do","login":{"password":"0bcn98KAKlxfbwK"}}
    '''
    req = requests.post(url, data=data, proxies=proxies).json()
    return req["stok"]


def getHostInfoList() -> list:
    url = "http://tplogin.cn/stok={}/ds".format(getLoginStok())
    data = '''
    {"system":{"name":["sys"]},"hosts_info":{"table":"host_info"},"network":{"name":"iface_mac"},"function":{"name":"new_module_spec"},"method":"get"}
    '''
    req = requests.post(url, data=data, proxies=proxies).json()
    return req["hosts_info"]["host_info"]


def getHostNameList() -> list:
    tlist = list(map(
        lambda x: list(x.values())[0]["hostname"],
        getHostInfoList()
    ))

    tlist = list(map(
        lambda x: x.replace("%2D", "-"),
        tlist
    ))

    return tlist

# %%

def alart(text: str):
    hwnd = win32api.MessageBox(
        0, text, "alart", win32con.MB_OK | win32con.MB_SYSTEMMODAL)  # MB_SYSTEMMODAL用于置顶

# %%


if __name__ == "__main__":
    miH = False
    mN = "OPPO-Reno-Z"

    while 1:
        try:
            hnl = getHostNameList()

            log.info(f"当前连接设备 {hnl}")

            if miH:
                if mN not in hnl:
                    miH = False
                    log.info("m leave home!!!")
                    alart("m leave home!!!")
            elif not miH:
                if mN in hnl:
                    miH = True
                    log.info("m arrive home!!!!!!!!!!!!!!")
                    alart("m arrive home!!!!!!!!!!!!!!")
        except Exception as e:
            log.error(f"发生错误 {e}")
            alart(f"发生错误 {e}")

        time.sleep(15)
