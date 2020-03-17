import os
import sys
import sqlite3
sys.path.append('./')
# 数据库封装
# 把数据库的操作函数都封装到一个函数里面，避免麻烦
def sql_dql(sql):
    db = sqlite3.connect('nonebot.db')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        db.close()
        return result
    except:
        return {}


def sql_dml(sql):
    db = sqlite3.connect('nonebot.db')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        db.close()
        return 1
    except:
        db.rollback()
        db.close()
        return 0