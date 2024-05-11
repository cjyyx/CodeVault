# %%

with open('AppUsage_example.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# %%

lines = data.strip().split('\n')

# %%

"""
[日期, [
    应用名称, 应用标识, 格式化时间, 使用时长（ms）
]]
"""
structured_data = []
current_date = None

for line in lines:
    if line.startswith('202'):  # 检查是否是日期行
        current_date = l3ine.split(',')[0]
        structured_data[current_date] = []
    else:
        # 解析应用数据
        parts = line.split(',')
        if len(parts) > 1:  # 确保是应用数据行
            app_data = {
                '应用名称': parts[1].strip(),
                '应用标识': parts[2].strip(),
                '格式化时间': parts[3].strip(),
                '使用时长（ms）': int(parts[4].strip()),
                '启动次数': int(parts[5].strip()),
                '通知次数': int(parts[6].strip())
            }
            structured_data[current_date].append(app_data)
