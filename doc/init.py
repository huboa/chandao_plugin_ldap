
'''
要通过 Python 创建一个简单的网站，带有 LDAP 登录和左侧菜单，你可以使用 Flask 框架来实现。Flask 是一个轻量级的 Web 框架，易于学习和使用。以下是一个基本的示例：

首先，确保已安装 Flask 和 python-ldap 包。你可以使用以下命令进行安装：

pip install Flask python-ldap
然后，创建一个名为 app.py 的 Python 文件，并添加以下代码：

python
'''
from flask import Flask, render_template, request, redirect
import ldap

# 创建 Flask 应用
app = Flask(__name__)

# 配置 LDAP 服务器信息
LDAP_SERVER = 'ldap://your_ldap_server'
LDAP_BASE_DN = 'your_base_dn'

# 定义左侧菜单项
menu_items = [
    {'title': 'Home', 'url': '/'},
    {'title': 'About', 'url': '/about'},
    {'title': 'Contact', 'url': '/contact'}
]

# 定义登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 连接到 LDAP 服务器验证用户凭据
        try:
            conn = ldap.initialize(LDAP_SERVER)
            conn.simple_bind_s(f'uid={username},{LDAP_BASE_DN}', password)
            conn.unbind_s()
            return redirect('/')
        except ldap.INVALID_CREDENTIALS:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

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

if __name__ == '__main__':
    app.run(debug=True)
'''
接下来，创建一个名为 templates 的文件夹，并在其中创建以下模板文件：
login.html：登录页面的 HTML 模板。
html
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <h2>Login</h2>
    {% if error %}
      <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="post" action="/login">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" required><br><br>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" required><br><br>
      <input type="submit" value="Login">
    </form>
  </body>
</html>

base.html：用作其他页面模板的基础模板，包括左侧菜单。
html
<!DOCTYPE html>
<html>
  <head>
    <title>My Website</title>
  </head>
  <body>
    <div>
      <h2>Menu</h2>
      <ul>
        {% for item in menu_items %}
          <li><a href="{{ item.url }}">{{ item.title }}</a></li>
        {% endfor %}
      </ul>
    </div>
    <div>
      {% block content %}{% endblock %}
    </div>
  </body>
</html>


home.html：主页的 HTML 模板。
html
{% extends 'base.html' %}

{% block content %}
  <h2>Welcome to the Home Page!</h2>
{% endblock %}


about.html：关于页面的 HTML 模板。
html
{% extends 'base.html' %}

{% block content %}
  <h2>About Us</h2>
  <p>This is the About page.</p>
{% endblock %}


contact.html：联系页面的 HTML 模板。
html
{% extends 'base.html' %}

{% block content %}
  <h2>Contact Us</h2>
  <p>This is the Contact page.</p>
{% endblock %}
最后，打开终端并在命令行中执行 python app.py 来运行应用程序。

通过浏览器访问 http://localhost:5000，你将看到一个简单的网站，带有登录功能和左侧菜单。请根据你的需求进行进一步修改和扩展。

请注意，在实际使用时，你需要根据你自己的 LDAP 服务器配置和页面设计进行适当的调整。此示例仅提供了一个起点，你可以根据需要进行定制化开发。
'''


