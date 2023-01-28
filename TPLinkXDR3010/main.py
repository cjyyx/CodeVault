# %%

import time

import requests
import win32api
import win32con
import win32gui


# %%

def getLoginStok() -> str:
    url = "http://tplogin.cn/"
    data = '''
    {"method":"do","login":{"password":"0bcn98KAKlxfbwK"}}
    '''
    req = requests.post(url, data=data).json()
    return req["stok"]


def getHostInfoList() -> list:
    url = "http://tplogin.cn/stok={}/ds".format(getLoginStok())
    data = '''
    {"system":{"name":["sys"]},"hosts_info":{"table":"host_info"},"network":{"name":"iface_mac"},"function":{"name":"new_module_spec"},"method":"get"}
    '''
    req = requests.post(url, data=data).json()
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
        hnl = getHostNameList()
        print(hnl)

        if miH:
            if mN not in hnl:
                miH = False
                alart("m leave home!!!")
        elif not miH:
            if mN in hnl:
                miH = True
                alart("m arrive home!!!!!!!!!!!!!!")

        time.sleep(15)
