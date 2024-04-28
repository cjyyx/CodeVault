'''
来自
https://zhuanlan.zhihu.com/p/152666193

'''
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.filedialog import askopenfilename

import sqlite3


class TkSqlit3:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack(fill="both")
        # sql结果展示
        self.treeviewResult = None
        # 存储db路径
        self.db3 = None
        self.varSql = StringVar()
        # 数据库操作对象
        self.conn = None
        self.cursor = None
        # 添加菜单
        menubar = Menu(root)
        menubar.add_command(label='打开', command=self.openSelectDialog)
        root.config(menu=menubar)
        # sql输入窗口
        sqlInput = Entry(self.frame, textvariable=self.varSql)
        sqlInput.pack(fill=X)
        sqlInput.bind('<Return>', self.showSQLResult)
        # 表名列表
        self.lbTable = Listbox(self.frame, height=100)
        self.lbTable.pack(side=LEFT, fill=Y)
        self.lbTable.bind("<<ListboxSelect>>", self.tableSelect)
        # 滚动条
        self.scrollBarX = Scrollbar(self.frame, orient="horizontal")
        self.scrollBarX.pack(side=BOTTOM, fill=X)
        self.scrollBarY = Scrollbar(self.frame, orient="vertical")
        self.scrollBarY.pack(side=RIGHT, fill=Y)

    def openSelectDialog(self):
        self.db3 = askopenfilename(
            filetypes=[('sqlite', '*.sqlite'), ('db', '*.db')], initialdir='.')
        self.conn = sqlite3.connect(self.db3)
        self.cursor = self.conn.cursor()
        self.root.title(self.db3)
        self.cursor.execute(
            "select name from sqlite_master where type='table'")
        for item in self.cursor.fetchall():
            self.lbTable.insert(END, item[0])

    def showSQLResult(self, event):
        result = self.cursor.execute(self.varSql.get())
        heads = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchall()
        self.showDataTable(heads, result)

    def tableSelect(self, event):
        idx = self.lbTable.curselection()[0]
        tableSelect = self.lbTable.get(idx)
        self.cursor.execute(f"select * from {tableSelect}")
        heads = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchall()
        self.showDataTable(heads, result)

    def showDataTable(self, heads, result):
        if self.treeviewResult:
            self.treeviewResult.destroy()
        self.treeviewResult = Treeview(
            self.frame,
            height=len(result),
            columns=[str(i) for i in range(len(heads))],
            show='headings',
            xscrollcommand=self.scrollBarX.set,
            yscrollcommand=self.scrollBarY.set)
        self.scrollBarX.config(command=self.treeviewResult.xview)
        self.scrollBarY.config(command=self.treeviewResult.yview)
        for i, text in enumerate(heads):
            self.treeviewResult.column(str(i), width=100, anchor="w")
            self.treeviewResult.heading(str(i), text=text)
        for i, row in enumerate(result):
            self.treeviewResult.insert('', i, values=row)
        self.treeviewResult.pack(side=LEFT, fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    root.geometry("%dx%d" % (800, 600))
    TkSqlit3(root)
    root.mainloop()
