from flask import Flask, request, redirect, render_template, jsonify,abort,session,flash
from datetime import timedelta
import json
import jwt


# 创建 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = '2VW4K1LN407ZJTNM'  # 设置密钥，用于加密和解密 token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# print(user_list.get('test'))


#定义全局请求处理函数
@app.before_request
def filter_token():
    # 排除登录页面和静态资源等不需要验证的路由
    if request.path == '/login' or request.path.startswith('/static') or request.path == '/get-token' :
        return
    token = request.cookies.get('token')  #
    if token:
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print('decode_token', payload)
            return
        except (jwt.DecodeError, IndexError):
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/get-token', methods=['GET', 'POST'])
def get_token():
    # 获取用户名和
    username = request.json.get('username')
    password = request.json.get('password')

    # 在这里验证用户名和密码，验证通过后生成 token
    payload = {username: password}
    print('encode_token_payload', payload)
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # 返回包含 token 的响应
    return jsonify({'token': token})


# @app.route('/clear-token', methods=['GET'])
# def clear_token():
#     headers = request.headers
#     if 'Authorization' in headers:
#         headers.pop('Authorization')
#     return 'Token cleared'


# 定义其他路由
@app.route('/home')
def index():
    menu_items = [
        {'url': '/home', 'title': '首页'},
        {'url': '/about', 'title': '关于我们'},
        {'url': '/contact', 'title': '联系我们'}
    ]

    return render_template('home.html', menu_items=menu_items)

@app.route('/')
def home():
    return redirect('/home')  # 将根路径重定向到首页


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
