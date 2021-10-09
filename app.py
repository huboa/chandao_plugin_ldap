# -*- coding:utf-8 -*-
from flask import Flask
from flask import request, render_template, jsonify
from ldap_client import LdapOpt
import mysql_client
import hashlib
import json

app = Flask(__name__)


@app.route('/')
def index():
    print("get /")
    return render_template('index.html')


@app.route("/", methods=['POST'])  # 请求方式为post
def reset_user_passwd():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    if username == None:
        return render_template('index.html')
    ldapuser = LdapOpt(username=username, password=password)
    if ldapuser.check_user():
        print("查询ldap用户%s--- 正常" % username)
        md5_password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        data = mysql_client.get_user_info(username)
        print("密码对比", md5_password, data[2])

        if md5_password == data[2]:
            print("密码相等")
        else:
            print("修改密码")
            mysql_client.update_accout_passwd(account_id=data[0], passwd=md5_password)

        data = mysql_client.get_user_info(username)
        dict = {}
        if md5_password == data[2]:
            msg = "密码同步成功"
            dict["stat"] = "yes"
            dict["msg"] = msg
            print(msg)
        else:
            msg = "修改密码失败,请重试"
            dict["stat"] = "no"
            print(msg)
            dict["msg"] = msg
        return jsonify(dict)
    else:
        dict = {}
        msg = "ldap认证失败,请重试"
        print(msg)
        dict["stat"] = "no"
        dict["msg"] = msg
        return jsonify(dict)


@app.route("/sync/")
def sync_users():
    ldap_user_obj = LdapOpt()
    ldap_users_list = ldap_user_obj.get_user_list()
    mysql_users_list = mysql_client.user_list()
    print(type(ldap_users_list), ldap_users_list)
    print(type(mysql_users_list), mysql_users_list)
    for n in mysql_users_list:
        if ldap_users_list.get(n):
            # print(n, "账号存在-更新邮箱")
            #
            mysql_client.update_accout_mail(ldap_users_list.get(n))
        else:
            print(n, "delete")
            if n != "admin":
                mysql_client.delete_accout(account=n)
    for k, v in ldap_users_list.items():
        if k not in mysql_users_list:
            # print("新建用户",k,v)
            mysql_client.create_accout(account_dict=v)
    return 'sync ok'


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=False
    )
