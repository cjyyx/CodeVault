import time

import keyboard
import pyautogui
import pyperclip


def output_mouse_position():
    time.sleep(1)  # 准备时间
    print("开始获取鼠标位置")
    try:
        for i in range(10):
            # Get and print the mouse coordinates.
            x, y = pyautogui.position()
            positionStr = "鼠标坐标点（X,Y）为：{},{}".format(
                str(x).rjust(4), str(y).rjust(4)
            )
            pix = pyautogui.screenshot().getpixel((x, y))  # 获取鼠标所在屏幕点的RGB颜色
            positionStr += (
                " RGB:("
                + str(pix[0]).rjust(3)
                + ","
                + str(pix[1]).rjust(3)
                + ","
                + str(pix[2]).rjust(3)
                + ")"
            )
            print(positionStr)
            time.sleep(0.5)  # 停顿时间
    except:
        print("获取鼠标位置失败")


def use_mouse_by_position(x: int, y: int, model: int):
    if model == 1:
        pyautogui.click(x, y, clicks=1, interval=0.2, duration=0.2, button="left")
        print("单击 {},{}".format(x, y))
    elif model == 2:
        pyautogui.click(x, y, clicks=2, interval=0.2, duration=0.2, button="left")
        print("双击 {},{}".format(x, y))
    elif model == 3:
        pyautogui.click(x, y, clicks=1, interval=0.2, duration=0.2, button="right")
        print("右键 {},{}".format(x, y))
    else:
        print("错误的model")


def use_mouse_by_img(imgPath: str, model: int):
    while True:
        location = pyautogui.locateCenterOnScreen(imgPath, confidence=0.9)
        if location is not None:

            if model == 1:
                pyautogui.click(
                    location.x,
                    location.y,
                    clicks=1,
                    interval=0.2,
                    duration=0.2,
                    button="left",
                )
                print("单击", imgPath)
            elif model == 2:
                pyautogui.click(
                    location.x,
                    location.y,
                    clicks=2,
                    interval=0.2,
                    duration=0.2,
                    button="left",
                )
                print("双击", imgPath)
            elif model == 3:
                pyautogui.click(
                    location.x,
                    location.y,
                    clicks=1,
                    interval=0.2,
                    duration=0.2,
                    button="right",
                )
                print("右键", imgPath)
            else:
                print("错误的model")

            break
        print("未找到匹配图片,0.1秒后重试")
        time.sleep(0.1)


def keyboard_input(content: str):
    pyperclip.copy(content)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    print("输入:", content)


def mouse_scroll(distance: int):
    pyautogui.scroll(distance)
    print("滚轮滑动{}距离".format(distance))


def slp(times: int):
    time.sleep(times)


is_altx = False


def test_a():
    global is_altx
    is_altx = True


def wait_start():
    print("请按alt+x开始")
    keyboard.wait("alt+x")
    keyboard.add_hotkey("alt+x", test_a)
    print("现在开始")


def is_exit():
    return is_altx
