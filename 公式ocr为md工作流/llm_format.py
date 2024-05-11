import os

import pyperclip
from zhipuai import ZhipuAI

api_key = os.environ.get("ZHIPU_AI_API_KEY", None)
client = ZhipuAI(api_key=api_key)

prompt = r"""
# Input
ocr结果
# Output
格式化结果
# Example1
Input:
```
假设$u$、$v$是已定义在论域$U$和$V$的两个语言变量，人类的语言控制规则为“如果
$u$是$A$,则$v$是$B$ ”,其蕴涵的模糊关系$R$为
$$R=(A\times B)\cup(\overline{A}\times V)$$
人类的语言控制规则为“如果$u$是$A$,则$v$是$B$;否则，$v$是$C$ ”
$$R=(A\times B)\cup(\overline{A}\times C)$$
```
Output:
```
假设 $u$、$v$ 是已定义在论域 $U$ 和 $V$ 的两个语言变量，人类的语言控制规则为“如果 $u$ 是 $A$，则 $v$ 是 $B$ ”，其蕴涵的模糊关系 $R$ 为

$$
R=(A\times B)\cup(\overline{A}\times V)
$$

人类的语言控制规则为“如果 $u$ 是 $A$，则 $v$ 是 $B$；否则，$v$ 是 $C$ ”

$$
R=(A\times B)\cup(\overline{A}\times C)
$$
```
# Example2
Input:
```
\begin{array}{rl}{TV-DV=0}\\{P_{_a}-P_{_R}=0}\\\end{array}
```
Output:
```
$$
TV-DV=0
$$

$$
P_{_a}-P_{_R}=0
$$
```

请理解并严格按照示例。
# WorkFlow
1. 读取输入ocr结果，理解文档内容，明白哪些是文本，哪些是latex公式。
2. 格式化，要求：
    - 内容与输入严格一致。
    - **行内公式格式为 $...$。**行内公式周围有中文字符时，中文字符与公式之间有一个空格。
    - 行间公式格式为 $$...$$，**且 $$ 单独占据一行**。
3. 直接输出格式化结果，不要有多余的语句。
# Init
如果你已完全理解并准备好了，请回复我明白了。
"""

input_ = """
# Input
{{input}}
"""

messages = [
    {"role": "user", "content": prompt},
    {"role": "assistant", "content": "明白了。"},
    {"role": "user", "content": input_},
]

# print(f"---\n{prompt}\n---")
# print(f"---\n{input_}\n---")

print("AI is working... Please wait.")

while 1:
    result = ""
    responses = client.chat.completions.create(
        model="glm-3-turbo",
        messages=messages,
        temperature=0.3,
        stream=True,
    )

    for response in responses:
        delta = response.choices[0].delta.content
        result += delta
        print(delta, end="")

    pyperclip.copy(result)

    print(
        "\n\nThe result has been copied to the clipboard.",
        "\nIf you are not satisfied with the result, please press Enter to re-run the program.",
        "\nOtherwise, please close the window.",
    )

    input()
