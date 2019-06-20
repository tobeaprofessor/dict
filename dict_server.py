"""
dict 服务端
功能：业务逻辑的处理
模型：多进程 TCP并发
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from dict_database import *
import time

#全局变量
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

db = Database()

#历史记录
def do_hist(c,data):
    name = data.split(" ")[1]
    r = db.history(name)
    if not r:
        c.send(b"Fail")
        return
    c.send(b"OK")
    for i in r:
        msg = "%s %-16s %s"%i
        time.sleep(0.1)
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b"##")

#查询单词
def do_check(c,data):
    tmp = data.split(" ")
    username = tmp[1]
    word = tmp[2]
    db.record(username,word)
    #找到返回解释，没找到返回None
    mean = db.check(word)
    if not mean:
        c.send("没有找到该单词".encode())
    else:
        c.send(mean.encode())


#登录处理
def do_signin(c,data):
    tmp = data.split(" ")
    username = tmp[1]
    pwd = tmp[2]
    if db.signin(username,pwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

#注册处理
def do_register(c,data):
    tmp = data.split(" ")
    username = tmp[1]
    pwd = tmp[2]
    if db.register(username,pwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

#接收客户端请求
def request(c):
    db.create_cursor() #生成游标
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if not data or data =="E":
            return False
        elif data[0] == "R":
            do_register(c,data)
        elif data[0] == "L":
            do_signin(c,data)
        elif data[0] =="C":
            do_check(c,data)
        elif data[0] == "H":
            do_hist(c,data)

#搭建网络
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)

    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    #循环等待客户端的连接
    print("listen from port 8888")
    while True:
        try:
            c,addr = s.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit()
        except Exception as e:
            print(e)
            continue

        #为客户端创建子进程
        p = Process(target=request,args=(c,))
        p.daemon = True
        p.start()

main()