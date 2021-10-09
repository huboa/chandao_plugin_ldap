import json
import os
import pymysql


def get_mysql_config():
    f = open('config.json', 'r')
    content = f.read()
    config = json.loads(content)
    f.closed
    mysql_conf_list = [
        "MYSQL_host",
        "MYSQL_port",
        "MYSQL_user",
        "MYSQL_passwd",
        "MYSQL_database"]
    mysql_config_dict = {}
    for n in mysql_conf_list:
        if os.getenv(n) == None:
            mysql_config_dict[n] = config.get("MYSQL").get(n)
        else:
            mysql_config_dict[n] = os.getenv(n)
    return mysql_config_dict


def db_connect():
    host = get_mysql_config()["MYSQL_host"]
    port = int(get_mysql_config()["MYSQL_port"])
    user = get_mysql_config()["MYSQL_user"]
    passwd = get_mysql_config()["MYSQL_passwd"]
    database = get_mysql_config()["MYSQL_database"]
    # print(host,port,user,passwd,database)
    db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, database=database)
    return db


def user_list():
    cursor = db_connect().cursor()
    sql = "select account from zt_user;"
    # print(sql,'=====userl_list========')
    cursor.execute(sql)
    # data = cursor.fetchone()
    data = cursor.fetchall()
    # print("Database version : %s " % data)
    user_list = []
    for n in data:
        user_list.append(n[0])
    user_list = list(set(user_list))
    # 打印所有用户
    print(user_list, type(user_list))
    return user_list


def get_user_info(accout):
    sql = "select id,account,password,email from zt_user where account like '%s' ;" % (accout)
    cursor = db_connect().cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    # print(host,"host")
    # print("mysql--getMysql",data)
    if data is None:
        return False
    else:
        return data


def update_accout_passwd(account_id, passwd):
    sql = "UPDATE zt_user set password='%s' where id='%s';" % (passwd, account_id)
    # print("修改用户",sql)
    cursor = db_connect().cursor()
    cursor.execute(sql)
    return True


def update_accout_mail(account_dict=None):
    account = account_dict.get("cn")
    email = account_dict.get("mail")
    # print(account,email,)
    userinfo = get_user_info(account)
    # print("userinfo",userinfo)
    if userinfo[3] != email:
        sql = "UPDATE zt_user set email='%s' where account='%s';" % (email, account)
        cursor = db_connect().cursor()
        cursor.execute(sql)
        # print("修改邮箱",sql)
    return True


def create_accout(account_dict):
    account = account_dict.get("cn")
    mail = account_dict.get("mail")
    realname = account_dict.get("displayname")
    # print(account,mail,realname)
    # sql="INSERT INTO zt_user (account,email,realname,birthday,`join`,locked,commiter) VALUES ('zhaosc2','zhaosc@digitlink.cn','赵胜冲','2020-07-15','2020-07-15','2020-07-15','admin')"
    sql = "insert into zt_user(account,email,realname,birthday,`join`,locked,commiter) values ('%s','%s','%s','2020-07-15','2020-07-15','2020-07-15','admin')" % (
        account, mail, realname)
    # print(sql)
    cursor = db_connect().cursor()
    cursor.execute(sql)
    return account


def delete_accout(account):
    "DELETE FROM `chandao`.`zt_user` WHERE `id` = 7"
    sql = "UPDATE zt_user set `deleted` = '1'  where account='%s'" % (account)
    print(sql)
    cursor = db_connect().cursor()
    cursor.execute(sql)
    return True


# 调试用
# user_list()
