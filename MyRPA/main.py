from RPAtools import *

wait_start()
use_mouse_by_img("1.png", 1)
use_mouse_by_img("2.png", 1)
keyboard_input("halloworld")
use_mouse_by_img("3.png", 1)
for _ in range(100):
    mouse_scroll(-10)
    slp(0.2)
    if is_exit():
        exit()
