"""
dict 数据库处理
功能： 提供服务端的所有数据库操作
"""
import pymysql
import hashlib

SALT = "#SF_"  # 盐


class Database:
    def __init__(self, host="localhost", port=3306,
                 user="root", pwd="123456", charset="utf8", database="dict"):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.charset = charset
        self.database = database
        self.connect_db()  # 连接数据库

    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.pwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.db.close()

    # 注册操作
    def register(self, name, pwd):
        sql = "select * from users where username ='%s'" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False
        # 密码加密处理
        hash = hashlib.md5((name + SALT).encode())
        hash.update(pwd.encode())
        pwd = hash.hexdigest()

        sql = "insert into users(username,pwd) values(%s,%s)"
        try:
            self.cur.execute(sql, [name, pwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def signin(self, name, pwd):
        hash = hashlib.md5((name + SALT).encode())
        hash.update(pwd.encode())
        pwd = hash.hexdigest()
        sql = "select * from users where username ='%s' and pwd ='%s'" % (name, pwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    def record(self, name, word):
        sql = "insert into records(username,word) values(%s,%s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def check(self, word):
        sql = "select mean from words where word ='%s'" % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    def history(self,name):
        sql = "select username,word,time from records  \
              where username ='%s'order by time desc limit 10"%name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        return  r