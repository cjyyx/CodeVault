# 下载的库
- pip install pyperclip
- pip install xlrd
- pip install pyautogui==0.9.50
- pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
- pip install pillow
- pip install keyboard
# 参考资料
- pyautogui库的使用说明 https://blog.csdn.net/qingfengxd1/article/details/108270159
- waterRPA https://www.bilibili.com/video/BV1T34y1o73U?spm_id_from=333.6.0.0
# 函数说明
|函数|说明|
|-|-|
|output_mouse_positon()|停顿1秒后，连续十次每隔半秒输出鼠标所在的位置|
|use_mouse_by_position(int x,int y,int model)|通过坐标使用鼠标，model{1:单击,2:双击,3:右键}|
|use_mouse_by_img(string imgPath,int model)|通过图片使用鼠标，model{1:单击,2:双击,3:右键}|
|keyboard_input(string content)|输入内容|
|mouse_scroll(int distance)|鼠标滚动|
|slp(int times)|暂停秒|
|wait_start()|按下'alt+x'停止等待|
|is_exit()|按下'alt+x'后输出为True|