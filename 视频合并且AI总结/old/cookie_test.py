from selenium import webdriver

options = webdriver.EdgeOptions()
options.add_argument("--user-data-dir=C:\\Users\\cjy\\AppData\\Local\\Microsoft\\Edge\\User Data")
options.add_argument("--profile-directory=Default")
service = webdriver.EdgeService(executable_path=r"C:\Users\cjy\Desktop\edgedriver_win64\msedgedriver.exe")
driver = webdriver.Edge(service=service,options=options)
driver.get("https://live.bilibili.com/1757326062")

# driver.implicitly_wait(20)

# cookies = driver.get_cookies()
# for cookie in cookies:
#     print(cookie)
# driver.quit()

input()
