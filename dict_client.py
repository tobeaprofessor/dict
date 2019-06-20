"""
dict 客户端
功能：根据用户输入，发送请求，得到结果
结构：一级界面 -- 注册 登录 退出
     二级界面 -- 查单词 历史记录 注销
"""
import getpass  # 隐藏输入  只能在终端运行 pycharm不支持
from socket import *
import sys

ADDR = ("127.0.0.1", 8888)
sockfd = socket()
sockfd.connect(ADDR)


def do_hist(name):
    msg = "H %s" % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == "OK":
        while True:
            data = sockfd.recv(1024).decode()
            if data == "##":
                break
            print(data)
    else:
        print("没有历史记录")


def do_check(name):
    while True:
        word = input("请输入单词,输入##退回上级界面：")
        if word == "##":
            break
        msg = "C %s %s" % (name, word)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        print(data)


# 二级界面
def login(name):
    while True:
        print("1查单词")
        print("2历史记录")
        print("3注销")
        choice = input("请输入1|2|3:")
        if choice == "1":
            do_check(name)
        elif choice == "2":
            do_hist(name)
        elif choice == "3":
            return
        else:
            print("请输入正确选项")


def do_signin():
    while True:
        username = input("请输入用户名")
        pwd = getpass.getpass()
        msg = "L %s %s" % (username, pwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == "OK":
            print("登录成功")
            login(username)
            return
        else:
            print("登录失败")
            return


def do_register():
    while True:
        username = input("请输入用户名")
        pwd = getpass.getpass()
        pwd_ = getpass.getpass("again:")
        if (" " in username) or (" " in pwd):
            print("用户名或密码不能有空格")
            continue
        if pwd != pwd_:
            print("两次密码输入不一致")
            continue
        msg = "R %s %s" % (username, pwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(username)
            return
        else:
            print("注册失败")
            return


def main():
    while True:
        print("1登录")
        print("2注册")
        print("3退出")
        choice = input("请输入1|2|3:")
        if choice == "1":
            do_signin()
        elif choice == "2":
            do_register()
        elif choice == "3":
            sockfd.send(b"E")
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")


main()
