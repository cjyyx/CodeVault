# %%
import json
import sqlite3
import time

import numpy as np


class OpenSqdb:
    '''返回游标'''

    def __init__(self, dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return False

# %%


def getData() -> np.array:
    data = np.random.random(8)
    return data

# %%
# 创建数据库


def creat_db():
    with OpenSqdb('data_record.sqlite') as cur:
        # time:时间戳
        cur.execute('''
        CREATE TABLE example_table
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time INTEGER,
            data TEXT
        );
        ''')

# %%
# 插入数据


def insert_db():
    data = getData()
    with OpenSqdb('data_record.sqlite') as cur:
        insert_stmt = '''
        INSERT INTO example_table (time,data) VALUES (?, ?)
        '''
        record = (
            int(time.time()),
            json.dumps(data.tolist())
        )
        cur.execute(insert_stmt, record)


# %%
if __name__ == '__main__':
    while 1:
        insert_db()

        now = int(time.time())
        timeArray = time.localtime(now)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print("[{}] insert ok".format(otherStyleTime))

        time.sleep(10)
