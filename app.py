
# # -*- coding:utf-8 -*-
from flask import Flask, redirect, request, render_template, jsonify

from flask import Flask, request, jsonify
import jwt
# from ldap_client import LdapOpt
import mysql_client
import hashlib
import json
#
# import  ldap3 as ldap

# 创建 Flask 应用
app = Flask(__name__)


# 定义左侧菜单项
menu_items = [
    {'title': 'Home', 'url': '/'},
    {'title': 'About', 'url': '/about'},
    {'title': 'Contact', 'url': '/contact'}
]

@app.route('/')
def index():
    print("get /")
    return render_template('index.html')

#
# @app.route("/", methods=['POST'])  # 请求方式为post
# def reset_user_passwd():
#     data = json.loads(request.data)
#     username = data['username']
#     password = data['password']
#     if username == None:
#         return render_template('index.html')
#     ldapuser = LdapOpt(username=username, password=password)
#     if ldapuser.check_user():
#         print("查询ldap用户%s--- 正常" % username)
#         md5_password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
#         data = mysql_client.get_user_info(username)
#         print("密码对比", md5_password, data[2])
#
#         if md5_password == data[2]:
#             print("密码相等")
#         else:
#             print("修改密码")
#             mysql_client.update_accout_passwd(account_id=data[0], passwd=md5_password)
#
#         data = mysql_client.get_user_info(username)
#         dict = {}
#         if md5_password == data[2]:
#             msg = "密码同步成功"
#             dict["stat"] = "yes"
#             dict["msg"] = msg
#             print(msg)
#         else:
#             msg = "修改密码失败,请重试"
#             dict["stat"] = "no"
#             print(msg)
#             dict["msg"] = msg
#         return jsonify(dict)
#     else:
#         dict = {}
#         msg = "ldap认证失败,请重试"
#         print(msg)
#         dict["stat"] = "no"
#         dict["msg"] = msg
#         return jsonify(dict)

# 定义登录页面路由
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         #连接到 LDAP 服务器验证用户凭据
#         # try:
#         #     conn = ldap.initialize(LDAP_SERVER)
#         #     conn.simple_bind_s(f'uid={username},{LDAP_BASE_DN}', password)
#         #     conn.unbind_s()
#         #     return redirect('/')
#         # except ldap.INVALID_CREDENTIALS:
#         #     error = 'Invalid username or password'
#         #     return render_template('login.html', error=error)
#         # try:
#         #     print('123')
#         # except True:
#         #     return render_template('login.html', error=error)
#
#     return render_template('login.html')

# 定义主页路由
@app.route('/')
def home():
    return render_template('home.html', menu_items=menu_items)

# 定义关于页面路由
@app.route('/about')
def about():
    return render_template('about.html', menu_items=menu_items)

# 定义联系页面路由
@app.route('/contact')
def contact():
    return render_template('contact.html', menu_items=menu_items)




# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 设置密钥，用于加密和解密 token


# 定义登录路由
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 验证用户名和密码，假设验证通过
    # ...

    # 生成 token
    payload = {'username': username}
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # 返回包含 token 的响应
    return jsonify({'token': token})


# 定义需要进行身份验证的路由
@app.route('/protected', methods=['GET'])
def protected():
    # 从请求的头部获取 token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        # 解析 token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = payload['username']

        # 根据解析出的用户信息进行后续操作
        # ...

        return jsonify({'message': f'Welcome, {username}!'})
    except jwt.DecodeError:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(debug=True)


# app = Flask(__name__)
#
#

# @app.route("/sync/")
# def sync_users():
#     ldap_user_obj = LdapOpt()
#     ldap_users_list = ldap_user_obj.get_user_list()
#     mysql_users_list = mysql_client.user_list()
#     print(type(ldap_users_list), ldap_users_list)
#     print(type(mysql_users_list), mysql_users_list)
#     for n in mysql_users_list:
#         if ldap_users_list.get(n):
#             # print(n, "账号存在-更新邮箱")
#             #
#             mysql_client.update_accout_mail(ldap_users_list.get(n))
#         else:
#             print(n, "delete")
#             if n != "admin":
#                 mysql_client.delete_accout(account=n)
#     for k, v in ldap_users_list.items():
#         if k not in mysql_users_list:
#             # print("新建用户",k,v)
#             mysql_client.create_accout(account_dict=v)
#     return 'sync ok'
#
#
# if __name__ == '__main__':
#     app.run(
#         host='0.0.0.0',
#         port=80,
#         debug=False
#     )
