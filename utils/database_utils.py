#! /usr/bin/python
#coding=utf-8
from werkzeug.security import generate_password_hash
import pymysql
import sys
passwd = '123456'
dbname = 'deepbc'
def rop_help():
    print("\n-------------------------------")
    print("欢迎使用DeepBC系统数据库管理工具：")
    print("1:清空用户表")
    print("2:清空BC信息表")
    print("3:插入新用户")
    print("-------------------------------\n")

def clear_users():
    conn = pymysql.connect(user='root',port=8888,passwd='123456',host='localhost',db=dbname,charset='utf8')
    cur = conn.cursor()
    sql = "delete from users;"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("\n清空用户表成功！")

def clear_ropinfo():
    conn = pymysql.connect(user='root',port=8888,passwd='123456',host='localhost',db=dbname,charset='utf8')
    cur = conn.cursor()
    sql = "delete from bc_info;"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("\n清空rop诊断表成功！")

def insert_user():
    username = input("\n输入一个新的用户名:")
    passwd = input("输入你的密码:")
    pass_hash = generate_password_hash(passwd)
    conn = pymysql.connect(user='root',port=8888,passwd='123456',host='localhost',db=dbname,charset='utf8')
    cur = conn.cursor()
    insert_sql = "insert into users (username, password_hash) values ('" + username + "','" + pass_hash + "');"
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("\n创建用户成功！")

while  True:
    rop_help()
    choose = input("请输入你的选择:")
    if choose == '1':
        clear_users()
    elif choose == '2':
        clear_ropinfo()
    elif choose == '3':
        insert_user()
    else:
        print("\n输入错误！没有这项选择")
