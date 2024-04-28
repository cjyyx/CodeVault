from DataMaintainer import *
from config import *

print("请输入 course_id")
course_id = input()
print("请输入 sub_id")
sub_id = input()

sub_maintain(course_id,sub_id)

dp = data_path.replace('/','\\')
os.system(f"explorer {dp}\\{course_id}\\{sub_id}\\enhanced_ppt")

while 1:
    sub_maintain(course_id,sub_id)
    time.sleep(1)