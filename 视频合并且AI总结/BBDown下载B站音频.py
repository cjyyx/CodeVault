"""
开始时运行

```bash
BBDown login
```

登录

"""

# %%

import os
import re
from datetime import datetime

from utils import Log

BV = "BV1XKxazfEk9"

# %%

# command = f"BBDown {BV}"
command = f"BBDown {BV} --audio-only"
print(f"运行命令：{command}\n{'-'*50}")
os.system(command)

# %%
